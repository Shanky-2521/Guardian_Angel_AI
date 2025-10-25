from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import chromadb
from datetime import datetime
import json
import time
import queue
import threading
import os
import requests as http_requests
from anthropic import Anthropic

app = Flask(__name__)
CORS(app)

# Initialize ChromaDB
chroma_client = chromadb.Client()
try:
    collection = chroma_client.get_collection(name="guardian_events")
except:
    collection = chroma_client.create_collection(name="guardian_events")

# SSE queue for real-time updates
event_queues = []
event_queues_lock = threading.Lock()

# OMI recording state (for real-time audio streaming)
omi_recording_sessions = {}
omi_recording_lock = threading.Lock()

# Check-in tap tracking (for triple-tap to resolve alert)
checkin_taps = {}
checkin_lock = threading.Lock()
CHECKIN_WINDOW_SECONDS = 5  # Must tap 3 times within 5 seconds

# IFTTT Webhook Configuration (for Alexa announcements)
IFTTT_WEBHOOK_KEY = os.getenv('IFTTT_WEBHOOK_KEY', 'kouHpRJ7j7LW7l-ssgtTToG7d2Il0zPpjygqNRuDubW')
IFTTT_EVENT_NAME = 'guardian_alert'

# Claude client (optional - will work without API key)
claude_client = None
if os.getenv('ANTHROPIC_API_KEY'):
    claude_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def broadcast_event(event_data):
    """Broadcast event to all connected SSE clients"""
    with event_queues_lock:
        for q in event_queues:
            try:
                q.put(event_data)
            except:
                pass

def trigger_alexa_announcement(alert_type="alert", message=""):
    """
    Trigger Alexa announcement via IFTTT webhook
    Integrated with original Arduino-Alexa system
    """
    try:
        url = f"https://maker.ifttt.com/trigger/{IFTTT_EVENT_NAME}/with/key/{IFTTT_WEBHOOK_KEY}"
        payload = {
            "value1": "Guardian Angel Alert" if alert_type == "alert" else "Guardian Angel Check-in",
            "value2": datetime.now().isoformat() + 'Z',
            "value3": message or "Emergency assistance needed"
        }
        
        print(f"🔊 Triggering Alexa announcement: {alert_type}")
        response = http_requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Alexa announcement sent successfully")
            return {
                'success': True,
                'status': 'sent',
                'message': 'Alexa announcement triggered'
            }
        else:
            print(f"⚠️  Alexa announcement failed: {response.status_code}")
            return {
                'success': False,
                'status': 'failed',
                'message': f'IFTTT returned {response.status_code}'
            }
    except Exception as e:
        print(f"❌ Alexa announcement error: {e}")
        return {
            'success': False,
            'status': 'error',
            'message': str(e)
        }

def trigger_omi_recording(event_id, description):
    """
    Trigger OMI Dev Kit 2 to start recording audio during emergency
    
    OMI Integration Options:
    1. OMI App API - If OMI exposes webhook/API
    2. OMI Friend Plugin - Custom plugin for Guardian Angel
    3. Manual trigger via OMI app
    
    For demo: Returns success status
    For production: Integrate with OMI API once available
    """
    omi_config = {
        'enabled': os.getenv('OMI_ENABLED', 'false').lower() == 'true',
        'api_url': os.getenv('OMI_API_URL', 'http://localhost:8000/omi'),
        'api_key': os.getenv('OMI_API_KEY', ''),
        'recording_duration': int(os.getenv('OMI_RECORDING_DURATION', '30'))  # 30 seconds default
    }
    
    if not omi_config['enabled']:
        # Demo mode - simulate OMI activation
        return {
            'success': True,
            'status': 'simulated',
            'message': 'OMI recording would be triggered (demo mode)',
            'recording_duration': omi_config['recording_duration']
        }
    
    try:
        # Actual OMI API integration
        omi_request = {
            'action': 'start_recording',
            'event_id': event_id,
            'trigger': 'guardian_angel_alert',
            'description': description,
            'duration': omi_config['recording_duration'],
            'metadata': {
                'priority': 'emergency',
                'auto_analyze': True
            }
        }
        
        response = http_requests.post(
            omi_config['api_url'],
            json=omi_request,
            headers={'Authorization': f"Bearer {omi_config['api_key']}"},
            timeout=5
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'status': 'activated',
                'message': 'OMI recording started',
                'recording_id': response.json().get('recording_id'),
                'recording_duration': omi_config['recording_duration']
            }
        else:
            return {
                'success': False,
                'status': 'error',
                'message': f'OMI API error: {response.status_code}'
            }
            
    except Exception as e:
        print(f"OMI activation error: {e}")
        return {
            'success': False,
            'status': 'error',
            'message': str(e)
        }

@app.route('/api/checkin', methods=['POST'])
def checkin():
    """Log a check-in event - Triple tap resolves active alert"""
    timestamp = datetime.now()
    timestamp_iso = timestamp.isoformat()
    event_id = f"checkin_{int(time.time() * 1000)}"
    current_time = time.time()
    
    # Track check-in taps (for triple-tap to resolve alert)
    user_id = request.json.get('user_id', 'default_user') if request.json else 'default_user'
    
    with checkin_lock:
        if user_id not in checkin_taps:
            checkin_taps[user_id] = []
        
        # Add current tap
        checkin_taps[user_id].append(current_time)
        
        # Remove taps older than CHECKIN_WINDOW_SECONDS
        checkin_taps[user_id] = [
            tap_time for tap_time in checkin_taps[user_id]
            if current_time - tap_time <= CHECKIN_WINDOW_SECONDS
        ]
        
        tap_count = len(checkin_taps[user_id])
    
    # Check if there's an active alert to resolve
    active_alert = None
    with omi_recording_lock:
        for alert_id, session_data in omi_recording_sessions.items():
            if session_data.get('active', False):
                active_alert = alert_id
                break
    
    # If 3 taps within window AND there's an active alert, auto-resolve it
    alert_resolved = False
    if tap_count >= 3 and active_alert:
        with omi_recording_lock:
            if active_alert in omi_recording_sessions:
                omi_recording_sessions[active_alert]['active'] = False
                omi_recording_sessions[active_alert]['ended_at'] = timestamp_iso
                print(f"🔒 OMI session {active_alert} deactivated - privacy protection enabled")
        alert_resolved = True
        print(f"🎉 TRIPLE TAP DETECTED! Alert {active_alert} auto-resolved")
        
        # Clear tap history after resolution
        with checkin_lock:
            checkin_taps[user_id] = []
        
        # Broadcast alert resolution
        broadcast_event({
            "type": "alert_resolved",
            "timestamp": timestamp_iso,
            "message": "Alert resolved via triple check-in",
            "alert_id": active_alert,
            "id": f"resolution_{int(time.time() * 1000)}"
        })
    
    # Store check-in in ChromaDB
    collection.add(
        documents=[json.dumps({
            "type": "checkin",
            "timestamp": timestamp_iso,
            "message": "User checked in successfully",
            "tap_count": tap_count,
            "alert_resolved": alert_resolved
        })],
        ids=[event_id],
        metadatas=[{"type": "checkin", "timestamp": timestamp_iso}]
    )
    
    # Broadcast check-in to SSE clients
    event_data = {
        "type": "checkin",
        "timestamp": timestamp_iso,
        "message": f"Check-in {tap_count}/3" if active_alert else "User checked in successfully",
        "id": event_id,
        "tap_count": tap_count,
        "alert_resolved": alert_resolved,
        "active_alert": active_alert is not None
    }
    broadcast_event(event_data)
    
    if alert_resolved:
        print(f"[{timestamp_iso}] Check-in #{tap_count} - Alert RESOLVED")
    elif active_alert:
        print(f"[{timestamp_iso}] Check-in #{tap_count}/3 (need {3 - tap_count} more to resolve alert)")
    else:
        print(f"[{timestamp_iso}] Check-in received")
    
    return jsonify({
        "status": "success",
        "event": event_data,
        "tap_count": tap_count,
        "alert_resolved": alert_resolved,
        "taps_needed": max(0, 3 - tap_count) if active_alert else 0
    }), 200

@app.route('/api/alert', methods=['POST'])
def alert():
    """Log an alert event and trigger OMI recording"""
    timestamp = datetime.now().isoformat()
    event_id = f"alert_{int(time.time() * 1000)}"
    data = request.json or {}
    description = data.get('description', 'Emergency alert triggered')
    
    # Store in ChromaDB
    collection.add(
        documents=[json.dumps({
            "type": "alert",
            "timestamp": timestamp,
            "message": description
        })],
        ids=[event_id],
        metadatas=[{"type": "alert", "timestamp": timestamp}]
    )
    
    # Activate OMI recording session (for continuous audio streaming)
    with omi_recording_lock:
        omi_recording_sessions[event_id] = {
            'started_at': timestamp,
            'alert_description': description,
            'active': True,
            'transcripts': []
        }
    
    # Trigger OMI recording (legacy support)
    omi_response = trigger_omi_recording(event_id, description)
    
    # Broadcast to SSE clients FIRST (for instant dashboard update)
    event_data = {
        "type": "alert",
        "timestamp": timestamp,
        "message": description,
        "id": event_id,
        "omi_activated": True,
        "omi_session": event_id,
        "alexa_announced": True  # Will be triggered async
    }
    broadcast_event(event_data)
    
    print(f"[{timestamp}] ALERT received: {description}")
    print(f"[{timestamp}] OMI recording: {omi_response.get('status', 'failed')}")
    
    # Trigger Alexa announcement in background (non-blocking)
    def trigger_alexa_async():
        alexa_response = trigger_alexa_announcement(alert_type="alert", message=description)
        print(f"[{timestamp}] Alexa announcement: {alexa_response.get('status', 'failed')}")
    
    threading.Thread(target=trigger_alexa_async, daemon=True).start()
    
    return jsonify({
        "status": "success",
        "event": event_data,
        "omi": omi_response,
        "alexa": {"status": "sending", "message": "Triggered in background"}
    }), 200

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events from ChromaDB"""
    try:
        results = collection.get()
        events = []
        
        if results['ids']:
            for i, doc_id in enumerate(results['ids']):
                doc_data = json.loads(results['documents'][i])
                events.append({
                    "id": doc_id,
                    **doc_data
                })
        
        # Sort by timestamp descending
        events.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return jsonify({"events": events}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Generate AI summary using intelligent analysis"""
    try:
        # Get recent events
        results = collection.get()
        events = []
        
        if results['ids']:
            for i, doc_id in enumerate(results['ids']):
                doc_data = json.loads(results['documents'][i])
                events.append(doc_data)
        
        # Sort by timestamp
        events.sort(key=lambda x: x.get('timestamp', ''))
        recent_events = events[-10:]  # Last 10 events
        
        if not recent_events:
            return jsonify({
                "summary": "No events recorded yet. The Guardian Angel system is standing by and ready to monitor safety status."
            }), 200
        
        # Generate intelligent summary
        checkin_count = sum(1 for e in recent_events if e['type'] == 'checkin')
        alert_count = sum(1 for e in recent_events if e['type'] == 'alert')
        last_event = recent_events[-1]
        total_events = len(events)
        
        # Calculate time since last event
        from datetime import datetime
        try:
            last_time = datetime.fromisoformat(last_event['timestamp'])
            time_ago = (datetime.now() - last_time).seconds
            if time_ago < 60:
                time_str = f"{time_ago} seconds ago"
            elif time_ago < 3600:
                time_str = f"{time_ago // 60} minutes ago"
            else:
                time_str = f"{time_ago // 3600} hours ago"
        except:
            time_str = "recently"
        
        # Build contextual summary
        if alert_count > checkin_count:
            status = "⚠️ HIGH ALERT"
            summary = f"{status}: System has detected {alert_count} alerts and {checkin_count} check-ins in recent activity. "
            summary += f"Last event was an {last_event['type']} {time_str}. "
            summary += "Immediate attention recommended. Emergency protocols may be active."
        elif alert_count > 0:
            status = "🔔 MONITORING"
            summary = f"{status}: Guardian Angel has logged {total_events} total events with {alert_count} alerts requiring review. "
            summary += f"User last checked in {time_str}. "
            summary += "System is actively monitoring for concerning patterns."
        else:
            status = "✅ NORMAL"
            summary = f"{status}: All systems operating normally with {checkin_count} successful check-ins recorded. "
            summary += f"Last activity was {time_str}. "
            summary += "No alerts detected. User appears safe and responsive."
        
        # Add recent event context
        if alert_count > 0:
            alert_messages = [e.get('message', '') for e in recent_events if e['type'] == 'alert']
            if alert_messages:
                summary += f" Recent alerts include: {alert_messages[-1]}"
        
        return jsonify({"summary": summary, "status": status}), 200
        
    except Exception as e:
        print(f"Summary error: {e}")
        return jsonify({"summary": "System is operational and monitoring safety events."}), 200

@app.route('/api/events/stream')
def event_stream():
    """Server-Sent Events endpoint for real-time updates"""
    def generate():
        q = queue.Queue()
        with event_queues_lock:
            event_queues.append(q)
        
        try:
            while True:
                try:
                    event = q.get(timeout=30)
                    yield f"data: {json.dumps(event)}\n\n"
                except queue.Empty:
                    # Send keep-alive ping
                    yield f": ping\n\n"
        finally:
            with event_queues_lock:
                event_queues.remove(q)
    
    # Prevent buffering for instant event delivery
    response = Response(generate(), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    return response

@app.route('/api/status', methods=['GET'])
def status():
    """Check system status"""
    try:
        results = collection.get()
        event_count = len(results['ids']) if results['ids'] else 0
        
        return jsonify({
            "status": "online",
            "total_events": event_count,
            "chroma_connected": True,
            "claude_available": claude_client is not None
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/omi/webhook', methods=['POST'])
def omi_webhook():
    """
    OMI Real-Time Transcript Processor Webhook
    Receives live transcripts during Guardian Angel alerts
    """
    try:
        # Get query parameters
        session_id = request.args.get('session_id')
        uid = request.args.get('uid')
        
        # Check if there's an active alert session FIRST (before any processing)
        active_session = None
        with omi_recording_lock:
            for session_id, session_data in omi_recording_sessions.items():
                if session_data.get('active', False):
                    active_session = session_id
                    break
        
        # If NO active alert, silently ignore and return success
        if not active_session:
            print(f"🔒 OMI webhook received but NO ACTIVE alert - transcript BLOCKED (privacy protection)")
            return jsonify({"status": "ok", "message": "No active alert - privacy protected"}), 200
        
        # Only if there's an ACTIVE ALERT, then process the transcript
        print(f"\n{'='*50}")
        print(f"🎤 OMI WEBHOOK - ACTIVE ALERT SESSION")
        print(f"Alert Session ID: {active_session}")
        print(f"UID: {uid}")
        print(f"{'='*50}\n")
        
        # Get transcript segments from body
        try:
            data = request.get_json(force=True) or []
            
            # OMI sends {"segments": [...]} format
            if isinstance(data, dict) and 'segments' in data:
                segments = data['segments']
            elif isinstance(data, list):
                segments = data
            elif isinstance(data, dict):
                segments = [data]
            else:
                segments = []
                
            print(f"Parsed {len(segments)} segments")
        except Exception as e:
            print(f"JSON parse error: {e}")
            segments = []
        
        timestamp = datetime.now().isoformat()
        distress_detected = False
        
        # Process transcript segments
        if segments and len(segments) > 0:
            # Combine recent segments into text
            transcript_text = " ".join([seg.get('text', '') for seg in segments])
            
            # Only process if we have actual text
            if transcript_text.strip():
                print(f"📝 Transcript: {transcript_text}")
                
                # Detect distress keywords
                distress_keywords = [
                    'help', 'emergency', 'fall', 'hurt', 'pain', 'scared', 'danger', 'fell',
                    'call 911', 'call police', 'call ambulance', 'cant move', "can't move",
                    'bleeding', 'attack', 'fire', 'smoke', 'intruder', 'chest pain',
                    'cant breathe', "can't breathe", 'stroke', 'heart attack'
                ]
                
                # Negative context words (suggests person is okay)
                negative_context = ["don't", "dont", "no need", "im fine", "im okay", "just kidding"]
                
                # Check for distress keywords
                has_distress_keyword = any(keyword in transcript_text.lower() for keyword in distress_keywords)
                
                # Check for negative context
                has_negative = any(neg in transcript_text.lower() for neg in negative_context)
                
                # Only flag as distress if we have keywords but no negative context
                distress_detected = has_distress_keyword and not has_negative
                
                # Optional: Use AI for smarter detection (if Claude available and transcript is ambiguous)
                ai_distress_level = None
                if claude_client and len(transcript_text) > 20:
                    try:
                        # Only use AI if keyword detection is uncertain
                        message = claude_client.messages.create(
                            model="claude-3-sonnet-20240229",
                            max_tokens=50,
                            messages=[{
                                "role": "user",
                                "content": f"Is this person in distress or danger? Answer only 'YES' or 'NO': \"{transcript_text}\""
                            }]
                        )
                        ai_response = message.content[0].text.strip().upper()
                        if 'YES' in ai_response:
                            ai_distress_level = 'high'
                            distress_detected = True  # AI override
                        print(f"🤖 AI Analysis: {ai_response}")
                    except Exception as e:
                        print(f"AI analysis skipped: {e}")
                
                if distress_detected:
                    print(f"⚠️  DISTRESS DETECTED! (Keywords: {has_distress_keyword}, AI: {ai_distress_level or 'N/A'})")
                else:
                    print(f"✓ Normal speech detected")
                
                # Store transcript in ChromaDB
                event_id = f"omi_transcript_{int(time.time() * 1000)}"
                collection.add(
                    documents=[json.dumps({
                        "type": "omi_transcript",
                        "timestamp": timestamp,
                        "session_id": session_id,
                        "uid": uid,
                        "transcript": transcript_text,
                        "distress_detected": distress_detected,
                        "segment_count": len(segments)
                    })],
                    ids=[event_id],
                    metadatas={"type": "omi_transcript", "timestamp": timestamp, "distress": str(distress_detected)}
                )
                
                # If distress detected, auto-escalate
                if distress_detected:
                    print(f"⚠️  DISTRESS DETECTED in OMI transcript: {transcript_text}")
                    # Could trigger additional alert here
                
                # Broadcast to SSE for dashboard (only if we have text)
                broadcast_event({
                    "type": "omi_transcript",
                    "timestamp": timestamp,
                    "transcript": transcript_text,
                    "distress_detected": distress_detected,
                    "session_id": session_id,
                    "uid": uid,
                    "id": event_id
                })
                
                print(f"[{timestamp}] OMI Transcript: {transcript_text[:50]}...")
            else:
                print(f"Empty transcript text, skipping...")
        else:
            print(f"No segments received, skipping...")
            
        return jsonify({
            "status": "success",
            "segments_processed": len(segments),
            "distress_detected": distress_detected
        }), 200
        
    except Exception as e:
        print(f"OMI webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/alert/resolve/<alert_id>', methods=['POST'])
def resolve_alert(alert_id):
    """Stop OMI recording session for resolved alert"""
    with omi_recording_lock:
        if alert_id in omi_recording_sessions:
            omi_recording_sessions[alert_id]['active'] = False
            omi_recording_sessions[alert_id]['ended_at'] = datetime.now().isoformat()
            print(f"⏹️  OMI recording session stopped for alert: {alert_id}")
            return jsonify({"status": "success", "message": "OMI recording stopped"}), 200
        else:
            return jsonify({"status": "error", "message": "Alert session not found"}), 404

@app.route('/')
def index():
    return jsonify({
        "service": "Guardian Angel AI Backend",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/checkin": "Log check-in event",
            "POST /api/alert": "Log alert event (activates OMI session)",
            "POST /api/alert/resolve/<id>": "Stop OMI recording session",
            "POST /api/omi/webhook": "OMI real-time transcript webhook",
            "GET /api/events": "Get all events",
            "GET /api/summary": "Get AI summary",
            "GET /api/events/stream": "SSE real-time events",
            "GET /api/status": "System status"
        }
    })

if __name__ == '__main__':
    print("🛡️  Guardian Angel Backend Starting...")
    print("📍 Server: http://localhost:5000")
    print("🔄 SSE Stream: http://localhost:5000/api/events/stream")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
