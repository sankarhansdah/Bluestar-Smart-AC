"""Bluestar AC client for Home Assistant."""
import asyncio
import logging
import time
from typing import Any, Dict, Optional

from .const import (
    MIN_TEMP,
    MAX_TEMP,
    FAN_MODES,
    SWING_MODES,
    PRESET_MODES,
    HVAC_MODES,
    DEFAULT_TEMPERATURE,
    DEFAULT_FAN_MODE,
    DEFAULT_SWING_MODE,
    DEFAULT_PRESET_MODE,
)

_LOGGER = logging.getLogger(__name__)

class BluestarACClient:
    """Client for Bluestar AC control."""
    
    def __init__(self, username: str, password: str, device_id: str, auth_type: str = "bluestar"):
        """Initialize the client."""
        self.username = username
        self.password = password
        self.device_id = device_id
        self.auth_type = auth_type
        self._aws_client = None
        self._connected = False
        
    def test_connection(self) -> bool:
        """Test the connection to the AC."""
        try:
            # Import here to avoid circular imports
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from working_aws_iot_client import BluestarAWSIoTClient
            
            client = BluestarAWSIoTClient()
            
            # Test login
            if not client.login_and_get_credentials():
                _LOGGER.error("Failed to login to Bluestar")
                return False
                
            # Test AWS IoT connection
            if not client.create_aws_iot_client():
                _LOGGER.error("Failed to create AWS IoT client")
                return False
                
            self._aws_client = client
            self._connected = True
            _LOGGER.info("Successfully connected to Bluestar AC")
            return True
            
        except Exception as e:
            _LOGGER.error("Connection test failed: %s", e)
            return False
    
    def _ensure_connected(self) -> bool:
        """Ensure we have a valid connection."""
        if not self._connected or not self._aws_client:
            return self.test_connection()
        return True
    
    def _send_command(self, payload: Dict[str, Any]) -> bool:
        """Send a command via AWS IoT."""
        if not self._ensure_connected():
            return False
            
        try:
            # Add timestamp and source
            payload["ts"] = int(time.time() * 1000)
            payload["src"] = "anmq"
            
            # Send via shadow update
            success = self._aws_client.send_shadow_update(payload)
            if success:
                _LOGGER.debug("Command sent successfully: %s", payload)
            else:
                _LOGGER.error("Failed to send command: %s", payload)
            return success
            
        except Exception as e:
            _LOGGER.error("Error sending command: %s", e)
            return False
    
    def set_power(self, power: bool) -> bool:
        """Set power state."""
        payload = {"pow": 1 if power else 0}
        return self._send_command(payload)
    
    def set_temperature(self, temperature: float) -> bool:
        """Set target temperature."""
        if not MIN_TEMP <= temperature <= MAX_TEMP:
            _LOGGER.error("Temperature %s out of range [%s, %s]", temperature, MIN_TEMP, MAX_TEMP)
            return False
            
        payload = {"stemp": f"{temperature:.1f}"}
        return self._send_command(payload)
    
    def set_mode(self, mode: str) -> bool:
        """Set HVAC mode."""
        mode_mapping = {
            "auto": 0,
            "cool": 1,
            "dry": 2,
            "fan": 3
        }
        
        if mode not in mode_mapping:
            _LOGGER.error("Invalid mode: %s", mode)
            return False
            
        payload = {"climate": mode_mapping[mode]}
        return self._send_command(payload)
    
    def set_fan_mode(self, fan_mode: str) -> bool:
        """Set fan mode."""
        fan_mapping = {
            "auto": 0,
            "low": 1,
            "medium": 2,
            "high": 3
        }
        
        if fan_mode not in fan_mapping:
            _LOGGER.error("Invalid fan mode: %s", fan_mode)
            return False
            
        payload = {"fspd": fan_mapping[fan_mode]}
        return self._send_command(payload)
    
    def set_swing_mode(self, swing_mode: str) -> bool:
        """Set swing mode."""
        if swing_mode == "off":
            payload = {"hswing": 0, "vswing": 0}
        elif swing_mode == "horizontal":
            payload = {"hswing": 1, "vswing": 0}
        elif swing_mode == "vertical":
            payload = {"hswing": 0, "vswing": 1}
        elif swing_mode == "both":
            payload = {"hswing": 1, "vswing": 1}
        else:
            _LOGGER.error("Invalid swing mode: %s", swing_mode)
            return False
            
        return self._send_command(payload)
    
    def set_preset_mode(self, preset_mode: str) -> bool:
        """Set preset mode."""
        if preset_mode == "none":
            # Turn off all special modes
            payload = {"eco": 0, "turbo": 0, "sleep": 0}
        elif preset_mode == "eco":
            payload = {"eco": 1, "turbo": 0, "sleep": 0}
        elif preset_mode == "turbo":
            payload = {"eco": 0, "turbo": 1, "sleep": 0}
        elif preset_mode == "sleep":
            payload = {"eco": 0, "turbo": 0, "sleep": 1}
        else:
            _LOGGER.error("Invalid preset mode: %s", preset_mode)
            return False
            
        return self._send_command(payload)
    
    def set_display(self, display: bool) -> bool:
        """Set display state."""
        payload = {"display": 1 if display else 0}
        return self._send_command(payload)
    
    def set_buzzer(self, buzzer: bool) -> bool:
        """Set buzzer state."""
        payload = {"buzzer": 1 if buzzer else 0}
        return self._send_command(payload)
    
    def close(self):
        """Close the client."""
        self._connected = False
        self._aws_client = None
