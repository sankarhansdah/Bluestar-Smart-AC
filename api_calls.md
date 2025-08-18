# Bluestar Smart AC API Documentation

## Overview
This document contains all the API endpoints, authentication methods, and control mechanisms discovered through reverse engineering the Bluestar Smart AC Android app.

## Base Configuration
- **Base URL**: `https://n3on22cp53.execute-api.ap-south-1.amazonaws.com/prod`
- **Region**: `ap-south-1`
- **Service**: AWS API Gateway + AWS IoT

## Authentication

### Login Endpoint
```
POST /auth/login
```

**Headers Required:**
```
X-APP-VER: v1.0.0-123
X-OS-NAME: Android
X-OS-VER: v13-33
User-Agent: com.bluestarindia.bluesmart
Content-Type: application/json
```

**Request Body:**
```json
{
  "auth_id": "9439614598",  // Phone number or email
  "password": "your_password",
  "auth_type": 1            // 1 for phone, 0 for email
}
```

**Response:**
```json
{
  "session": "749386b2-53d6-4d7c-8f7f-dfbfbb6e5e02",
  "user": {
    "id": "1043df4f-2edf-486b-8a41-8d839cb96c63",
    "name": "Sankar",
    "phone": "9439614598",
    "email": "hansdahshankar@gmail.com",
    "tuya_user_id": "BLSTR:1043df4f-2edf-486b-8a41-8d839cb96c63"
  },
  "mi": "YTI2MzgxZGw3bXVkbzQtYXRzLmlvdC5hcC1zb3V0aC0xLmFtYXpvbmF3cy5jb206OkFLSUEyRE80TUNKSjIyNFhMRFM2Ojo3RmhBbXA5Vm1sYm5CdUtIWWRPbG1CVWJBdXNKc0RYZWVTeGVqcEFE"
}
```

**Important Notes:**
- `mi` field contains base64-encoded AWS IoT credentials
- Decoded `mi` contains: `a26381dl7mudo4-ats.iot.ap-south-1.amazonaws.com::AKIA2DO4MCJJ224XLDSS6::7FhAmp9VmlbnBuKHdYdOlmBUbAusJsDXeeSxejpAD`

## Device Management

### Get Devices List
```
GET /things
```

**Headers Required:**
```
X-APP-SESSION: {session_token}
X-APP-VER: v1.0.0-123
X-OS-NAME: Android
X-OS-VER: v13-33
User-Agent: com.bluestarindia.bluesmart
```

**Response:**
```json
{
  "things": [
    {
      "thing_id": "24587ca091f8",
      "type": 1,
      "model_id": "da8d34d2-449f-42be-a537-6391772dfb86",
      "f_ver": "0.5.7",
      "user_config": {
        "pow": "1",
        "fspd": "4",
        "mode": "2",
        "name": "AC",
        "stemp": "25",
        "power": 1,
        "fan_speed": 4,
        "temperature": "23.0"
      },
      "model_config": {
        "min_temp": 16,
        "max_temp": 30,
        "mode": {
          "0": {"name": "fan", "fspd": {"fixed": false, "default": 2}},
          "2": {"name": "cool", "fspd": {"fixed": false, "default": 7}, "stemp": {"fixed": false, "default": "24"}},
          "3": {"name": "dry", "fspd": {"fixed": true, "default": 2}, "stemp": {"fixed": false, "default": "24"}},
          "4": {"name": "auto", "fspd": {"fixed": true, "default": 7}, "stemp": {"fixed": false, "default": "24"}}
        },
        "fspd": {
          "2": "low",
          "3": "med", 
          "4": "high",
          "6": "turbo",
          "7": "auto"
        }
      }
    }
  ],
  "states": {
    "24587ca091f8": {
      "state": {
        "pow": 0,
        "mode": 2,
        "stemp": "16.0",
        "fspd": 2,
        "ctemp": "30.5",
        "src": "iosmq"
      },
      "connected": true
    }
  }
}
```

## AC Control APIs

### Method 1: Preferences Endpoint (WORKING)
```
POST /things/{device_id}/preferences
```

**Headers Required:**
```
X-APP-SESSION: {session_token}
X-APP-VER: v1.0.0-123
X-OS-NAME: Android
X-OS-VER: v13-33
User-Agent: com.bluestarindia.bluesmart
Content-Type: application/json
```

**Request Body:**
```json
{
  "preferences": {
    "pow": "1",           // Power: "1" = ON, "0" = OFF
    "stemp": "24",        // Set temperature (string)
    "mode": "2",          // Mode: "2" = Cool, "1" = Heat, "0" = Fan, "3" = Dry, "4" = Auto
    "fspd": "4"           // Fan speed: "2" = Low, "3" = Medium, "4" = High, "6" = Turbo, "7" = Auto
  }
}
```

**Response (Success):**
```json
{
  "code": "STATUS_SUCCESS",
  "message": "Request successfull"
}
```

**Important Notes:**
- This is the ONLY endpoint that successfully controls the AC
- All other endpoints return "Missing Authentication Token" for write operations
- Temperature must be sent as a string
- Power values must be strings: "1" or "0"

### Method 2: State Endpoint (READ ONLY)
```
GET /things/{device_id}/state
```

**Response:**
```json
{
  "state": {
    "pow": 0,
    "mode": 2,
    "stemp": "16.0",
    "fspd": 2,
    "ctemp": "30.5",
    "src": "iosmq"
  }
}
```

**Note:** This endpoint only works for reading state, not for control.

### Method 3: Control Endpoint (FAILS)
```
POST /things/{device_id}/control
```

**Note:** This endpoint consistently returns "Missing Authentication Token" for all write operations.

## AWS IoT MQTT Control (Advanced)

### Connection Details
- **Endpoint**: `a26381dl7mudo4-ats.iot.ap-south-1.amazonaws.com`
- **Region**: `ap-south-1`
- **Service**: `iotdata` (NOT `iotdevicegateway`)
- **Protocol**: WebSocket + MQTT over WebSocket
- **Authentication**: AWS SigV4 with temporary credentials from `mi` field

### MQTT Topics
```
# Device Shadow Updates
$aws/things/{device_id}/shadow/update    # Desired state
$aws/things/{device_id}/shadow/get       # Get current state
$aws/things/{device_id}/shadow/update/accepted
$aws/things/{device_id}/shadow/update/rejected
$aws/things/{device_id}/shadow/update/delta

# Direct Control
things/{device_id}/control                # Force sync command
things/{device_id}/control/accepted
things/{device_id}/control/rejected
```

### MQTT Payloads

**Shadow Update (Desired State):**
```json
{
  "state": {
    "desired": {
      "src": "anmq",
      "pow": 1,
      "mode": 2,
      "stemp": "24.0",
      "fspd": 4
    }
  }
}
```

**Force Sync Command:**
```json
{
  "fpsh": 1
}
```

**Client ID Format:**
```
u-{user_id}
```

**QoS Level:**
- All publishes use QoS 0 (At most once)

## Control Parameters Reference

### Power Control
- **Parameter**: `pow`
- **Values**: `"1"` (ON), `"0"` (OFF)
- **Type**: String

### Temperature Control
- **Parameter**: `stemp`
- **Range**: 16-30°C
- **Type**: String (e.g., `"24"`)
- **Note**: Must be sent as string, not number

### Mode Control
- **Parameter**: `mode`
- **Values**:
  - `"0"` = Fan
  - `"1"` = Heat
  - `"2"` = Cool
  - `"3"` = Dry
  - `"4"` = Auto
- **Type**: String

### Fan Speed Control
- **Parameter**: `fspd`
- **Values**:
  - `"2"` = Low
  - `"3"` = Medium
  - `"4"` = High
  - `"6"` = Turbo
  - `"7"` = Auto
- **Type**: String

### Additional Features
- **Parameter**: `eco`
- **Values**: `"1"` (ON), `"0"` (OFF)
- **Type**: String

- **Parameter**: `turbo`
- **Values**: `"1"` (ON), `"0"` (OFF)
- **Type**: String

## Working Control Examples

### Turn AC ON
```bash
curl -X POST "https://n3on22cp53.execute-api.ap-south-1.amazonaws.com/prod/things/24587ca091f8/preferences" \
  -H "X-APP-SESSION: YOUR_SESSION_TOKEN" \
  -H "X-APP-VER: v1.0.0-123" \
  -H "X-OS-NAME: Android" \
  -H "X-OS-VER: v13-33" \
  -H "User-Agent: com.bluestarindia.bluesmart" \
  -H "Content-Type: application/json" \
  -d '{"preferences": {"pow": "1"}}'
```

### Set Temperature to 24°C
```bash
curl -X POST "https://n3on22cp53.execute-api.ap-south-1.amazonaws.com/prod/things/24587ca091f8/preferences" \
  -H "X-APP-SESSION: YOUR_SESSION_TOKEN" \
  -H "X-APP-VER: v1.0.0-123" \
  -H "X-OS-NAME: Android" \
  -H "X-OS-VER: v13-33" \
  -H "User-Agent: com.bluestarindia.bluesmart" \
  -H "Content-Type: application/json" \
  -d '{"preferences": {"stemp": "24"}}'
```

### Set Mode to Cool
```bash
curl -X POST "https://n3on22cp53.execute-api.ap-south-1.amazonaws.com/prod/things/24587ca091f8/preferences" \
  -H "X-APP-SESSION: YOUR_SESSION_TOKEN" \
  -H "X-APP-VER: v1.0.0-123" \
  -H "X-OS-NAME: Android" \
  -H "X-OS-VER: v13-33" \
  -H "User-Agent: com.bluestarindia.bluesmart" \
  -H "Content-Type: application/json" \
  -d '{"preferences": {"mode": "2"}}'
```

## Authentication Flow Summary

1. **Login**: POST to `/auth/login` with phone/email + password
2. **Extract Session**: Use `session` token from response
3. **Control AC**: POST to `/things/{device_id}/preferences` with `X-APP-SESSION` header
4. **Payload Format**: Always use `{"preferences": {...}}` structure

## Key Discoveries

1. **Working Control Method**: Only `/preferences` endpoint works for AC control
2. **Authentication**: `X-APP-SESSION` header is required for all operations
3. **Data Types**: All control values must be strings, not numbers
4. **AWS IoT**: The app uses AWS IoT MQTT for real-time control, but REST API works for basic control
5. **Tuya Integration**: Evidence of Tuya IoT platform integration found in decompiled code

## Troubleshooting

### Common Issues
1. **"Missing Authentication Token"**: Use `/preferences` endpoint, not `/control` or `/state`
2. **"Not authenticated"**: Ensure `X-APP-SESSION` header contains valid session token
3. **Control not working**: Verify payload uses `{"preferences": {...}}` format
4. **Type errors**: Ensure all values are strings, not numbers

### Debug Endpoints
- **Device Info**: `GET /api/debug/devices-info`
- **Raw Response**: `GET /api/debug/things-raw`
- **Parsed Response**: `GET /api/debug/things-parsed`

## Conclusion

The Bluestar Smart AC can be controlled via REST API using the `/preferences` endpoint with the correct authentication headers. The AWS IoT MQTT approach provides real-time control but requires complex WebSocket + SigV4 authentication that we haven't fully implemented yet.

For basic AC control, the REST API method is sufficient and reliable.

