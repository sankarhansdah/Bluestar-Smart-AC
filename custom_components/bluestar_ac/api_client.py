"""API client for Bluestar Smart AC."""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

import httpx

from .const import (
    BASE_URL,
    LOGIN_URL,
    DEVICES_URL,
    DEVICE_STATE_URL,
    DEVICE_INFO_URL,
    DEFAULT_HEADERS,
    POWER_ON,
    POWER_OFF,
)

_LOGGER = logging.getLogger(__name__)


class BluestarClient:
    """Client for Bluestar Smart AC API."""

    def __init__(self, email: str, password: str, region: str = "IN"):
        """Initialize the client."""
        self.email = email
        self.password = password
        self.region = region
        self._session_token: Optional[str] = None
        self._token_expiry: float = 0
        self._client: Optional[httpx.AsyncClient] = None
        self._lock = asyncio.Lock()

    async def _ensure_client(self) -> None:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                headers=DEFAULT_HEADERS.copy()
            )

    async def _get_auth_headers(self) -> Dict[str, str]:
        """Get headers with authentication."""
        headers = DEFAULT_HEADERS.copy()
        if self._session_token:
            headers["X-APP-SESSION"] = self._session_token
        return headers

    async def _make_request(
        self, method: str, url: str, **kwargs
    ) -> Optional[httpx.Response]:
        """Make HTTP request with error handling."""
        await self._ensure_client()
        
        try:
            response = await self._client.request(method, url, **kwargs)
            _LOGGER.debug(
                "%s %s: %s", method, url, response.status_code
            )
            
            if response.status_code == 401:
                _LOGGER.warning("Authentication failed, attempting re-login")
                await self._login()
                # Retry with new token
                if self._session_token:
                    headers = kwargs.get("headers", {})
                    headers["X-APP-SESSION"] = self._session_token
                    kwargs["headers"] = headers
                    response = await self._client.request(method, url, **kwargs)
            
            return response
            
        except httpx.TimeoutException:
            _LOGGER.error("Request timeout for %s %s", method, url)
            return None
        except httpx.RequestError as e:
            _LOGGER.error("Request error for %s %s: %s", method, url, e)
            return None
        except Exception as e:
            _LOGGER.error("Unexpected error for %s %s: %s", method, url, e)
            return None

    async def _login(self) -> bool:
        """Login to the Bluestar API."""
        async with self._lock:
            if self._session_token and time.time() < self._token_expiry:
                return True

            _LOGGER.info("Logging in to Bluestar API")
            
            payload = {
                "auth_id": self.email,
                "auth_type": 1,  # 1 for email, 0 for phone
                "password": self.password
            }
            
            response = await self._make_request("POST", LOGIN_URL, json=payload)
            if not response:
                return False
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "data" in data and "session_token" in data["data"]:
                        self._session_token = data["data"]["session_token"]
                        # Set token expiry to 1 hour from now
                        self._token_expiry = time.time() + 3600
                        _LOGGER.info("Login successful")
                        return True
                    else:
                        _LOGGER.error("No session token in login response")
                        return False
                except Exception as e:
                    _LOGGER.error("Failed to parse login response: %s", e)
                    return False
            else:
                _LOGGER.error(
                    "Login failed with status %d: %s",
                    response.status_code,
                    response.text
                )
                return False

    async def ensure_authenticated(self) -> bool:
        """Ensure we have a valid session token."""
        return await self._login()

    async def get_devices(self) -> List[Dict[str, Any]]:
        """Get list of user's devices."""
        if not await self.ensure_authenticated():
            return []
        
        headers = await self._get_auth_headers()
        response = await self._make_request("GET", DEVICES_URL, headers=headers)
        
        if not response or response.status_code != 200:
            return []
        
        try:
            data = response.json()
            devices = data.get("data", [])
            _LOGGER.info("Found %d devices", len(devices))
            return devices
        except Exception as e:
            _LOGGER.error("Failed to parse devices response: %s", e)
            return []

    async def get_device_status(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific device."""
        if not await self.ensure_authenticated():
            return None
        
        url = DEVICE_STATE_URL.format(device_id=device_id)
        headers = await self._get_auth_headers()
        response = await self._make_request("GET", url, headers=headers)
        
        if not response or response.status_code != 200:
            return None
        
        try:
            data = response.json()
            return data.get("data", {})
        except Exception as e:
            _LOGGER.error("Failed to parse device status response: %s", e)
            return None

    async def set_device_state(
        self, device_id: str, **kwargs
    ) -> bool:
        """Set device state."""
        if not await self.ensure_authenticated():
            return False
        
        url = DEVICE_STATE_URL.format(device_id=device_id)
        headers = await self._get_auth_headers()
        
        # Build payload from kwargs
        payload = {}
        if "power" in kwargs:
            payload["power"] = kwargs["power"]
        if "mode" in kwargs:
            payload["mode"] = kwargs["mode"]
        if "temp" in kwargs:
            payload["temp"] = int(kwargs["temp"])
        if "fan_speed" in kwargs:
            payload["fan_speed"] = kwargs["fan_speed"]
        
        if not payload:
            _LOGGER.warning("No valid state parameters provided")
            return False
        
        _LOGGER.info("Setting device %s state: %s", device_id, payload)
        
        response = await self._make_request(
            "POST", url, json=payload, headers=headers
        )
        
        if not response:
            return False
        
        success = response.status_code == 200
        if success:
            _LOGGER.info("Device state updated successfully")
        else:
            _LOGGER.error(
                "Failed to update device state: %d - %s",
                response.status_code,
                response.text
            )
        
        return success

    async def get_device_info(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed device information."""
        if not await self.ensure_authenticated():
            return None
        
        url = DEVICE_INFO_URL.format(device_id=device_id)
        params = {"is_tuya_device": "true"}
        headers = await self._get_auth_headers()
        
        response = await self._make_request(
            "GET", url, params=params, headers=headers
        )
        
        if not response or response.status_code != 200:
            return None
        
        try:
            data = response.json()
            return data.get("data", {})
        except Exception as e:
            _LOGGER.error("Failed to parse device info response: %s", e)
            return None

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

