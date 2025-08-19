"""Switch platform for Bluestar AC."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, CONF_DEVICE_ID

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bluestar AC switch platform."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    device_id = config_entry.data[CONF_DEVICE_ID]
    
    # Create switches for additional controls
    switches = [
        BluestarACDisplaySwitch(client, device_id),
        BluestarACBuzzerSwitch(client, device_id),
    ]
    
    async_add_entities(switches, True)

class BluestarACDisplaySwitch(SwitchEntity):
    """Representation of a Bluestar AC display switch."""
    
    def __init__(self, client, device_id: str):
        """Initialize the display switch."""
        self._client = client
        self._device_id = device_id
        self._attr_unique_id = f"bluestar_ac_display_{device_id}"
        self._attr_name = f"Bluestar AC Display {device_id}"
        self._attr_has_entity_name = True
        self._attr_is_on = False
        
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._client._connected
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the display on."""
        success = await self.hass.async_add_executor_job(
            self._client.set_display, True
        )
        if success:
            self._attr_is_on = True
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to turn on display")
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the display off."""
        success = await self.hass.async_add_executor_job(
            self._client.set_display, False
        )
        if success:
            self._attr_is_on = False
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to turn off display")
    
    async def async_update(self) -> None:
        """Update the entity state."""
        # For now, we'll just update the connection status
        # In the future, we could implement state polling from the AC
        if not self._client._connected:
            await self.hass.async_add_executor_job(self._client.test_connection)

class BluestarACBuzzerSwitch(SwitchEntity):
    """Representation of a Bluestar AC buzzer switch."""
    
    def __init__(self, client, device_id: str):
        """Initialize the buzzer switch."""
        self._client = client
        self._device_id = device_id
        self._attr_unique_id = f"bluestar_ac_buzzer_{device_id}"
        self._attr_name = f"Bluestar AC Buzzer {device_id}"
        self._attr_has_entity_name = True
        self._attr_is_on = False
        
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._client._connected
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the buzzer on."""
        success = await self.hass.async_add_executor_job(
            self._client.set_buzzer, True
        )
        if success:
            self._attr_is_on = True
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to turn on buzzer")
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the buzzer off."""
        success = await self.hass.async_add_executor_job(
            self._client.set_buzzer, False
        )
        if success:
            self._attr_is_on = False
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to turn off buzzer")
    
    async def async_update(self) -> None:
        """Update the entity state."""
        # For now, we'll just update the connection status
        # In the future, we could implement state polling from the AC
        if not self._client._connected:
            await self.hass.async_add_executor_job(self._client.test_connection)
