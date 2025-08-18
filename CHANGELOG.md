# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial development and testing

## [1.0.0] - 2025-08-19

### Added
- **Initial Release** 🎉
- Full Bluestar AC control integration
- Climate entity with power, temperature, mode, fan speed, swing, and preset controls
- Dedicated fan entity with speed control
- Switch entities for display and buzzer control
- AWS IoT MQTT communication (same as official app)
- Easy configuration flow with connection testing
- Full Home Assistant integration
- HACS compatibility
- Comprehensive documentation

### Features
- **Climate Control**: Power ON/OFF, temperature (16°C-30°C), modes (Auto/Cool/Dry/Fan)
- **Fan Control**: Speed control (Auto/Low/Medium/High) with percentage
- **Swing Control**: Horizontal, vertical, both, or off
- **Special Modes**: Eco, Turbo, Sleep modes
- **Additional Controls**: Display and buzzer switches
- **Real-time Control**: Direct AWS IoT communication
- **Error Handling**: Robust error handling and reconnection

### Technical
- AWS IoT Core MQTT integration
- AWS SigV4 authentication
- Shadow update communication
- Proper Home Assistant entity structure
- Async/await support
- Comprehensive logging

---

## Version History

- **v1.0.0**: Initial release with full AC control capabilities
