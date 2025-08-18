"""Climate platform for Bluestar AC."""
import logging
from typing import Any, List, Optional

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    FanMode,
    SwingMode,
    PresetMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_DEVICE_ID,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    DOMAIN,
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

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bluestar AC climate platform."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    device_id = config_entry.data[CONF_DEVICE_ID]
    
    async_add_entities([BluestarACClimate(client, device_id)], True)

class BluestarACClimate(ClimateEntity):
    """Representation of a Bluestar AC climate entity."""
    
    def __init__(self, client, device_id: str):
        """Initialize the climate entity."""
        self._client = client
        self._device_id = device_id
        self._attr_unique_id = f"bluestar_ac_{device_id}"
        self._attr_name = f"Bluestar AC {device_id}"
        self._attr_has_entity_name = True
        
        # Set supported features
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE |
            ClimateEntityFeature.FAN_MODE |
            ClimateEntityFeature.SWING_MODE |
            ClimateEntityFeature.PRESET_MODE
        )
        
        # Set temperature unit
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_min_temp = MIN_TEMP
        self._attr_max_temp = MAX_TEMP
        self._attr_target_temperature = DEFAULT_TEMPERATURE
        
        # Set available modes
        self._attr_hvac_modes = [HVACMode(mode) for mode in HVAC_MODES]
        self._attr_fan_modes = FAN_MODES
        self._attr_swing_modes = SWING_MODES
        self._attr_preset_modes = PRESET_MODES
        
        # Initialize state
        self._attr_hvac_mode = HVACMode.COOL
        self._attr_fan_mode = DEFAULT_FAN_MODE
        self._attr_swing_mode = DEFAULT_SWING_MODE
        self._attr_preset_mode = DEFAULT_PRESET_MODE
        self._attr_current_temperature = DEFAULT_TEMPERATURE
        
        # Power state
        self._attr_hvac_mode = HVACMode.OFF
        
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._client._connected
    
    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if ATTR_TEMPERATURE in kwargs:
            temperature = kwargs[ATTR_TEMPERATURE]
            success = await self.hass.async_add_executor_job(
                self._client.set_temperature, temperature
            )
            if success:
                self._attr_target_temperature = temperature
                self.async_write_ha_state()
            else:
                _LOGGER.error("Failed to set temperature to %s", temperature)
    
    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        if hvac_mode == HVACMode.OFF:
            success = await self.hass.async_add_executor_job(
                self._client.set_power, False
            )
            if success:
                self._attr_hvac_mode = hvac_mode
                self.async_write_ha_state()
        else:
            # First turn on power
            power_success = await self.hass.async_add_executor_job(
                self._client.set_power, True
            )
            if power_success:
                # Then set mode
                mode_success = await self.hass.async_add_executor_job(
                    self._client.set_mode, hvac_mode.value
                )
                if mode_success:
                    self._attr_hvac_mode = hvac_mode
                    self.async_write_ha_state()
                else:
                    _LOGGER.error("Failed to set HVAC mode to %s", hvac_mode)
            else:
                _LOGGER.error("Failed to turn on power")
    
    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        success = await self.hass.async_add_executor_job(
            self._client.set_fan_mode, fan_mode
        )
        if success:
            self._attr_fan_mode = fan_mode
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set fan mode to %s", fan_mode)
    
    async def async_set_swing_mode(self, swing_mode: str) -> None:
        """Set new target swing mode."""
        success = await self.hass.async_add_executor_job(
            self._client.set_swing_mode, swing_mode
        )
        if success:
            self._attr_swing_mode = swing_mode
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set swing mode to %s", swing_mode)
    
    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        success = await self.hass.async_add_executor_job(
            self._client.set_preset_mode, preset_mode
        )
        if success:
            self._attr_preset_mode = preset_mode
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set preset mode to %s", preset_mode)
    
    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        success = await self.hass.async_add_executor_job(
            self._client.set_power, True
        )
        if success:
            self._attr_hvac_mode = HVACMode.COOL
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to turn on AC")
    
    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        success = await self.hass.async_add_executor_job(
            self._client.set_power, False
        )
        if success:
            self._attr_hvac_mode = HVACMode.OFF
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to turn off AC")
    
    async def async_update(self) -> None:
        """Update the entity state."""
        # For now, we'll just update the connection status
        # In the future, we could implement state polling from the AC
        if not self._client._connected:
            await self.hass.async_add_executor_job(self._client.test_connection)
