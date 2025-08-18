# 🔍 Frida & Network Analysis for Bluestar MQTT Commands

This document outlines the approach to capture the **exact MQTT commands** that the Bluestar iOS app sends to control the AC.

## 🎯 Goal

Capture the **precise MQTT payload structure** that the mobile app uses, so we can replicate it exactly in our Python scripts.

## 🛠️ Tools Created

### 1. **iOS Frida Hook Script** (`frida_hook_ios_mqtt.js`)
- Hooks into iOS MQTT methods
- Captures AWS IoT MQTT Manager calls
- Monitors JSON serialization
- Tracks network requests

### 2. **Network Traffic Monitor** (`simple_network_monitor.py`)
- Uses `tcpdump` to capture MQTT packets
- Monitors ports 8883, 443, 1883
- Analyzes packet payloads for MQTT patterns
- Extracts JSON content

### 3. **MQTT Payload Tester** (`test_mqtt_payloads.py`)
- Tests various payload formats systematically
- Attempts different command structures
- Validates what works vs. what doesn't

## 🚀 How to Use

### Option A: iOS Frida (Requires Jailbroken Device)

1. **Install Frida on iOS device**
2. **Run the hook script:**
   ```bash
   frida -U -l frida_hook_ios_mqtt.js -f com.bluestar.bluesmart
   ```

3. **Use the iOS app to control the AC**
4. **Watch console for captured MQTT commands**

### Option B: Network Traffic Analysis (No Jailbreak Required)

1. **Start network monitoring:**
   ```bash
   python3 simple_network_monitor.py
   ```

2. **Use the iOS app to control the AC**
3. **Watch for MQTT packets and JSON payloads**

### Option C: Systematic Payload Testing

1. **Run the payload tester:**
   ```bash
   python3 test_mqtt_payloads.py
   ```

2. **Monitor AC response to each format**
3. **Identify which payload structure works**

## 📱 What We're Looking For

### MQTT Command Structure
```json
{
  "src": "iosmq",           // Source identifier
  "cmd": "set",             // Command type
  "attrs": {                // Attributes to set
    "pow": 1,               // Power state
    "mode": 2,              // Mode (cool/heat/etc)
    "stemp": "23.0",        // Set temperature
    "fspd": 4               // Fan speed
  },
  "fpsh": 1,                // Force push flag
  "ts": 1234567890,         // Timestamp
  "reqId": "uuid-here"      // Request ID
}
```

### MQTT Topics
- **Control:** `things/{device_id}/control`
- **Shadow Update:** `$aws/things/{device_id}/shadow/update`
- **Shadow Get:** `$aws/things/{device_id}/shadow/get`

## 🔍 Expected Findings

Based on our analysis, we expect to find:

1. **Exact JSON structure** the app uses
2. **Required fields** that can't be omitted
3. **Data types** (string vs number for temperature)
4. **Source identifiers** that matter
5. **Timing patterns** for commands
6. **QoS levels** used by the app

## 🎯 Next Steps After Capture

1. **Replicate exact payload** in our Python scripts
2. **Test with captured structure**
3. **Verify AC responds** to the exact format
4. **Implement working control** in our web interface

## 🚨 Troubleshooting

### Frida Issues
- **Device not found:** Check USB connection and device trust
- **Permission denied:** Ensure device is trusted in iOS
- **App not found:** Verify bundle identifier

### Network Monitor Issues
- **No packets:** Check interface name and permissions
- **Permission denied:** Run with `sudo` for tcpdump
- **No MQTT traffic:** Verify app is actually sending MQTT

### Payload Tester Issues
- **Connection failed:** Check AWS credentials and endpoint
- **No AC response:** Verify payload format matches app exactly

## 📋 Success Criteria

✅ **MQTT commands captured** from iOS app  
✅ **Exact payload structure** identified  
✅ **AC responds** to replicated commands  
✅ **Web interface** can control AC successfully  

## 🔄 Fallback Plan

If Frida/network analysis fails:

1. **Deep decompilation** of iOS app binary
2. **Static analysis** of MQTT client code
3. **Reverse engineering** of command structures
4. **Trial and error** with different payload formats

## 📚 Resources

- [Frida Documentation](https://frida.re/docs/)
- [MQTT Protocol Specification](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)
- [AWS IoT MQTT Guide](https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html)
- [iOS App Reverse Engineering](https://github.com/iOS-Reverse-Engineering-Dev/iOS-Reverse-Engineering)

---

**🎯 The goal is to capture the EXACT command that works, then replicate it perfectly in our Python scripts!**

