# Bluestar AC Home Assistant Integration

This is a custom Home Assistant integration for controlling Bluestar Smart AC units. It provides full control over your AC including temperature, mode, fan speed, swing, and special modes.

## Features

- **Climate Control**: Full AC control with temperature, mode, and fan speed
- **Fan Control**: Dedicated fan entity with speed control
- **Switch Controls**: Display and buzzer controls
- **All AC Modes**: Auto, Cool, Dry, Fan modes
- **Special Modes**: Eco, Turbo, Sleep modes
- **Swing Control**: Horizontal and vertical swing control
- **Real-time Control**: Direct AWS IoT MQTT communication

## Installation

### Method 1: Manual Installation (Recommended)

1. **Copy the integration folder** to your Home Assistant `config/custom_components/` directory:
   ```bash
   cp -r custom_components/bluestar_ac /path/to/homeassistant/config/custom_components/
   ```

2. **Restart Home Assistant**

3. **Add Integration**:
   - Go to **Settings** → **Devices & Services**
   - Click **+ Add Integration**
   - Search for **"Bluestar AC"**
   - Click on it and follow the setup wizard

### Method 2: HACS Installation

1. **Add this repository** to HACS as a custom repository
2. **Install the integration** through HACS
3. **Restart Home Assistant**
4. **Add the integration** through the UI

## Configuration

### Required Information

- **Username/Phone Number**: Your Bluestar account username or phone number
- **Password**: Your Bluestar account password
- **Device ID**: Your AC's device ID (e.g., `24587ca091f8`)
- **Authentication Type**: Usually `bluestar` (default)

### Setup Steps

1. **Get Your Device ID**:
   - Use the device ID from your working web interface
   - Or check the Bluestar app for device information

2. **Configure the Integration**:
   - Enter your credentials
   - Enter your device ID
   - Test the connection
   - Save the configuration

## Usage

### Climate Entity

The main climate entity provides:
- **Power Control**: Turn AC on/off
- **Temperature Control**: Set target temperature (16°C - 30°C)
- **Mode Control**: Auto, Cool, Dry, Fan modes
- **Fan Speed**: Auto, Low, Medium, High
- **Swing Control**: Horizontal, Vertical, Both, Off
- **Preset Modes**: Eco, Turbo, Sleep, None

### Fan Entity

Dedicated fan control with:
- **Speed Control**: Auto, Low, Medium, High
- **Percentage Control**: 0% (Auto) to 100% (High)

### Switch Entities

Additional controls:
- **Display Switch**: Turn AC display on/off
- **Buzzer Switch**: Turn AC buzzer on/off

## Troubleshooting

### Connection Issues

1. **Check Credentials**: Verify username/password are correct
2. **Verify Device ID**: Ensure device ID matches your AC
3. **Network Access**: Ensure Home Assistant can access the internet
4. **Check Logs**: Look for error messages in Home Assistant logs

### Control Issues

1. **Verify AC is Online**: Ensure AC is connected to WiFi
2. **Check Integration Status**: Verify integration shows as "Connected"
3. **Restart Integration**: Try removing and re-adding the integration

### Common Error Messages

- **"connection_failed"**: Check credentials and device ID
- **"already_configured"**: Device is already set up
- **"unknown"**: Unexpected error, check logs

## Technical Details

### Communication Method

This integration uses the **exact same AWS IoT MQTT communication** as the official Bluestar app:
- **Protocol**: AWS IoT Core MQTT
- **Authentication**: AWS SigV4 with Bluestar credentials
- **Payload Format**: JSON with timestamp and source identification
- **Topics**: AWS IoT Shadow updates

### Supported Commands

- **Power**: `{"pow": 1, "ts": <timestamp>, "src": "anmq"}`
- **Temperature**: `{"stemp": "24.0", "ts": <timestamp>, "src": "anmq"}`
- **Mode**: `{"climate": 1, "ts": <timestamp>, "src": "anmq"}`
- **Fan Speed**: `{"fspd": 2, "ts": <timestamp>, "src": "anmq"}`
- **Swing**: `{"hswing": 1, "vswing": 1, "ts": <timestamp>, "src": "anmq"}`
- **Special Modes**: `{"eco": 1, "turbo": 0, "sleep": 0, "ts": <timestamp>, "src": "anmq"}`

## Development

### Requirements

- Home Assistant 2023.8.0 or later
- Python 3.10 or later
- Access to Bluestar AWS IoT endpoints

### Local Development

1. **Clone the repository**
2. **Copy to custom_components**
3. **Restart Home Assistant**
4. **Test changes**

## Support

For issues and questions:
1. **Check the logs** for error messages
2. **Verify configuration** is correct
3. **Test basic connectivity** first
4. **Create an issue** with detailed information

## License

This integration is provided as-is for personal use. It integrates with Bluestar's official services and follows their communication protocols.

## Acknowledgments

- **Bluestar India** for their Smart AC platform
- **Home Assistant community** for the integration framework
- **Reverse engineering** of the official mobile app for protocol details
