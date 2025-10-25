# 🔧 OMI Integration Troubleshooting

## Issue: Transcripts stop sending after talking for a bit

### Why This Happens:
OMI has session management - it groups conversations into sessions. When you stop talking for ~30-60 seconds, the session ends and OMI stops sending real-time transcripts.

### Solutions:

#### 1. Keep Talking (Quick Fix)
- Speak continuously or in short bursts
- Don't pause more than 30 seconds between phrases
- Good for demo purposes

#### 2. Start New Recording Session
In OMI app:
- Press the button to stop recording
- Press again to start a new session
- Transcripts will resume

#### 3. Check Session ID in Logs
If you see repeated webhook calls with **no transcript text**, the session has ended. Start a new one.

---

## Issue: Transcripts appear in status but not timeline

### Fixed! ✅
- Backend now broadcasts full transcript data
- Frontend displays OMI events in **purple**
- Distress events show **orange ⚠️ badge**

### Verify It's Working:
1. Open browser console (F12)
2. Look for: `SSE received: {type: "omi_transcript", ...}`
3. Check dashboard timeline - should show purple OMI events

---

## Issue: Distress not detected

### Check These Keywords (case-insensitive):
- help
- emergency
- fall / fell
- hurt
- pain
- scared
- danger

### Test Phrases:
✅ "Help! I need assistance!"
✅ "Emergency! Call someone!"
✅ "I fell down and hurt my leg!"
✅ "I'm scared and in danger!"

❌ "I'm fine" - Won't trigger
❌ "Everything is okay" - Won't trigger

---

## Issue: ngrok connection lost

### Symptoms:
- OMI webhook fails
- Dashboard shows "ERR_NGROK_3200"

### Fix:
```bash
# Restart ngrok
ngrok http 5000

# Get new URL
curl http://127.0.0.1:4040/api/tunnels | grep public_url

# Update in OMI app with new URL
```

---

## Issue: Flask backend crashed

### Check:
```bash
# Is it running?
curl http://localhost:5000/api/status

# If not, restart:
cd /Users/spartan/Documents/calhacks/Guardian_Angel_AI/backend
python3 app.py
```

---

## Quick Debug Checklist

Before demo, verify:

- [ ] Flask backend running (http://localhost:5000)
- [ ] ngrok tunnel active (http://127.0.0.1:4040)
- [ ] OMI webhook configured with correct URL
- [ ] OMI device powered on (🔵 blue light)
- [ ] OMI connected to phone app
- [ ] Dashboard open (http://localhost:5173)
- [ ] Browser console shows SSE messages
- [ ] Test with "help emergency" phrase

---

## Best Practices for Demo

### 1. Pre-Record Sessions
If live OMI fails, have backup:
- Use the dashboard "Simulate Alert" button
- Shows same system flow
- Reliable for judges

### 2. Keep Sessions Short
- Speak for 10-20 seconds
- Check dashboard
- Start new session if needed

### 3. Use Clear Keywords
Speak loudly and clearly:
- "This is an emergency!"
- "Help! I need assistance!"
- "I have fallen down!"

### 4. Have Flask Console Visible
Shows real-time processing:
```
==================================================
🎤 OMI WEBHOOK RECEIVED
📝 Transcript: Help! Emergency!
⚠️  DISTRESS KEYWORDS DETECTED!
==================================================
```

---

## Contact Support

- Email: aarav@basedhardware.com
- Cal Hacks Slack: @Aarav Garg
- Discord: http://discord.omi.me

---

**Most issues are solved by restarting the OMI recording session!**
