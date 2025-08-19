"""Fan platform for Bluestar AC."""
import logging
from typing import Any, List, Optional

from homeassistant.components.fan import (
    FanEntity,
    FanEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, CONF_DEVICE_ID, FAN_MODES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bluestar AC fan platform."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    device_id = config_entry.data[CONF_DEVICE_ID]
    
    async_add_entities([BluestarACFan(client, device_id)], True)

class BluestarACFan(FanEntity):
    """Representation of a Bluestar AC fan."""
    
    def __init__(self, client, device_id: str):
        """Initialize the fan entity."""
        self._client = client
        self._device_id = device_id
        self._attr_unique_id = f"bluestar_ac_fan_{device_id}"
        self._attr_name = f"Bluestar AC Fan {device_id}"
        self._attr_has_entity_name = True
        
        # Set supported features
        self._attr_supported_features = FanEntityFeature.SET_SPEED
        
        # Set available speeds
        self._attr_speed_count = len(FAN_MODES)
        self._attr_percentage = 0
        self._attr_speed = "auto"
        
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._client._connected
    
    @property
    def is_on(self) -> bool:
        """Return true if the entity is on."""
        # The fan is on if the AC is on and not in auto mode
        return self._attr_speed != "auto"
    
    async def async_turn_on(self, speed: Optional[str] = None, percentage: Optional[int] = None, preset_mode: Optional[str] = None, **kwargs: Any) -> None:
        """Turn the fan on."""
        if speed:
            await self.async_set_speed(speed)
        elif percentage:
            await self.async_set_percentage(percentage)
        else:
            # Default to medium speed
            await self.async_set_speed("medium")
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the fan off (set to auto)."""
        await self.async_set_speed("auto")
    
    async def async_set_speed(self, speed: str) -> None:
        """Set the speed of the fan."""
        if speed not in FAN_MODES:
            _LOGGER.error("Invalid fan speed: %s", speed)
            return
            
        success = await self.hass.async_add_executor_job(
            self._client.set_fan_mode, speed
        )
        if success:
            self._attr_speed = speed
            # Calculate percentage based on speed
            if speed == "auto":
                self._attr_percentage = 0
            elif speed == "low":
                self._attr_percentage = 33
            elif speed == "medium":
                self._attr_percentage = 66
            elif speed == "high":
                self._attr_percentage = 100
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set fan speed to %s", speed)
    
    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        if percentage == 0:
            await self.async_set_speed("auto")
        elif percentage <= 33:
            await self.async_set_speed("low")
        elif percentage <= 66:
            await self.async_set_speed("medium")
        else:
            await self.async_set_speed("high")
    
    async def async_update(self) -> None:
        """Update the entity state."""
        # For now, we'll just update the connection status
        # In the future, we could implement state polling from the AC
        if not self._client._connected:
            await self.hass.async_add_executor_job(self._client.test_connection)
