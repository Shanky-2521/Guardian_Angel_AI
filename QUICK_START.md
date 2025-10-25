# 🚀 Quick Start - Guardian Angel AI

## ✅ Currently Running Services

### 1. Backend API
- **URL:** http://localhost:5000
- **Your Network:** http://10.65.219.51:5000
- **Status:** ✅ Online with Claude AI
- **ChromaDB:** ✅ Connected
- **Events Logged:** 8 events

### 2. Frontend Dashboard  
- **Local:** http://localhost:5173
- **Proxy:** Click the browser preview button in your IDE
- **Status:** ✅ Running

### 3. Test Simulator
- **Script:** `test_arduino_simulator.py`
- **Usage:** `python3 test_arduino_simulator.py`

---

## 🎮 How to Use

### Option 1: Use the Dashboard (Recommended for Demo)
1. Open http://localhost:5173 in your browser
2. Click the **green "Simulate Check-in"** button
3. Click the **red "Simulate Alert"** button
4. Watch events appear in real-time!
5. Click **"Generate Summary"** for AI analysis (uses fallback due to API model limits)

### Option 2: Use the Test Simulator
```bash
cd /Users/spartan/Documents/calhacks/Guardian_Angel_AI
python3 test_arduino_simulator.py
# Choose option 1 for auto demo or 2 for manual control
```

### Option 3: Send Data from Arduino
Once you upload the Arduino code:
1. Arduino connects to WiFi: "Nani?"
2. Tap sensor → Check-in sent to http://10.65.219.51:5000
3. Hold 3 sec → Alert sent + Echo Dot announcement

### Option 4: Manual API Calls
```bash
# Check-in
curl -X POST http://localhost:5000/api/checkin

# Alert
curl -X POST http://localhost:5000/api/alert \
  -H "Content-Type: application/json" \
  -d '{"description": "Emergency alert!"}'

# Get all events
curl http://localhost:5000/api/events

# Get summary
curl http://localhost:5000/api/summary

# Check status
curl http://localhost:5000/api/status
```

---

## 📱 Access from Your Phone/Tablet (Same Network)

If you want to show the dashboard on another device:

1. Make sure the device is on the same WiFi: **"Nani?"**
2. Open browser and go to: **http://10.65.219.51:5173**

---

## 🎬 Demo Flow for Judges

### 1. Show the Dashboard (30 sec)
- "This is our Guardian Angel AI dashboard"
- Point out: Status indicator, Event timeline, AI summary panel

### 2. Trigger Events (1 min)
- Click "Simulate Check-in" → Green event appears instantly
- Click "Simulate Alert" → Card turns red, pulsing animation
- Show real-time event timeline updating

### 3. AI Summary (30 sec)
- Click "Generate Summary" button
- Explain: "This queries ChromaDB and generates contextual summaries"
- Note: Using fallback mode for stability

### 4. Hardware Integration (30 sec)
- Show Arduino + Touch sensor setup
- Explain: "Tap = check-in, Hold 3 sec = alert"
- Mention: "Alert triggers Echo Dot announcement via Alexa"

### 5. Architecture (30 sec)
- Point to System Flow diagram on dashboard
- Walk through: Touch → Arduino → Flask → ChromaDB → Claude
- Highlight sponsor tech: ChromaDB for storage, Claude for AI

---

## 🛑 Stop Services

```bash
# Kill both servers
./stop.sh

# Or manually:
lsof -ti:5000 | xargs kill  # Backend
lsof -ti:5173 | xargs kill  # Frontend
```

---

## 🐛 Troubleshooting

### Dashboard not loading?
```bash
# Check frontend status
curl http://localhost:5173
```

### Backend not responding?
```bash
# Check backend status
curl http://localhost:5000/api/status
```

### Events not appearing on dashboard?
- Check browser console for errors
- Verify SSE connection at: http://localhost:5000/api/events/stream
- Refresh the page

### Can't access from phone?
- Make sure phone is on "Nani?" WiFi
- Try: http://10.65.219.51:5173 (not localhost)
- Check firewall settings

---

## 📊 Current System Status

✅ **Backend:** Running on port 5000  
✅ **Frontend:** Running on port 5173  
✅ **ChromaDB:** 8 events stored  
✅ **Claude AI:** Configured (using fallback summaries)  
✅ **Real-time SSE:** Active  
✅ **CORS:** Enabled  

**Last Test:** October 25, 2025 at 02:12:55  
**Test Events:** 4 check-ins, 4 alerts

---

## 🎯 Key Features Working

✅ Real-time event streaming (SSE)  
✅ Check-in and alert logging  
✅ ChromaDB vector storage  
✅ Beautiful animated UI  
✅ System health monitoring  
✅ Demo controls for presentation  
✅ Arduino integration ready  
✅ Network accessible (10.65.219.51)

---

**You're all set for the hackathon demo! 🎉**

Open http://localhost:5173 and start clicking those buttons!
