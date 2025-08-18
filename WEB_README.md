# 🌐 Bluestar Smart AC Web Interface

A beautiful, feature-rich web application to test all Bluestar Smart AC API features discovered in the reverse engineering analysis.

## ✨ Features

### 🔐 Authentication
- **Unified Login Field**: Single "Mobile no./Email" field that accepts both email and phone numbers
- **Smart Authentication**: Automatically tries email login first, then phone login if needed
- **Simple Flow**: Just enter your credentials and click Sign In - no OTP needed for login
- **Session Management**: Automatic token handling and refresh
- **Secure Logout**: Proper session cleanup

### 🏠 Device Management
- **Device Discovery**: Automatically lists all your AC units
- **Real-time Status**: Get current device state and settings
- **Device Information**: View detailed device metadata

### ❄️ Full AC Control
- **Power Control**: Turn AC units on/off
- **Temperature Control**: Set target temperature (16°C - 30°C)
- **Mode Selection**: 
  - Cool 🧊
  - Heat 🔥
  - Auto 🤖
  - Fan 💨
  - Dry 🌬️
- **Fan Speed Control**: Auto, Low, Medium, High
- **Status Monitoring**: Real-time device status updates

### 🎨 User Experience
- **Modern UI**: Beautiful gradient design with smooth animations
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Feedback**: Success/error messages with auto-hide
- **Interactive Controls**: Hover effects and visual feedback

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Using virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Or use Makefile
make web-install
```

### 2. Start the Web App
```bash
# Start the server
python3 app.py

# Or use Makefile
make web
```

### 3. Open in Browser
- Navigate to: `http://localhost:5000`
- Enter your Bluestar app credentials
- Start controlling your AC units!

## 🔧 API Endpoints Tested

The web interface tests all the API endpoints we discovered:

- **`POST /auth/login`** - User authentication (email/password)
- **`POST /auth/login`** - Phone OTP authentication
- **`GET /things`** - Device discovery
- **`GET /things/{id}/state`** - Device status
- **`POST /things/{id}/state`** - Device control
- **`GET /things/{id}/info`** - Device information

## 📱 Screenshots

### Login Screen
- Clean, professional login form
- Email and password fields
- Loading states and error handling

### Main Dashboard
- Device cards for each AC unit
- Power controls (On/Off)
- Temperature slider (16°C - 30°C)
- Mode selection buttons
- Fan speed controls
- Real-time status display

## 🛡️ Security Features

- **HTTPS Only**: All API calls use secure connections
- **Session Management**: Secure session tokens
- **Input Validation**: Proper parameter sanitization
- **Error Handling**: Graceful failure handling
- **No Credential Storage**: Passwords never stored locally

## 🔍 Testing Scenarios

### 1. Authentication Testing
- ✅ **Unified Field**: Single input field for mobile/email
- ✅ **Smart Authentication**: Automatic email/phone login attempts
- ✅ **Email Login**: Valid/invalid credentials handling
- ✅ **Phone Login**: Phone number + password authentication
- ✅ Session persistence and secure logout

### 2. Device Discovery
- ✅ List all devices
- ✅ Handle empty device lists
- ✅ Device metadata display

### 3. Device Control
- ✅ Power on/off
- ✅ Temperature setting
- ✅ Mode switching
- ✅ Fan speed control
- ✅ Status retrieval

### 4. Error Handling
- ✅ Network failures
- ✅ API errors
- ✅ Invalid device IDs
- ✅ Authentication failures

## 🚨 Important Notes

1. **Use Real Credentials**: This app makes actual API calls to Bluestar servers
2. **Test Safely**: Start with power-off commands to verify functionality
3. **Monitor Responses**: Check browser console for detailed API responses
4. **Session Timeout**: Tokens expire after 1 hour, re-login required

## 🐛 Troubleshooting

### Common Issues

**"Login failed"**
- Verify your Bluestar app credentials
- Check if your account has active devices
- Ensure internet connection

**"No devices found"**
- Your account may not have registered AC units
- Try refreshing the device list
- Check if devices are online in the Bluestar app

**"Control failed"**
- Device may be offline
- Check device status first
- Verify device ID is correct

### Debug Mode

Enable debug logging by checking the browser console:
- Network tab shows all API calls
- Console shows detailed error messages
- Response data is logged for debugging

## 🔄 Development

### File Structure
```
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface template
├── requirements.txt       # Python dependencies
└── WEB_README.md         # This file
```

### Adding Features
- **New Controls**: Add to the device card template
- **API Endpoints**: Extend the Flask routes
- **UI Elements**: Modify the HTML/CSS/JavaScript

### Testing New Features
1. Add the feature to the web interface
2. Test with real API calls
3. Verify error handling
4. Update documentation

## 📞 Support

If you encounter issues:
1. Check the browser console for errors
2. Verify your Bluestar credentials
3. Ensure your AC units are online
4. Check the API documentation in `docs/api_map.md`

## 🎯 Next Steps

After testing the web interface:
1. **Home Assistant Integration**: Use the verified API calls in the HA component
2. **Automation**: Create scripts for scheduled AC control
3. **Monitoring**: Build dashboards for energy usage
4. **Integration**: Connect with other smart home systems

---

**Happy AC Testing! ❄️✨**
