# 🔧 OMI Configuration Troubleshooting

## Problem: Alert triggers but no transcripts appear

### Root Cause:
OMI device is not configured to send transcripts to Guardian Angel backend.

---

## ✅ Solution: Configure OMI App

### Your Webhook URL:
```
https://smearier-melodiously-eliseo.ngrok-free.dev/api/omi/webhook
```

### Step-by-Step Configuration:

#### Option A: Real-Time Transcript Webhook (Recommended)

1. **Open OMI App**
2. **Settings** → **Developer Mode** → **ON**
3. **Developer Settings** → **Real-Time Transcript Webhook**
4. **Paste URL:** `https://smearier-melodiously-eliseo.ngrok-free.dev/api/omi/webhook`
5. **Save**

#### Option B: Real-Time Audio Streaming

1. **Open OMI App**
2. **Settings** → **Developer Mode** → **ON**
3. **Developer Settings** → **Real-Time Audio Streaming**
4. **Paste URL:** `https://smearier-melodiously-eliseo.ngrok-free.dev/api/omi/webhook`
5. **Every X seconds:** `5`
6. **Save**

---

## 🧪 Verify Configuration

### Test 1: Check if OMI is Sending Anything

```bash
# Watch Flask console
# You should see webhooks every 5-10 seconds:
🎤 OMI WEBHOOK RECEIVED
```

If you see this, OMI is configured correctly!

### Test 2: Test with Alert

```bash
# 1. Trigger alert
curl -X POST http://localhost:5000/api/alert \
  -d '{"description":"Config test"}'

# 2. Speak into OMI
# "Help! Emergency test!"

# 3. Check Flask console within 10 seconds
# Should see:
🎯 Active alert session found
📝 Transcript: Help! Emergency test!
⚠️ DISTRESS DETECTED!
```

---

## 🔍 Common Issues

### Issue 1: "No webhooks appearing in Flask"

**Possible causes:**
- OMI app webhook URL not configured
- Wrong URL entered
- OMI device not connected (check 🔵 blue light)
- ngrok tunnel expired

**Fix:**
```bash
# Check ngrok is running
curl http://127.0.0.1:4040/api/tunnels

# Should show: smearier-melodiously-eliseo.ngrok-free.dev
# If different, update URL in OMI app
```

### Issue 2: "Webhooks arriving but say 'No active session'"

**This is CORRECT behavior!** It means:
- ✅ OMI is configured properly
- ✅ Transcripts are arriving
- ✅ System is protecting privacy (only processing during alerts)

**Next step:** Trigger an alert, THEN speak

### Issue 3: "Transcripts in wrong language"

**Cause:** OMI detected non-English speech

**Fix:** Speak clearly in English with good pronunciation

---

## 📊 What Success Looks Like

### Before Alert (Normal):
```
Flask Console:
🎤 OMI WEBHOOK RECEIVED
Parsed 2 segments
No active alert session - skipping transcript processing
```

### During Alert (Active):
```
Flask Console:
🎤 OMI WEBHOOK RECEIVED
Parsed 2 segments
🎯 Active alert session found: alert_123456
📝 Transcript: Help! I need assistance!
⚠️ DISTRESS DETECTED!
```

---

## 🎬 Complete Demo Flow

### Setup (Before Demo):
1. OMI powered on (🔵 blue light)
2. OMI app webhook configured
3. ngrok running
4. Flask backend running
5. Dashboard open

### During Demo:
1. **Trigger alert** (hold touch sensor)
   - Flask: "ALERT received"
   - Dashboard: Shows alert

2. **Speak into OMI** (no button press!)
   - "Help! I've fallen!"
   - Wait 5-10 seconds (OMI batches transcripts)

3. **Point to screens:**
   - Flask console: Shows transcript + distress detection
   - Dashboard: Purple OMI card with orange ⚠️ badge

---

## ⚡ Quick Test Commands

### Test ngrok
```bash
curl http://127.0.0.1:4040/api/tunnels | grep public_url
```

### Test webhook endpoint
```bash
curl -X POST "http://localhost:5000/api/omi/webhook?uid=test" \
  -d '{"segments":[{"text":"test"}]}'
```

### Trigger alert
```bash
curl -X POST http://localhost:5000/api/alert \
  -d '{"description":"Manual test"}'
```

### Simulate OMI transcript
```bash
curl -X POST "http://localhost:5000/api/omi/webhook?uid=manual" \
  -d '{"segments":[{"text":"Help! Emergency!"}]}'
```

### Check events
```bash
curl http://localhost:5000/api/events | python3 -m json.tool | head -50
```

---

## 📱 OMI App Screenshots Locations

Look for these sections in OMI app:
- Settings
  - Developer Mode (toggle)
    - Developer Settings
      - Real-Time Transcript Webhook ← **ENTER URL HERE**
      - OR Real-Time Audio Streaming ← **OR HERE**

---

## ✅ Checklist

Configuration complete when you see:
- [ ] OMI device powered on (🔵 blue)
- [ ] OMI app Developer Mode = ON
- [ ] Webhook URL configured in OMI app
- [ ] Flask console shows OMI webhooks arriving
- [ ] Test alert + speech = transcript appears
- [ ] Dashboard shows OMI events in timeline

---

## 🆘 Still Not Working?

### Check All Services:
```bash
# Backend running?
curl http://localhost:5000/api/status

# ngrok running?
curl http://127.0.0.1:4040/api/tunnels

# Dashboard running?
curl http://localhost:5173
```

### Watch Flask Console Live:
Keep Flask console visible during demo - you'll see exactly what's happening in real-time!

---

## 📧 Get Help

- **OMI Discord:** http://discord.omi.me
- **OMI Team:** aarav@basedhardware.com
- **Cal Hacks Slack:** @Aarav Garg

Most common issue: **Webhook URL not configured in OMI app!**
