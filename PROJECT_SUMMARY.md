# 🛡️ Guardian Angel AI - Complete Project Summary

## 📋 Project Overview

**Guardian Angel AI** is an intelligent emergency response system that combines IoT hardware (Arduino), wearable AI (OMI), voice synthesis (Fish Audio), and real-time dashboards to provide comprehensive safety monitoring and emergency assistance.

**Built for:** Cal Hacks 2025  
**Team:** Your Team Name  
**Prize Targets:** Best Use of Fish Audio ($250 + $250 API credits)

---

## 🎯 Problem Statement

Traditional emergency alert systems have critical limitations:
- ❌ **Robotic, unclear alerts** - "Alert!" provides no context
- ❌ **No situation awareness** - Emergency contacts don't know severity
- ❌ **Poor accessibility** - Elderly and vulnerable populations struggle with complex systems
- ❌ **Delayed response** - Lack of information slows emergency response

**Guardian Angel AI solves this with intelligent, context-aware emergency communication.**

---

## ✨ Key Features

### 🔴 **Emergency Detection**
- **Arduino touch sensor** - 3-second hold triggers emergency alert
- **Instant response** - Sub-100ms dashboard updates
- **Multi-channel alerts** - Alexa announcements + Dashboard + OMI recording

### 🎤 **Real-Time Audio Monitoring (OMI Integration)**
- **Automatic recording** during emergencies
- **Live transcription** of user speech
- **Distress detection** using AI keyword analysis
- **Privacy protection** - Stops recording after alert resolution

### 🐟 **Intelligent Voice Summaries (Fish Audio)**
- **Smart analysis** - Processes OMI transcripts for context
- **Natural voice** - Professional TTS instead of robotic alerts
- **Context-aware messaging** - Includes severity, time, keywords, actions
- **Auto-generated** - Triggers every 3 transcripts
- **Local playback** - Plays on emergency contact's device

### ✅ **Quick Resolution**
- **Triple-tap check-in** - 3 taps within 5 seconds resolves alert
- **Privacy enforcement** - Automatically stops OMI recording
- **Status tracking** - Real-time alert state on dashboard

### 📊 **Real-Time Dashboard**
- **Live updates** via Server-Sent Events (SSE)
- **Event timeline** - Alerts, transcripts, check-ins
- **System flow visualization** - See data flow in real-time
- **Alert status** - Visual indicators (red/green/idle)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Guardian Angel AI System                 │
└─────────────────────────────────────────────────────────────┘

    [Arduino R4 WiFi]                    [OMI Dev Kit 2]
    Touch Sensor (GPIO 8)                Wearable AI Device
           │                                    │
           │ WiFi                               │ Webhook
           │                                    │
           ↓                                    ↓
    ┌──────────────────────────────────────────────────┐
    │  simple_server_enhanced.py (Arduino Laptop)      │
    │  • Receives Arduino events                       │
    │  • Forwards via ngrok tunnel                     │
    └──────────────────────────────────────────────────┘
                         │
                         │ HTTPS (ngrok)
                         ↓
    ┌──────────────────────────────────────────────────┐
    │  Backend (Flask API) - Main Laptop               │
    │  • ChromaDB for event storage                    │
    │  • SSE for real-time updates                     │
    │  • OMI transcript processing                     │
    │  • Fish Audio integration                        │
    │  • Alert state management                        │
    └──────────────────────────────────────────────────┘
           │              │              │
           │              │              │
           ↓              ↓              ↓
    [Fish Audio]    [IFTTT/Alexa]   [Dashboard]
    Natural Voice   Voice Announce   Real-time UI
    Summaries       "Alert!"         Live Updates
```

---

## 🛠️ Tech Stack

### Hardware
- **Arduino R4 WiFi** - ESP32-based microcontroller
- **Grove Touch Sensor** - Capacitive touch detection
- **OMI Dev Kit 2** - Wearable AI device with real-time transcription

### Backend
- **Python 3.9+** - Core language
- **Flask** - Web framework and API server
- **ChromaDB** - Vector database for event storage
- **ngrok** - Secure tunneling for cross-network communication
- **Fish Audio API** - Text-to-speech synthesis
- **Anthropic Claude** (Optional) - AI distress analysis

### Frontend
- **React** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Lucide Icons** - Icon library

### Integrations
- **IFTTT Webhooks** - Alexa voice announcements
- **Server-Sent Events (SSE)** - Real-time dashboard updates

---

## 📁 Project Structure

```
Guardian_Angel_AI/
├── arduino/
│   └── GuardianAngel/
│       └── GuardianAngel.ino          # Arduino firmware
│
├── backend/
│   └── app.py                         # Main Flask API (650+ lines)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # Main dashboard component
│   │   └── main.jsx                   # Entry point
│   └── package.json
│
├── simple_server_enhanced.py          # Arduino → Backend relay
├── test_fish_audio.py                 # Fish Audio integration test
│
├── ARDUINO_ALEXA_INTEGRATION.md       # Arduino setup guide
├── PROJECT_SUMMARY.md                 # This file
└── README.md                          # Original README
```

---

## 🔄 How It Works

### 1️⃣ **Emergency Alert Triggered**

```
User holds Arduino touch sensor for 3 seconds
    ↓
Arduino sends HTTP POST to simple_server_enhanced.py
    ↓
Server forwards to backend via ngrok tunnel
    ↓
Backend creates alert in ChromaDB
```

### 2️⃣ **Multi-Channel Response**

```
Backend receives alert
    ├─→ IFTTT Webhook → Alexa announces "Guardian Angel Alert!"
    ├─→ SSE Broadcast → Dashboard shows alert (red status)
    └─→ OMI Activation → Starts recording audio
```

### 3️⃣ **OMI Real-Time Processing**

```
OMI captures audio + generates transcripts
    ↓
Webhook sends transcripts to backend
    ↓
Backend analyzes for distress keywords
    ↓
Stores in ChromaDB + Broadcasts to dashboard
    ↓
After 3 transcripts → Fish Audio processing
```

### 4️⃣ **🐟 Fish Audio Intelligence**

```
Collect 3 OMI transcripts:
    - "Help me please"
    - "Someone is following me"
    - "I'm scared"
    ↓
Smart Analysis:
    - Detect keywords: help (3x), scared (1x)
    - Calculate severity: HIGH
    - Generate context: time, action needed
    ↓
Create Summary:
    "Critical emergency detected at 3:45 PM. 
     Multiple distress signals identified. 
     User mentioned: help, scared, following.
     Immediate response required."
    ↓
Fish Audio TTS API:
    - Convert text → natural voice (MP3)
    - Professional female voice
    - Calm, clear pronunciation
    ↓
Playback:
    - Download MP3 to /tmp/
    - Play on local machine (afplay/mpg123)
    - Emergency contact hears natural voice
```

### 5️⃣ **Alert Resolution**

```
User taps sensor 3 times within 5 seconds
    ↓
Backend detects triple-tap pattern
    ↓
Marks alert as resolved
    ↓
Stops OMI recording (privacy protection)
    ↓
Dashboard status → Green
    ↓
Old transcripts filtered from timeline
```

---

## 🐟 Fish Audio Integration - Deep Dive

### Why Fish Audio?

**Traditional Alert:**
```
🔊 "Guardian Angel Alert!"
```
- No context
- Robotic voice
- Doesn't tell you what to do

**Fish Audio Enhanced:**
```
🔊 "Emergency alert detected at 3:45 PM. Analysis of user speech 
    shows multiple distress signals. User mentioned: help, scared, 
    and danger. Alert level: Critical. Immediate response required. 
    Location: Home."
```
- Full context
- Natural, professional voice
- Actionable information
- Includes severity and time

### Technical Implementation

**1. Transcript Collection:**
```python
# OMI webhook stores transcripts in session
omi_recording_sessions[alert_id]['transcripts'] = [
    "Help me please",
    "Someone is following me",
    "I'm scared"
]
```

**2. Smart Summary Generation:**
```python
def generate_smart_summary(transcripts):
    # Analyze content
    distress_keywords = ['help', 'emergency', 'danger', ...]
    distress_count = count_keywords(transcripts)
    
    # Generate contextual summary
    if distress_count >= 3:
        return "Critical emergency detected..."
    elif distress_count >= 1:
        return "Emergency alert. Distress detected..."
    else:
        return "Alert triggered. User said: ..."
```

**3. Fish Audio TTS:**
```python
def fish_audio_text_to_speech(summary_text):
    response = requests.post(
        "https://api.fish.audio/v1/tts",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "text": summary_text,
            "voice": "professional_female",
            "language": "en",
            "format": "mp3"
        }
    )
    return response.json()['audio_url']
```

**4. Local Playback:**
```python
def play_audio_locally(audio_url):
    urllib.request.urlretrieve(audio_url, "/tmp/summary.mp3")
    os.system("afplay /tmp/summary.mp3 &")  # macOS
```

**5. Auto-Trigger:**
```python
# In OMI webhook handler
if transcript_count % 3 == 0:  # Every 3 transcripts
    summary = generate_smart_summary(transcripts)
    audio_url = fish_audio_text_to_speech(summary)
    play_audio_locally(audio_url)
```

### API Endpoints

**POST /api/fish-audio/summary**
```json
{
  "transcripts": ["Help me", "Emergency", "I need help"],
  "play": true
}

Response:
{
  "summary": "Emergency alert at 3:45 PM...",
  "audio_url": "https://fish.audio/output/abc123.mp3",
  "transcript_count": 3,
  "mode": "production"
}
```

---

## 🚀 Setup Instructions

### Prerequisites
- Arduino R4 WiFi
- OMI Dev Kit 2 (optional but recommended)
- 2 Laptops (or 1 with port forwarding)
- Python 3.9+
- Node.js 18+
- ngrok account (free)

### 1️⃣ **Backend Setup (Main Laptop)**

```bash
cd Guardian_Angel_AI

# Install Python dependencies
pip install flask flask-cors chromadb anthropic requests

# (Optional) Set Fish Audio API key
export FISH_AUDIO_API_KEY="your_key_from_fish.audio"

# Start ngrok tunnel
ngrok http 5000
# Copy the public URL (e.g., https://abc123.ngrok-free.dev)

# Start backend
python3 backend/app.py
```

### 2️⃣ **Frontend Setup (Main Laptop)**

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### 3️⃣ **Arduino Laptop Setup**

```bash
# Edit simple_server_enhanced.py
GUARDIAN_AI_HOST = "abc123.ngrok-free.dev"  # Your ngrok URL

# Start relay server
python3 simple_server_enhanced.py
```

### 4️⃣ **Arduino Configuration**

```cpp
// In GuardianAngel.ino
const char* WIFI_SSID = "Your_WiFi";
const char* WIFI_PASS = "Your_Password";
const char* SERVER_HOST = "192.168.x.x";  // Arduino laptop IP
const uint16_t SERVER_PORT = 5002;

// Upload to Arduino R4 WiFi
```

### 5️⃣ **OMI Configuration**

1. Open OMI mobile app
2. Go to "Plugins" → "Developer" 
3. Add webhook: `https://abc123.ngrok-free.dev/api/omi/webhook?session_id=omi&uid=user1`
4. Enable webhook

---

## 🧪 Testing

### Test Fish Audio Integration
```bash
python3 test_fish_audio.py
```

### Test Arduino Alert
```bash
# Press and hold touch sensor for 3 seconds
# Check dashboard for alert + transcripts
```

### Test API Endpoints
```bash
# Create alert
curl -X POST http://localhost:5000/api/alert \
  -H "Content-Type: application/json" \
  -d '{"description":"Test alert"}'

# Generate Fish Audio summary
curl -X POST http://localhost:5000/api/fish-audio/summary \
  -H "Content-Type: application/json" \
  -d '{"transcripts":["Help","Emergency","Scared"],"play":true}'

# Check system status
curl http://localhost:5000/api/status
```

---

## 🏆 Prize Submission - Best Use of Fish Audio

### Why Guardian Angel Wins:

**1. Creative Use Case ✅**
- Emergency response is critical, life-saving application
- Not just another chatbot or voice assistant
- Real-world impact potential

**2. Technical Excellence ✅**
- Full production-ready integration
- Multi-modal system (IoT + AI + Voice)
- Real-time processing pipeline
- Automatic triggering system

**3. Best Showcase of Fish Audio ✅**
- Natural voice > Robotic alerts (clear advantage)
- Context-aware summaries (shows intelligence)
- Professional emergency voice (appropriate use case)
- Immediate actionable information

**4. Real-World Value ✅**
- Lives could be saved with clearer communication
- Faster emergency response times
- Better outcomes for vulnerable populations
- Scalable to healthcare, senior care, safety devices

### Comparison

| Feature | Traditional TTS | Fish Audio (Ours) |
|---------|----------------|-------------------|
| Voice Quality | Robotic, unclear | Natural, professional |
| Context | Generic "Alert!" | Full situation details |
| Emergency Use | Confusing | Clear, actionable |
| Information | None | Time, severity, keywords |
| User Trust | Low | High (sounds official) |
| Response Speed | Delayed (confusion) | Faster (clear info) |

---

## 📊 Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| Arduino Integration | ✅ Complete | Touch sensor, WiFi, HTTP |
| Alexa Announcements | ✅ Complete | IFTTT webhook integration |
| Real-time Dashboard | ✅ Complete | SSE, live updates, timeline |
| OMI Transcription | ✅ Complete | Real-time audio → text |
| Fish Audio TTS | ✅ Complete | Smart summaries → voice |
| Distress Detection | ✅ Complete | AI keyword + Claude analysis |
| Privacy Protection | ✅ Complete | Auto-stop after resolution |
| Triple-Tap Resolution | ✅ Complete | 3 taps = alert resolved |
| ngrok Tunneling | ✅ Complete | Cross-network communication |
| Event Storage | ✅ Complete | ChromaDB persistence |
| Auto-Processing | ✅ Complete | Fish Audio every 3 transcripts |

---

## 🎯 Key Metrics

- **Response Time:** <100ms dashboard updates
- **Alert Detection:** 3-second hold → instant trigger
- **Transcription:** Real-time (OMI webhook)
- **Summary Generation:** ~1-2 seconds
- **Voice Synthesis:** 2-5 seconds (Fish Audio API)
- **Total Alert-to-Voice:** ~10-15 seconds end-to-end

---

## 💡 Future Enhancements

### Near-Term
- [ ] Multi-language support (Fish Audio supports it!)
- [ ] Voice cloning (user's own voice for authenticity)
- [ ] SMS/email notifications to emergency contacts
- [ ] GPS location integration
- [ ] Fall detection with accelerometer

### Long-Term
- [ ] Mobile app for emergency contacts
- [ ] Integration with 911 dispatch systems
- [ ] Wearable hardware (beyond OMI)
- [ ] AI video analysis (camera integration)
- [ ] Healthcare monitoring (heart rate, vitals)
- [ ] Senior care facility deployment

---

## 🌟 Use Cases

### 1. **Elderly Care**
- Fall detection + voice summaries
- Caregiver dashboard monitoring
- Clear emergency communication

### 2. **Personal Safety**
- Walking alone at night
- Instant help with context
- Emergency contacts notified

### 3. **Healthcare Monitoring**
- Patient distress detection
- Nurse station alerts
- Context-aware summaries

### 4. **Home Security**
- Intrusion alerts
- Situation assessment
- Emergency response coordination

---

## 👥 Team & Acknowledgments

**Built at Cal Hacks 2025**

### Technologies Used
- Arduino R4 WiFi
- OMI Dev Kit 2
- Fish Audio TTS API
- ChromaDB
- Flask & React
- ngrok
- IFTTT

### Special Thanks
- Fish Audio for TTS API
- OMI for Dev Kit 2
- Cal Hacks organizers

---

## 📞 Contact & Links

**GitHub:** [Your GitHub Repository]  
**Demo Video:** [Your Demo Link]  
**Live Dashboard:** http://localhost:5173  
**API Documentation:** http://localhost:5000/

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🎉 Conclusion

**Guardian Angel AI** demonstrates the power of combining IoT hardware, wearable AI, and intelligent voice synthesis to create a life-saving emergency response system. 

By using **Fish Audio's natural TTS**, we've transformed robotic "Alert!" messages into clear, context-aware emergency communications that can save lives.

**This is more than a hackathon project - it's a platform that could protect vulnerable populations worldwide.** 🌍🛡️

---

**Built with ❤️ for Cal Hacks 2025**
