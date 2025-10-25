"""
Guardian Angel - OMI Recording Control Plugin

This would be deployed as an OMI App that:
1. Listens for Guardian Angel alerts
2. Triggers OMI to start/stop recording
3. Sends transcripts back to Guardian Angel

Note: This is a conceptual implementation for Cal Hacks.
Actual OMI plugin deployment requires following their app submission process.
"""

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# OMI App Configuration
OMI_APP_ID = os.getenv('OMI_APP_ID', 'guardian_angel')
GUARDIAN_ANGEL_BACKEND = os.getenv('GUARDIAN_ANGEL_BACKEND', 'http://localhost:5000')

# Recording state
recording_state = {
    'active': False,
    'session_id': None,
    'started_at': None
}

@app.route('/omi/control/start', methods=['POST'])
def start_recording():
    """
    Called by Guardian Angel when alert is triggered
    This would signal OMI to start recording
    """
    data = request.json or {}
    alert_id = data.get('alert_id')
    
    # In actual implementation, this would use OMI's internal API
    # to trigger recording. For now, we document the flow.
    
    recording_state['active'] = True
    recording_state['session_id'] = alert_id
    recording_state['started_at'] = data.get('timestamp')
    
    print(f"🎤 OMI Recording STARTED for alert: {alert_id}")
    
    # Response that OMI app would send
    return jsonify({
        'status': 'recording_started',
        'session_id': alert_id,
        'message': 'OMI is now capturing audio for emergency analysis'
    }), 200

@app.route('/omi/control/stop', methods=['POST'])
def stop_recording():
    """
    Called by Guardian Angel when situation is resolved
    This would signal OMI to stop recording
    """
    data = request.json or {}
    
    recording_state['active'] = False
    session_id = recording_state['session_id']
    
    print(f"⏹️  OMI Recording STOPPED for session: {session_id}")
    
    # Clear state
    recording_state['session_id'] = None
    
    return jsonify({
        'status': 'recording_stopped',
        'session_id': session_id,
        'message': 'OMI recording has been stopped'
    }), 200

@app.route('/omi/status', methods=['GET'])
def get_status():
    """Check current recording status"""
    return jsonify({
        'recording': recording_state['active'],
        'session_id': recording_state['session_id'],
        'started_at': recording_state['started_at']
    }), 200

@app.route('/omi/transcript', methods=['POST'])
def receive_transcript():
    """
    Receives transcripts from OMI and forwards to Guardian Angel
    This is called by OMI during recording
    """
    segments = request.json or []
    
    if recording_state['active']:
        # Forward to Guardian Angel webhook
        try:
            response = requests.post(
                f"{GUARDIAN_ANGEL_BACKEND}/api/omi/webhook",
                json={'segments': segments},
                params={
                    'session_id': recording_state['session_id'],
                    'uid': 'guardian_angel_controlled'
                }
            )
            print(f"✓ Forwarded {len(segments)} segments to Guardian Angel")
            return jsonify({'status': 'forwarded'}), 200
        except Exception as e:
            print(f"Error forwarding to Guardian Angel: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return jsonify({'status': 'not_recording'}), 200

if __name__ == '__main__':
    print("🛡️ Guardian Angel - OMI Control Plugin")
    print("📍 Listening on http://localhost:8001")
    app.run(host='0.0.0.0', port=8001, debug=True)
