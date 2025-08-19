# ❄️ Bluestar AC - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![maintainer](https://img.shields.io/badge/maintainer-%40sankarhansdah-blue.svg)](https://github.com/sankarhansdah)
[![version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/sankarhansdah/Bluestar-Smart-AC)

A **Home Assistant integration** for controlling Bluestar Smart AC units. This integration provides full control over your AC including temperature, mode, fan speed, swing, and special modes using the **exact same communication method** as the official Bluestar app.

## 🚀 Features

- **🌡️ Full AC Control**: Power, temperature, mode, fan speed, swing
- **💨 Dedicated Fan Entity**: Speed control with percentage
- **🔌 Switch Controls**: Display and buzzer controls
- **🎛️ All AC Modes**: Auto, Cool, Dry, Fan modes
- **🌿 Special Modes**: Eco, Turbo, Sleep modes
- **🔄 Swing Control**: Horizontal and vertical swing
- **⚡ Real-time Control**: Direct AWS IoT MQTT communication
- **🏠 Native Home Assistant**: Full integration with HA ecosystem

## 📱 Screenshots

*[Add screenshots of your integration in Home Assistant here]*

## 🏗️ Installation

### HACS Installation (Recommended)

1. **Install HACS** if you haven't already: [HACS Installation Guide](https://hacs.xyz/docs/installation/installation/)
2. **Add this repository** to HACS:
   - Go to HACS → Integrations
   - Click the 3 dots menu → Custom repositories
   - Add repository: `sankarhansdah/Bluestar-Smart-AC`
   - Category: Integration
3. **Install the integration**:
   - Search for "Bluestar AC" in HACS
   - Click "Download"
   - Restart Home Assistant
4. **Add the integration**:
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Bluestar AC"
   - Follow the setup wizard

### Manual Installation

1. **Download** the latest release
2. **Copy** `custom_components/bluestar_ac/` to your Home Assistant `config/custom_components/` directory
3. **Restart** Home Assistant
4. **Add integration** via the UI

## ⚙️ Configuration

### Required Information

- **Username/Phone Number**: Your Bluestar account credentials
- **Password**: Your Bluestar account password
- **Device ID**: Your AC's device ID (e.g., `24587ca091f8`)
- **Authentication Type**: Usually `bluestar` (default)

### Setup Steps

1. **Get Your Device ID**:
   - Check your Bluestar app for device information
   - Or use the device ID from your working setup

2. **Configure the Integration**:
   - Enter your credentials
   - Enter your device ID
   - Test the connection
   - Save the configuration

## 🎯 Usage

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

## 🔧 Troubleshooting

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

## 🌟 Advanced Features

### Automation Examples

```yaml
# Turn AC on when temperature is high
automation:
  - alias: "AC Auto On - High Temp"
    trigger:
      platform: numeric_state
      entity_id: sensor.living_room_temperature
      above: 28
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.bluestar_ac_24587ca091f8
        data:
          hvac_mode: cool
      - service: climate.set_temperature
        target:
          entity_id: climate.bluestar_ac_24587ca091f8
        data:
          temperature: 24

# Turn AC off when leaving home
automation:
  - alias: "AC Auto Off - Away"
    trigger:
      platform: state
      entity_id: person.your_name
      to: "not_home"
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.bluestar_ac_24587ca091f8
        data:
          hvac_mode: off
```

### Dashboard Integration

- **Lovelace cards** for AC control
- **Custom buttons** for quick actions
- **Temperature graphs** and history
- **Status indicators** for all features

## 🔬 Technical Details

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. **Fork** this repository
2. **Clone** your fork
3. **Make changes** and test them
4. **Submit** a pull request

### Testing

1. **Install** the integration in your Home Assistant
2. **Test** all features thoroughly
3. **Report** any issues with detailed information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Bluestar India** for their Smart AC platform
- **Home Assistant community** for the integration framework
- **HACS** for making custom integrations easy to install
- **Reverse engineering** of the official mobile app for protocol details

## 📞 Support

- **GitHub Issues**: [Create an issue](https://github.com/sankarhansdah/Bluestar-Smart-AC/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sankarhansdah/Bluestar-Smart-AC/discussions)
- **Documentation**: Check the [Wiki](https://github.com/sankarhansdah/Bluestar-Smart-AC/wiki) for detailed guides

## ⭐ Star This Repository

If you find this integration useful, please give it a ⭐ star on GitHub!

---

**Made with ❤️ for the Home Assistant community**

*This integration transforms your Bluestar AC into a smart home superstar!* 🌟❄️🏠

