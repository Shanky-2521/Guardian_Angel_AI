# 🎤 OMI Integration - Quick Reference Card

## ⚡ Quick Setup (5 Minutes)

### 1. Power On OMI
Press and hold center button for 3 seconds
- 🔴 Red = On, not connected
- 🔵 Blue = On and connected ✓

### 2. Pair with Phone
- Open OMI app
- Follow pairing instructions
- Test: Speak and check for transcription

### 3. Enable Developer Mode
- OMI App → Settings → Developer Mode → ON

### 4. Get Your Webhook URL

**Option A: ngrok (Recommended)**
```bash
brew install ngrok
ngrok http 5000
# Copy the https URL
```

**Option B: Local Network**
```
http://10.65.219.51:5000/api/omi/webhook
```

### 5. Configure Webhook
- OMI App → Developer Settings
- Real-Time Transcript Webhook: Paste your URL
- Save

### 6. Test
Speak into OMI: "Help! Emergency!"
Check Flask console for transcripts

---

## 🎯 What It Does

When an alert triggers:
1. OMI captures audio → transcribes in real-time
2. Sends to Guardian Angel webhook
3. AI detects distress keywords
4. Stores in ChromaDB
5. Shows on dashboard with ⚠️ alert

---

## 🔑 Distress Keywords

System auto-detects:
- help
- emergency  
- fall / fallen
- hurt
- pain
- scared
- danger

---

## 🧪 Quick Test

```bash
curl -X POST "http://localhost:5000/api/omi/webhook?session_id=test&uid=user" \
  -H "Content-Type: application/json" \
  -d '[{"text":"Help! I fell down!", "speaker":"SPEAKER_00"}]'
```

Expected: `"distress_detected": true`

---

## 📍 Your URLs

- **Dashboard:** http://localhost:5173
- **Backend:** http://localhost:5000
- **Network Backend:** http://10.65.219.51:5000
- **OMI Webhook:** http://10.65.219.51:5000/api/omi/webhook
- **ngrok URL:** (Run `ngrok http 5000` to get)

---

## 🎬 30-Second Demo

1. "Watch this - I'll trigger an alert"
2. Click red button on dashboard
3. Speak into OMI: "Help! I've fallen!"
4. Point to dashboard: "Real-time transcript + distress detection"
5. "System automatically captured emergency context"

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| OMI not connecting | Check Bluetooth, repair device |
| No webhooks | Verify URL in OMI app settings |
| No distress detection | Use exact keywords: help, emergency |
| ngrok down | Restart: `ngrok http 5000` |

---

## 📋 Pre-Demo Checklist

- [ ] OMI powered on (🔵 blue)
- [ ] Paired with phone
- [ ] Developer mode enabled
- [ ] Webhook URL configured
- [ ] Flask backend running
- [ ] ngrok active (if using)
- [ ] Dashboard open
- [ ] Test with "help" keyword

---

## 🏆 For Cal Hacks Submission

Submit in OMI app → App Store:
- Name: Guardian Angel Safety Monitor
- Description: Auto-recording emergency safety device
- Webhook: Your ngrok/network URL

**Rewards:** $89 Omi device + $299 Omi Glasses

---

## 📞 Emergency Contacts

- Aarav Garg: aarav@basedhardware.com
- Cal Hacks Slack: @Aarav Garg
- Discord: http://discord.omi.me

---

**🎉 System Status: READY FOR DEMO**
