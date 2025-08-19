"""Constants for the Bluestar AC integration."""
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_PASSWORD,
    CONF_USERNAME,
)

DOMAIN = "bluestar_ac"

# Configuration keys
CONF_AUTH_ID = "auth_id"
CONF_AUTH_TYPE = "auth_type"
DEFAULT_AUTH_TYPE = "bluestar"

# Device info
MANUFACTURER = "Bluestar"
MODEL = "Smart AC"

# Supported features
SUPPORT_TARGET_TEMPERATURE = 1
SUPPORT_FAN_MODE = 2
SUPPORT_SWING_MODE = 4
SUPPORT_PRESET_MODE = 8

# Temperature range
MIN_TEMP = 16
MAX_TEMP = 30

# Fan modes
FAN_MODES = ["auto", "low", "medium", "high"]

# Swing modes
SWING_MODES = ["off", "horizontal", "vertical", "both"]

# Preset modes
PRESET_MODES = ["none", "eco", "turbo", "sleep"]

# HVAC modes
HVAC_MODES = ["off", "auto", "cool", "dry", "fan"]

# Default values
DEFAULT_TEMPERATURE = 24
DEFAULT_FAN_MODE = "auto"
DEFAULT_SWING_MODE = "off"
DEFAULT_PRESET_MODE = "none"

