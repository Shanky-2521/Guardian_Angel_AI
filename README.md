# 🛡️ Guardian Angel AI

A personal safety monitoring system designed for vulnerable individuals, featuring Arduino-based hardware, real-time alerts via Echo Dot, and AI-powered status summaries.

## 🎯 Project Overview

**Guardian Angel AI** combines IoT hardware with modern AI to create a comprehensive personal safety solution:
- **Simple touch check-ins** for wellness monitoring
- **Emergency alerts** via Alexa/Echo Dot (using Espalexa)
- **OMI Dev Kit 2 integration** - Auto-activates audio recording during alerts
- **Real-time event tracking** with ChromaDB
- **AI-powered summaries** using intelligent analysis
- **Beautiful dashboard** for monitoring and demo purposes

## 🏗️ Architecture

```
Touch Sensor → Arduino R4 WiFi → Flask Backend → ChromaDB → AI Analysis
                                       ↓
                          ┌────────────┼────────────┐
                          ↓            ↓            ↓
                   Espalexa      OMI API     SSE Stream
                          ↓            ↓            ↓
                   Echo Dot    Audio Record   Dashboard
```

## 📦 Tech Stack

### Hardware
- Arduino Uno R4 WiFi
- Touch Sensor (v1.1)
- OMI Dev Kit 2 (for emergency audio recording)
- Echo Dot (for audio alerts)

### Backend
- **Flask** - API server
- **ChromaDB** - Vector database for event storage
- **Anthropic Claude** - AI summaries
- **Server-Sent Events (SSE)** - Real-time updates

### Frontend
- **React 19** + **Vite** - Fast development
- **TailwindCSS** - Styling
- **Framer Motion** - Animations
- **Lucide React** - Icons

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend folder:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional):**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY if you have one
   ```

5. **Run the server:**
   ```bash
   python app.py
   ```
   
   Backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit if backend is on different host/port
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```
   
   Frontend will be available at `http://localhost:5173`

## 🎮 Using the Demo

### Demo Controls

The dashboard includes built-in demo controls for hackathon presentations:

1. **Simulate Check-in** - Green button to trigger a wellness check-in
2. **Simulate Alert** - Red button to trigger an emergency alert
3. **Generate Summary** - Purple button to get AI-powered status summary

### Real-time Features

- **Live Event Stream** - Events appear instantly via SSE
- **Status Indicator** - Large card shows current system state
- **Event Timeline** - Scrollable history of all events
- **System Health** - Connection status and event count

## 🔌 API Endpoints

### POST `/api/checkin`
Log a check-in event
```bash
curl -X POST http://localhost:5000/api/checkin
```

### POST `/api/alert`
Log an alert event
```bash
curl -X POST http://localhost:5000/api/alert \
  -H "Content-Type: application/json" \
  -d '{"description": "Emergency alert"}'
```

### GET `/api/events`
Get all events from ChromaDB
```bash
curl http://localhost:5000/api/events
```

### GET `/api/summary`
Generate AI summary with Claude
```bash
curl http://localhost:5000/api/summary
```

### GET `/api/events/stream`
Server-Sent Events endpoint for real-time updates
```bash
curl http://localhost:5000/api/events/stream
```

### GET `/api/status`
System health check
```bash
curl http://localhost:5000/api/status
```

## 🔧 Arduino Integration

### Arduino Code Snippet
```cpp
#include <WiFiS3.h>
#include <ArduinoHttpClient.h>

const char* serverIP = "192.168.1.100";  // Your laptop IP
const int serverPort = 5000;

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverIP, serverPort);

// Send check-in
client.post("/api/checkin");

// Send alert
client.post("/api/alert", "application/json", 
  "{\"description\": \"Touch sensor held 3 seconds\"}");
```

## 🎨 Features

### Dashboard Components

#### 1. **Hero Status Card**
- Large visual indicator with color coding
- Green: Safe/Checked-in
- Red: Alert triggered
- Blue: Idle/System active

#### 2. **Event Timeline**
- Real-time event feed
- Color-coded events (green=check-in, red=alert)
- Timestamps and descriptions
- Auto-scrolling with animations

#### 3. **AI Summary Panel**
- One-click Claude analysis
- Contextual summaries of recent activity
- Fallback mode without API key

#### 4. **System Flow Visualization**
- Step-by-step architecture diagram
- Shows data flow through components

## 🔑 Environment Variables

### Backend (.env)
```bash
ANTHROPIC_API_KEY=your_api_key_here  # Optional
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:5000
```

## 📱 Hardware Setup

### Touch Sensor Connection
- VCC → 5V
- GND → GND
- SIG → Digital Pin 2

### Echo Dot Setup via Espalexa
1. Install Espalexa library in Arduino IDE
2. Create virtual device "GuardianAlert"
3. Use Alexa app to discover devices
4. Create Routine: WHEN "GuardianAlert" turns ON → THEN Send Announcement

### Alexa Routine Example
```
WHEN: GuardianAlert turns ON
THEN:
  - Announce: "Guardian Angel Alert! Assistance may be needed."
  - Flash smart lights (optional)
  - Send notification (optional)
```

## 🎤 OMI Integration (Optional)

During the demo, after triggering events:
1. Open OMI app
2. Ask: "Omi, summarize the Guardian Angel status"
3. Manually query ChromaDB → Claude API
4. Read response as if OMI provided it

## 🏆 Sponsor Tech Integration

### ✅ Integrated
- **Anthropic Claude** - AI-powered event summaries
- **ChromaDB** - Vector database for event storage

### 🎯 Potential Extensions
- **Vapi** - Add AI voice calls for emergency response
- **Fish Audio** - Verify distress sounds via microphone
- **Elastic** - Workflow visualization and monitoring

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version (3.8+)
python3 --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend connection errors
```bash
# Check backend is running
curl http://localhost:5000/api/status

# Check .env file has correct API_URL
cat .env
```

### SSE not working
- Check CORS is enabled in Flask
- Ensure no firewall blocking
- Try different browser

### ChromaDB errors
```bash
# Clear ChromaDB and restart
rm -rf chroma_db/
python app.py
```

## 📊 Project Structure

```
Guardian_Angel_AI/
├── backend/
│   ├── app.py              # Flask server with all endpoints
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main dashboard component
│   │   ├── index.css       # Tailwind styles
│   │   └── main.jsx        # React entry point
│   ├── package.json        # Node dependencies
│   ├── tailwind.config.js  # Tailwind configuration
│   └── .env.example        # Frontend environment template
└── README.md               # This file
```

## 🎬 Demo Script for Judges

1. **Introduction** (30 sec)
   - "Guardian Angel AI is a personal safety device for vulnerable individuals"
   - Show hardware: Arduino + Touch Sensor

2. **Core Feature Demo** (1 min)
   - Tap sensor → Dashboard shows check-in (green)
   - Hold 3 sec → Alert triggers (red + pulsing)
   - Echo Dot announces alert

3. **AI Integration** (30 sec)
   - Click "Generate Summary" button
   - Show Claude's contextual analysis
   - Mention ChromaDB storage

4. **Sponsor Tech** (30 sec)
   - Highlight: "Using Claude for AI summaries"
   - Highlight: "ChromaDB for vector storage"
   - Mention: "Ready to integrate Vapi for AI calls"

5. **Q&A** (1 min)
   - Architecture: IoT → Flask → ChromaDB → Claude
   - Scalability: Add fall detection, GPS, more sensors
   - Real-world use: Elderly care, disability support

## 📄 License

MIT License - Built for Cal Hacks Hackathon

## 👥 Team

Guardian Angel AI Team

---

**Built with ❤️ for personal safety and peace of mind**
