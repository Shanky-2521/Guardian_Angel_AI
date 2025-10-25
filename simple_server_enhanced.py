#!/usr/bin/env python3
"""
Enhanced Guardian Angel server - forwards to both Alexa AND Guardian Angel AI
"""
from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# IFTTT Configuration
IFTTT_WEBHOOK_KEY = "kouHpRJ7j7LW7l-ssgtTToG7d2Il0zPpjygqNRuDubW"
IFTTT_EVENT_NAME = "guardian_alert"

# Guardian Angel AI Backend Configuration
# Connected to Guardian Angel AI Backend on other laptop
GUARDIAN_AI_HOST = "10.65.219.51"  # Your other laptop's IP
GUARDIAN_AI_PORT = 5000

@app.route('/alert', methods=['POST'])
def alert():
    print("ALERT RECEIVED!")
    
    # 1. Send IFTTT webhook (for Alexa)
    webhook_url = f"https://maker.ifttt.com/trigger/{IFTTT_EVENT_NAME}/with/key/{IFTTT_WEBHOOK_KEY}"
    webhook_payload = {
        "value1": "Guardian Angel Alert",
        "value2": datetime.utcnow().isoformat() + 'Z',
        "value3": "Emergency assistance needed"
    }
    
    print(f"Sending to IFTTT/Alexa: {webhook_url}")
    
    try:
        ifttt_response = requests.post(webhook_url, json=webhook_payload, timeout=10)
        print(f"Alexa: {ifttt_response.status_code} - {ifttt_response.text}")
    except Exception as e:
        print(f"Alexa error: {e}")
    
    # 2. Forward to Guardian Angel AI Backend (for dashboard + OMI)
    guardian_url = f"http://{GUARDIAN_AI_HOST}:{GUARDIAN_AI_PORT}/api/alert"
    guardian_payload = {
        "description": "Emergency alert from Arduino"
    }
    
    print(f"Forwarding to Guardian Angel AI: {guardian_url}")
    
    try:
        guardian_response = requests.post(
            guardian_url,
            json=guardian_payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        print(f"Guardian AI: {guardian_response.status_code}")
        print(f"   Dashboard updated, OMI activated")
    except Exception as e:
        print(f"Guardian AI unreachable: {e}")
        print(f"   (Alexa still works, but dashboard won't update)")
    
    return "Alert sent to Alexa and Guardian Angel AI!"

@app.route('/checkin', methods=['POST'])
def checkin():
    print("CHECK-IN RECEIVED!")
    
    # Forward check-in to Guardian Angel AI Backend
    guardian_url = f"http://{GUARDIAN_AI_HOST}:{GUARDIAN_AI_PORT}/api/checkin"
    
    print(f"Forwarding check-in to Guardian Angel AI: {guardian_url}")
    
    try:
        guardian_response = requests.post(
            guardian_url,
            json={},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        data = guardian_response.json()
        tap_count = data.get('tap_count', 0)
        alert_resolved = data.get('alert_resolved', False)
        
        print(f"Check-in: Tap {tap_count}/3")
        
        if alert_resolved:
            print(f"Alert RESOLVED via triple-tap!")
        
    except Exception as e:
        print(f"Guardian AI unreachable: {e}")
    
    return "Check-in logged"

@app.route('/')
def root():
    return '''
    <h1>Guardian Angel Server - Enhanced</h1>
    <p>Forwards alerts to both Alexa (IFTTT) and Guardian Angel AI (Dashboard + OMI)</p>
    <ul>
        <li>IFTTT/Alexa: Active</li>
        <li>Guardian Angel AI: ''' + GUARDIAN_AI_HOST + ':' + str(GUARDIAN_AI_PORT) + '''</li>
    </ul>
    '''

if __name__ == '__main__':
    print("="*70)
    print("Guardian Angel Server - Enhanced Version")
    print("="*70)
    print()
    print("IFTTT/Alexa Integration: Enabled")
    print(f"Guardian Angel AI Backend: {GUARDIAN_AI_HOST}:{GUARDIAN_AI_PORT}")
    print()
    print("IMPORTANT: Update GUARDIAN_AI_HOST with your laptop's IP!")
    print()
    print("Starting server on port 5002...")
    print("="*70)
    app.run(host='0.0.0.0', port=5002, debug=True)
