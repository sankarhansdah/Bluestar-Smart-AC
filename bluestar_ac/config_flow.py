"""Config flow for Bluestar AC integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    CONF_AUTH_TYPE,
    DEFAULT_AUTH_TYPE,
)
from .bluestar_client import BluestarACClient

_LOGGER = logging.getLogger(__name__)

class BluestarACConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bluestar AC."""
    
    VERSION = 1
    
    def __init__(self):
        """Initialize the config flow."""
        self._errors = {}
    
    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        self._errors = {}
        
        if user_input is not None:
            try:
                # Test the connection
                client = BluestarACClient(
                    user_input["username"],
                    user_input["password"],
                    user_input["device_id"],
                    user_input.get("auth_type", DEFAULT_AUTH_TYPE)
                )
                
                # Test connection
                success = await self.hass.async_add_executor_job(client.test_connection)
                
                if success:
                    # Create unique ID
                    unique_id = f"bluestar_ac_{user_input['device_id']}"
                    
                    # Check if already configured
                    await self.async_set_unique_id(unique_id)
                    self._abort_if_unique_id_configured()
                    
                    # Create config entry
                    return self.async_create_entry(
                        title=f"Bluestar AC {user_input['device_id']}",
                        data=user_input
                    )
                else:
                    self._errors["base"] = "connection_failed"
                    
            except Exception as ex:
                _LOGGER.error("Config flow error: %s", ex)
                self._errors["base"] = "unknown"
        
        # Show the form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Required("device_id"): str,
                vol.Optional("auth_type", default=DEFAULT_AUTH_TYPE): str,
            }),
            errors=self._errors,
        )
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return BluestarACOptionsFlow(config_entry)

class BluestarACOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""
    
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
    
    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "auth_type",
                    default=self.config_entry.data.get("auth_type", DEFAULT_AUTH_TYPE)
                ): str,
            })
        )

class ConnectionFailed(HomeAssistantError):
    """Error to indicate we cannot connect."""

