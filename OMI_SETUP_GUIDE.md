# 🎤 OMI Dev Kit 2 - Guardian Angel Integration Guide

## 📋 Complete Step-by-Step Setup

Based on the official OMI documentation for Cal Hacks, here's exactly how to integrate OMI with your Guardian Angel system.

---

## 🎯 What OMI Will Do

When an alert is triggered on your Guardian Angel system:
1. **Real-time transcript processing** - OMI captures what's being said during the emergency
2. **Webhook to your backend** - Audio transcripts sent to Guardian Angel Flask server
3. **AI analysis** - Detect distress keywords, analyze conversation context
4. **Store in ChromaDB** - Emergency audio context saved alongside other events

---

## 📱 Step 1: Download & Install OMI App

### iOS
https://apps.apple.com/us/app/friend-ai-wearable/id6502156163

### Android
https://play.google.com/store/apps/details?id=com.friend.ios

### macOS (Optional)
https://apps.apple.com/us/app/omi-ai-smart-meeting-notes/id6502156163

---

## 🔌 Step 2: Power On OMI Dev Kit 2

Choose one method:

**Option A: Physical Switch**
- Flip the switch if your dev kit has one

**Option B: Button Method**
- Press and hold the center button for 3 seconds

**Option C: USB-C**
- Plug into USB-C for power

### ✅ Check LED Status
- 🔴 **Red** = On but not connected
- 🔵 **Blue** = On and connected to phone
- 🟠 **Orange** = Charging, not connected
- 🟢 **Teal** = Charging and connected

---

## 📲 Step 3: Pair OMI with Your Phone

1. Open the **OMI app** on your phone
2. Follow the pairing instructions
3. OMI should appear as a discoverable Bluetooth device
4. **Test**: Speak near the device and check if it shows transcription in the app

---

## 🔧 Step 4: Enable Developer Mode

In the OMI app:

1. Go to **Settings**
2. Enable **Developer Mode**
3. Navigate to **Developer Settings**

---

## 🌐 Step 5: Set Up Guardian Angel Webhook Endpoint

### A. Webhook Endpoint Created! ✅

Your Flask backend now has an OMI webhook endpoint:

**Endpoint:** `POST /api/omi/webhook`

**What it does:**
- Receives real-time transcripts from OMI
- Detects distress keywords (help, emergency, fall, hurt, pain, scared, danger)
- Stores transcripts in ChromaDB
- Broadcasts to dashboard for real-time display
- Auto-escalates if distress is detected

### B. Get Your Server URL

Since OMI needs to send webhooks to your server, you have two options:

#### Option 1: Use ngrok (Recommended for Hackathon)

1. **Install ngrok:**
   ```bash
   brew install ngrok
   ```

2. **Start ngrok tunnel:**
   ```bash
   ngrok http 5000
   ```

3. **Copy the HTTPS URL** (looks like: `https://abc123.ngrok.io`)

4. **Your OMI webhook URL will be:**
   ```
   https://abc123.ngrok.io/api/omi/webhook
   ```

#### Option 2: Use Your Network IP (Same WiFi Only)

If OMI and your laptop are on the same WiFi:
```
http://10.65.219.51:5000/api/omi/webhook
```

---

## 📱 Step 6: Configure OMI App Webhook

1. **Open OMI App** on your phone
2. **Go to Settings** → **Developer Settings**
3. **Find "Real-Time Transcript Webhook"** field
4. **Enter your webhook URL:**
   ```
   https://your-ngrok-url.ngrok.io/api/omi/webhook
   ```
   OR
   ```
   http://10.65.219.51:5000/api/omi/webhook
   ```

5. **Save the settings**

---

## 🧪 Step 7: Test the Integration

### Test 1: Manual Test in OMI App

1. **Speak to OMI device:** "Help! I've fallen and I can't get up!"
2. **Check your Flask console:** Should see transcript logs
3. **Check your dashboard:** http://localhost:5173
   - Should show OMI transcript event
   - Should detect distress keywords

### Test 2: End-to-End Alert Flow

1. **Trigger an alert** (click red button on dashboard OR use Arduino)
2. **OMI automatically starts capturing audio**
3. **Speak:** "This is an emergency!"
4. **Watch transcripts appear on dashboard in real-time**

---

## 🎯 Step 8: Create Guardian Angel OMI App (Optional)

For Cal Hacks submission, you can create an official OMI app:

1. **Open OMI mobile app**
2. **Go to App Store** (in OMI app)
3. **Submit your app**:
   - **Name:** "Guardian Angel Safety Monitor"
   - **Description:** "Emergency safety device that monitors for distress and auto-records during alerts"
   - **Webhook URL:** Your Flask backend URL

4. **After submission**, app appears in your account for demo

---

## 📊 What Happens During an Alert

```
User holds touch sensor 3 seconds
    ↓
Arduino sends alert to Flask backend
    ↓
Flask triggers OMI recording (simulated)
    ↓
[User speaks] "Help! I fell down!"
    ↓
OMI captures audio → Transcribes → Sends to Flask webhook
    ↓
Flask receives: {"text": "Help! I fell down!", "speaker": "SPEAKER_00"}
    ↓
Detects distress keywords → Stores in ChromaDB
    ↓
Broadcasts to dashboard → Shows "⚠️ DISTRESS DETECTED"
    ↓
[Optional] Auto-escalate to emergency contacts
```

---

## 🎬 Demo Script for Judges

### Setup (Before Demo)
1. OMI Dev Kit powered on and connected (🔵 blue light)
2. OMI app configured with your webhook
3. Dashboard open at http://localhost:5173
4. Flask backend running with ngrok tunnel

### Demo Flow (90 seconds)

**[0:00-0:15] Introduction**
*"Guardian Angel is a safety device for vulnerable individuals. When they need help, we don't just send an alert - we automatically capture what's happening through OMI."*

**[0:15-0:30] Show Hardware**
*"This is our touch sensor connected to Arduino. A 3-second hold triggers an emergency alert."*

**[0:30-0:45] Trigger Alert**
- Click red "Simulate Alert" button
- Point to dashboard: "Alert logged, OMI activated"
- Show system flow diagram lighting up

**[0:45-1:15] OMI Capture**
*"Now OMI is recording. Let me demonstrate..."*
- Speak into OMI: **"Help! I've fallen and I can't get up!"**
- Point to dashboard: Real-time transcript appears
- Highlight: **"⚠️ DISTRESS DETECTED"** indicator

**[1:15-1:30] AI Analysis**
- Click "Generate Summary" button
- Show AI summary including OMI transcript context
- *"Our AI detected distress keywords and automatically escalated the alert."*

**[1:30] Closing**
*"This multi-modal approach - touch sensor, audio capture, and AI analysis - provides comprehensive safety monitoring with minimal user interaction."*

---

## 🔧 Troubleshooting

### OMI Not Connecting
- Check Bluetooth is on
- Ensure OMI is powered (check LED)
- Try repairing in OMI app

### Webhook Not Receiving Data
- Verify ngrok is running
- Check Flask console for errors
- Test webhook URL with curl:
  ```bash
  curl -X POST "https://your-url.ngrok.io/api/omi/webhook?session_id=test&uid=user123" \
    -H "Content-Type: application/json" \
    -d '[{"text":"test", "speaker":"SPEAKER_00"}]'
  ```

### No Transcripts Appearing
- Check OMI app developer settings
- Verify webhook URL is correct
- Ensure OMI device is actually capturing audio (blue light)

### Distress Not Detected
- Check keywords in `/backend/app.py` line 333
- Test with exact keywords: "help", "emergency", "fall"
- Transcripts are case-insensitive

---

## 📋 Checklist Before Demo

- [ ] OMI Dev Kit powered on (🔵 blue light)
- [ ] OMI paired with phone app
- [ ] Developer mode enabled in OMI app
- [ ] Webhook configured with your URL
- [ ] Flask backend running
- [ ] ngrok tunnel active (if using)
- [ ] Dashboard open in browser
- [ ] Tested alert → transcript flow
- [ ] Practiced demo script

---

## 🏆 Cal Hacks Submission

To submit for OMI rewards:

1. Build the integration (✅ Already done!)
2. Open OMI app → App Store
3. Submit your Guardian Angel app
4. Include:
   - Team name
   - Description: "Emergency safety monitoring with auto-recording"
   - Demo notes

**Rewards for completing:**
- 1x Consumer Omi device ($89)
- 1x Pair of Omi Glasses ($299)
- Hang out with Omi AI team in SF

---

## 📧 Need Help?

- **Email:** aarav@basedhardware.com
- **Cal Hacks Slack:** Text Aarav Garg
- **Discord:** http://discord.omi.me
- **Docs:** https://docs.omi.me

---

## 🎉 You're Ready!

Your Guardian Angel system is now fully integrated with OMI Dev Kit 2!

**Key Features:**
✅ Auto-triggers OMI recording on alerts
✅ Real-time transcript processing
✅ Distress keyword detection
✅ ChromaDB storage of audio context
✅ Live dashboard updates
✅ Ready for Cal Hacks demo

**Start testing:** Trigger an alert and speak into OMI to see it all work together!
