# 🏠 HACS Installation Guide for Bluestar AC

This guide will walk you through installing the Bluestar AC integration via HACS (Home Assistant Community Store).

## 📋 Prerequisites

- **Home Assistant** installed and running
- **HACS** installed in your Home Assistant instance
- **Bluestar AC account** with credentials
- **Device ID** of your AC unit

## 🚀 Step-by-Step Installation

### 1. Install HACS (if not already installed)

If you don't have HACS installed yet, follow the [official HACS installation guide](https://hacs.xyz/docs/installation/installation/).

### 2. Add Custom Repository

1. **Open HACS** in your Home Assistant sidebar
2. **Go to Integrations** section
3. **Click the 3 dots menu** (⋮) in the top right
4. **Select "Custom repositories"**
5. **Click "Add"**
6. **Fill in the details**:
   - **Repository**: `sankarhansdah/Bluestar-Smart-AC`
   - **Category**: `Integration`
   - **Click "Add"**

### 3. Install the Integration

1. **Search for "Bluestar AC"** in the HACS Integrations section
2. **Click on "Bluestar AC"** when it appears
3. **Click "Download"**
4. **Restart Home Assistant** when prompted

### 4. Configure the Integration

1. **Go to Settings** → **Devices & Services**
2. **Click "+ Add Integration"**
3. **Search for "Bluestar AC"**
4. **Click on "Bluestar AC"**
5. **Fill in your credentials**:
   - **Username/Phone Number**: Your Bluestar account
   - **Password**: Your Bluestar account password
   - **Device ID**: Your AC's device ID (e.g., `24587ca091f8`)
   - **Authentication Type**: `bluestar` (default)
6. **Click "Submit"**
7. **Test the connection** when prompted
8. **Click "Finish"**

## 🔧 Configuration Details

### Required Information

| Field | Description | Example |
|-------|-------------|---------|
| **Username/Phone** | Your Bluestar account login | `your@email.com` or `+919876543210` |
| **Password** | Your Bluestar account password | `yourpassword` |
| **Device ID** | Your AC's unique identifier | `24587ca091f8` |
| **Auth Type** | Authentication method | `bluestar` (default) |

### Finding Your Device ID

1. **Check your Bluestar app**:
   - Open the Bluestar Smart AC app
   - Go to device settings
   - Look for device information or ID

2. **Check your working setup**:
   - If you have the web interface working, use the same device ID
   - Check the URL or configuration files

3. **Contact Bluestar support** if you can't find it

## ✅ Verification

After installation, you should see:

### New Entities
- **Climate Entity**: `climate.bluestar_ac_[device_id]`
- **Fan Entity**: `fan.bluestar_ac_fan_[device_id]`
- **Switch Entities**: 
  - `switch.bluestar_ac_display_[device_id]`
  - `switch.bluestar_ac_buzzer_[device_id]`

### Integration Status
- **Status**: "Connected" or "Connected (1 device)"
- **No errors** in the integration details

## 🧪 Testing

### Basic Functionality
1. **Power Control**: Turn AC on/off
2. **Temperature**: Set target temperature
3. **Mode**: Change between Auto/Cool/Dry/Fan
4. **Fan Speed**: Adjust fan speed

### Advanced Features
1. **Swing Control**: Test horizontal/vertical swing
2. **Special Modes**: Try Eco, Turbo, Sleep modes
3. **Additional Controls**: Test display and buzzer switches

## 🔍 Troubleshooting

### Common Issues

#### Integration Not Found
- **Solution**: Ensure you've restarted Home Assistant after installation
- **Check**: Verify the integration files are in `config/custom_components/bluestar_ac/`

#### Connection Failed
- **Check**: Verify your credentials and device ID
- **Test**: Try logging into the Bluestar app first
- **Verify**: Ensure your AC is online and connected to WiFi

#### Controls Not Working
- **Check**: Integration status shows "Connected"
- **Verify**: AC is responding to the official app
- **Restart**: Try restarting the integration

### Debug Steps

1. **Enable Debug Logging**:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.bluestar_ac: debug
   ```

2. **Check Home Assistant Logs**:
   - Go to Developer Tools → Logs
   - Look for errors related to "bluestar_ac"

3. **Verify Integration Files**:
   - Check `config/custom_components/bluestar_ac/` exists
   - Ensure all files are present and readable

## 📱 Mobile App Integration

Once installed, you can control your AC from:
- **Home Assistant Mobile App**
- **Voice assistants** (Google Assistant, Alexa)
- **Automations** and scripts
- **Custom dashboards**

## 🔄 Updates

### Automatic Updates
- HACS will notify you of new versions
- Click "Update" in HACS to get the latest version
- Restart Home Assistant after updates

### Manual Updates
- Download the latest release from GitHub
- Replace the files in `config/custom_components/bluestar_ac/`
- Restart Home Assistant

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Review the logs** for error messages
3. **Check GitHub Issues** for known problems
4. **Create a new issue** with detailed information:
   - Home Assistant version
   - HACS version
   - Error messages
   - Steps to reproduce

## 🎉 Success!

Once everything is working, you'll have:
- **Full AC control** from Home Assistant
- **Smart automations** for your AC
- **Voice control** capabilities
- **Mobile app control**
- **Professional integration** with your smart home

---

**Happy Home Automating! 🏠✨**

*Your Bluestar AC is now a smart home superstar!* 🌟❄️
