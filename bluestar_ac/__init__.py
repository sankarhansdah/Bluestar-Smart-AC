"""The Bluestar AC integration."""
import asyncio
import logging
from typing import Any, Dict

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_PASSWORD,
    CONF_USERNAME,
    Platform,
)

from .const import (
    DOMAIN,
    CONF_AUTH_ID,
    CONF_AUTH_TYPE,
    DEFAULT_AUTH_TYPE,
)
from .bluestar_client import BluestarACClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.SWITCH, Platform.FAN]

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_DEVICE_ID): str,
        vol.Optional(CONF_AUTH_TYPE, default=DEFAULT_AUTH_TYPE): str,
    })
})

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bluestar AC from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    config = entry.data
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]
    device_id = config[CONF_DEVICE_ID]
    auth_type = config.get(CONF_AUTH_TYPE, DEFAULT_AUTH_TYPE)
    
    # Create client
    client = BluestarACClient(username, password, device_id, auth_type)
    
    try:
        # Test connection
        await hass.async_add_executor_job(client.test_connection)
    except Exception as ex:
        _LOGGER.error("Failed to connect to Bluestar AC: %s", ex)
        raise ConfigEntryNotReady from ex
    
    # Store client in hass data
    hass.data[DOMAIN][entry.entry_id] = client
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

