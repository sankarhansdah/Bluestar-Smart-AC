# Bluestar AC Control (AWS IoT WS-MQTT, SigV4)

## 🎯 What This Does

This script creates a **production-ready AWS IoT MQTT client** that mirrors the Bluestar mobile app exactly:

- ✅ **Connects via WebSockets + SigV4** using temporary STS credentials
- ✅ **Uses exact clientId pattern** `u-<USER_ID>` (required by the app)
- ✅ **Publishes to device shadow** with `src:"anmq"` and correct types
- ✅ **Sends force apply command** `{"fpsh": 1}` to trigger the AC
- ✅ **Subscribes to diagnostic topics** to verify round-trip
- ✅ **QoS 0** for all publishes (matches the app behavior)

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
# Activate your virtual environment
source venv/bin/activate

# Install AWS IoT SDK v2
pip install -r requirements.txt
```

### 2. Create Environment File
```bash
# Copy the example
cp env_example.txt .env

# Edit .env with your real credentials from login 'mi' block
nano .env
```

### 3. Fill Your Credentials

**From your login response, extract these values:**

```json
{
  "session": "8bfbfd8b-5da0-476e-99c8-c9c6f812d36d",
  "user": {
    "id": "1043df4f-2edf-486b-8a41-8d839cb96c63"
  },
  "mi": "YTI2MzgxZGw3bXVkbzQtYXRzLmlvdC5hcC1zb3V0aC0xLmFtYXpvbmF3cy5jb206OkFLSUEyRE80TUNKSjIyNFhMRFM2Ojo3RmhBbXA5Vm1sYm5CdUtIWWRPbG1CVWJBdXNKc0RYZWVTeGVqcEFE"
}
```

**Decode the `mi` field to get AWS credentials:**
```bash
# The mi field contains: endpoint:access_key:secret_key:session_token
# Decode from base64 and split by colons
```

**Your .env should look like:**
```bash
IOT_ENDPOINT=a26381dl7mudo4-ats.iot.ap-south-1.amazonaws.com
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=AKIA2DO4MCJJ224XLD6
AWS_SECRET_ACCESS_KEY=7FhAmp9VmlbnBuKHYdOlmBUaAuJsDXeeSxejpAD
AWS_SESSION_TOKEN=7FhAmp9VmlbnBuKHYdOlmBUaAuJsDXeeSxejpAD

BLUESTAR_THING_ID=24587ca091f8
BLUESTAR_USER_ID=1043df4f-2edf-486b-8a41-8d839cb96c63
```

## 🎮 Usage

### Basic Control (Turn ON AC)
```bash
python mqtt_control.py --pow 1 --mode 2 --stemp 23.0 --fspd 4
```

### Turn OFF AC
```bash
python mqtt_control.py --pow 0 --mode 2 --stemp 23.0 --fspd 4
```

### Change Temperature
```bash
python mqtt_control.py --pow 1 --mode 2 --stemp 25.0 --fspd 4
```

### With TRACE Logs (First Time)
```bash
python mqtt_control.py --trace --pow 1 --mode 2 --stemp 23.0 --fspd 4
```

## 🔍 Expected Flow

1. **Connects** with clientId=`u-1043df4f-2edf-486b-8a41-8d839cb96c63`
2. **Subscribes** to diagnostic topics
3. **Gets current shadow** state
4. **Publishes desired state** to `$aws/things/24587ca091f8/shadow/update`
5. **Publishes force apply** `{"fpsh": 1}` to `things/24587ca091f8/control`
6. **You should see**:
   - `.../shadow/update/accepted` 
   - `.../shadow/update/delta` with new `reported.pow: 1`
   - AC physically responds (power on/temp change)

## 🛠️ Troubleshooting

### Connection Issues
- **Session token missing** → Handshake fails. Ensure `AWS_SESSION_TOKEN` is set
- **Clock skew** → Sync system time (macOS: System Settings → Date & Time)
- **Wrong endpoint** → Must be `*-ats.iot.ap-south-1.amazonaws.com`

### Policy Issues
- **Connect works but publish/subscribe don't** → IoT policy may restrict topics
- **Use exact clientId** = `u-<USER_ID>` (required pattern)
- **Check region** = `ap-south-1`

### Type Issues
- **Keep `stemp` as string** with one decimal: `"23.0"`
- **Others can be integers**: `pow: 1`, `mode: 2`, `fspd: 4`
- **QoS must be 0** (matches app)

## 📱 Integration with Web UI

This MQTT control can be integrated into your Flask web interface:

1. **Add MQTT control endpoints** to `app.py`
2. **Call this script** from web routes
3. **Real-time AC control** via the beautiful modern UI

## 🎯 Success Criteria

✅ **You see `[MQTT] Connected`**  
✅ **You receive `.../accepted` or `.../delta` responses**  
✅ **AC physically responds** (power on/off, temp change)  
✅ **No WebSocket handshake errors**  

## 🚨 If Still Blocked

1. **Run with `--trace`** and paste the last 20 lines around "WebSocket handshake failed"
2. **Confirm exact `clientId`** in `.env` (must be `u-<USER_ID>`)
3. **Confirm `AWS_SESSION_TOKEN`** present and not expired
4. **Check system clock** is accurate

---

**This is the exact same MQTT implementation the mobile app uses!** 🎯✨

