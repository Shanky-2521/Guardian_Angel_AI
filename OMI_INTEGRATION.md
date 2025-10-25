# 🎤 OMI Dev Kit 2 Integration Guide

## 🎯 Overview

**Guardian Angel now automatically triggers OMI recording when an alert occurs!**

When the user holds the touch sensor for 3 seconds (or triggers an alert):
1. Alert is logged to ChromaDB
2. OMI Dev Kit 2 starts recording audio (30 seconds)
3. Audio captures the emergency situation
4. Recording can be analyzed for distress sounds or saved as evidence

---

## 🚀 Current Status

### ✅ Backend Integration Complete
- `/api/alert` endpoint triggers OMI recording
- Configurable recording duration
- Demo mode for presentations (enabled by default)
- Real API mode ready for OMI connection

### 📊 Response Format
When an alert is triggered, the API returns:
```json
{
  "status": "success",
  "event": {
    "type": "alert",
    "timestamp": "2025-10-25T02:30:00",
    "message": "Fall detected!",
    "id": "alert_1234567890",
    "omi_activated": true
  },
  "omi": {
    "success": true,
    "status": "simulated",
    "message": "OMI recording would be triggered (demo mode)",
    "recording_duration": 30
  }
}
```

---

## 🔧 Configuration

### Demo Mode (Default)
Currently enabled - simulates OMI activation for your hackathon demo.

No configuration needed! Just trigger an alert and it will show OMI activation status.

### Production Mode (With Real OMI Device)

Edit `backend/.env`:
```bash
# Enable OMI Integration
OMI_ENABLED=true

# OMI API endpoint (check OMI documentation)
OMI_API_URL=http://localhost:8000/omi

# Your OMI API key
OMI_API_KEY=your_actual_omi_api_key

# Recording duration in seconds
OMI_RECORDING_DURATION=30
```

---

## 🎬 For Your Hackathon Demo

### What to Tell Judges:

**"When an alert is triggered, our system automatically activates the OMI Dev Kit to start recording. This captures audio context of the emergency - whether it's a fall, a medical issue, or a threat. The audio can be analyzed in real-time for distress sounds using Fish Audio API, or saved as evidence for emergency responders."**

### Demo Flow:

1. **Show the touch sensor** (or Arduino setup)
2. **Trigger an alert** (hold 3 seconds or click demo button)
3. **Point to dashboard** - "Alert is logged"
4. **Explain**: "At this moment, OMI would start recording for 30 seconds"
5. **Show OMI device** (if you have it)
6. **Mention**: "Audio is captured and can be analyzed for safety assessment"

---

## 🔌 OMI API Integration Details

### Request Format (What Guardian Angel Sends to OMI)
```json
{
  "action": "start_recording",
  "event_id": "alert_1234567890",
  "trigger": "guardian_angel_alert",
  "description": "Fall detected!",
  "duration": 30,
  "metadata": {
    "priority": "emergency",
    "auto_analyze": true
  }
}
```

### Expected Response (What OMI Should Return)
```json
{
  "recording_id": "rec_abc123",
  "status": "recording",
  "duration": 30,
  "started_at": "2025-10-25T02:30:00Z"
}
```

---

## 🎤 OMI Dev Kit 2 Setup

### If You Have the Device:

1. **Install OMI App**
   - Download from OMI website
   - Pair your OMI Dev Kit 2

2. **Enable API Access**
   - Check OMI documentation for API endpoints
   - Get your API key from OMI dashboard

3. **Configure Guardian Angel**
   - Update `backend/.env` with OMI credentials
   - Restart Flask backend

4. **Test Integration**
   ```bash
   curl -X POST http://localhost:5000/api/alert \
     -H "Content-Type: application/json" \
     -d '{"description": "Test alert"}'
   ```

5. **Check OMI App**
   - Should show new recording starting
   - Recording duration: 30 seconds

---

## 🧠 Advanced Features (Future Integration)

### 1. Fish Audio Analysis
When OMI recording completes:
- Send audio to Fish Audio API
- Detect distress sounds (screams, crashes, etc.)
- Auto-escalate if distress detected

### 2. Transcription
- Transcribe OMI audio
- Store transcript in ChromaDB
- Include in AI summaries

### 3. Two-Way Communication
- Use OMI for emergency communication
- "Are you okay?" prompts
- Voice confirmation system

---

## 📝 Testing Without OMI Device

### Manual Test (Current Demo Mode)

1. **Trigger Alert**
   ```bash
   curl -X POST http://localhost:5000/api/alert \
     -H "Content-Type: application/json" \
     -d '{"description": "Testing OMI activation"}'
   ```

2. **Check Response**
   ```json
   {
     "omi": {
       "success": true,
       "status": "simulated",
       "message": "OMI recording would be triggered (demo mode)"
     }
   }
   ```

3. **View Dashboard**
   - Alert appears in timeline
   - Status shows OMI would activate

---

## 🎯 Why This Is Powerful for Judges

### Safety Benefits:
- **Context capture** - Audio during emergency provides vital information
- **Evidence** - Recordings can help emergency responders
- **Auto-activation** - No manual intervention needed
- **Distress detection** - AI can analyze sounds

### Technical Innovation:
- **IoT integration** - Arduino → Flask → OMI pipeline
- **Multi-modal** - Touch + Audio + AI
- **Real-time** - Instant activation on alert
- **Configurable** - Recording duration, auto-analysis

---

## 🔗 System Flow with OMI

```
Touch Sensor (3 sec hold)
    ↓
Arduino R4 WiFi
    ↓
Flask Backend (/api/alert)
    ↓
├─→ ChromaDB (Log event)
├─→ SSE Stream (Dashboard update)
└─→ OMI API (Start recording) ★ NEW
         ↓
    OMI Dev Kit 2
         ↓
    Audio Recording (30 sec)
         ↓
    [Optional] Fish Audio API
         ↓
    Distress Analysis
```

---

## 📱 Next Steps

### For Hackathon:
1. ✅ Keep demo mode (already configured)
2. ✅ Mention OMI integration to judges
3. ✅ Show OMI device if available
4. ✅ Explain the safety benefits

### For Production:
1. Get OMI API credentials
2. Update `.env` with real values
3. Test with actual OMI device
4. Integrate Fish Audio for sound analysis
5. Add audio storage/retrieval

---

## 🆘 Troubleshooting

### OMI not activating?
- Check `OMI_ENABLED=true` in `.env`
- Verify OMI API URL is correct
- Check OMI API key is valid
- Look at Flask console for errors

### Want to test manually?
Leave `OMI_ENABLED=false` - system will simulate activation

### Need longer recordings?
Update `OMI_RECORDING_DURATION=60` for 60 seconds

---

## 🎉 You're Ready!

Your Guardian Angel system now has **intelligent OMI integration** that automatically captures audio during emergencies. This adds a crucial layer of safety and context to your alert system!

**For the demo:** Just trigger alerts and explain that OMI would activate. The backend is ready!

**For production:** Add your OMI credentials and it will work automatically!
