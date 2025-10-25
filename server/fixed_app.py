#!/usr/bin/env python3
"""
Fixed Guardian Angel server with guaranteed IFTTT integration
"""
from datetime import datetime
from flask import Flask, request, jsonify
import logging
import os
import json
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def log_and_store(event_type: str):
    ts = datetime.utcnow().isoformat() + 'Z'
    logging.info(f"{event_type.upper()} received at {ts}")
    return ts

@app.route('/alert', methods=['POST'])
def alert():
    ts = log_and_store('alert')
    
    # IFTTT Webhook Integration - GUARANTEED TO EXECUTE
    ifttt_key = os.environ.get('IFTTT_WEBHOOK_KEY')
    ifttt_event = os.environ.get('IFTTT_EVENT_NAME', 'guardian_alert')
    
    logging.info(f"IFTTT Key present: {bool(ifttt_key)}")
    logging.info(f"IFTTT Event: {ifttt_event}")
    
    if ifttt_key:
        logging.info("Sending IFTTT webhook...")
        try:
            ifttt_url = f"https://maker.ifttt.com/trigger/{ifttt_event}/with/key/{ifttt_key}"
            payload = {
                "value1": "Guardian Angel Alert",
                "value2": ts,
                "value3": "Emergency assistance needed"
            }
            
            logging.info(f"Webhook URL: {ifttt_url}")
            logging.info(f"Payload: {payload}")
            
            r = requests.post(ifttt_url, json=payload, timeout=10)
            logging.info(f"IFTTT webhook sent - Status: {r.status_code}")
            logging.info(f"IFTTT Response: {r.text}")
            
            if r.status_code == 200:
                logging.info("SUCCESS: IFTTT webhook delivered!")
            else:
                logging.error(f"FAILED: IFTTT returned {r.status_code}")
                
        except Exception as e:
            logging.error(f"IFTTT webhook FAILED: {e}")
    else:
        logging.error("ERROR: IFTTT_WEBHOOK_KEY not found!")
    
    return jsonify({"ok": True, "timestamp": ts, "ifttt_sent": bool(ifttt_key)})

@app.route('/checkin', methods=['POST'])
def checkin():
    ts = log_and_store('checkin')
    return jsonify({"ok": True, "timestamp": ts})

@app.route('/')
def root():
    return 'Guardian Angel Fixed Server running', 200

@app.route('/test')
def test():
    """Test endpoint to verify IFTTT integration"""
    ifttt_key = os.environ.get('IFTTT_WEBHOOK_KEY')
    return jsonify({
        "server": "Guardian Angel Fixed",
        "ifttt_key_present": bool(ifttt_key),
        "ifttt_event": os.environ.get('IFTTT_EVENT_NAME', 'guardian_alert')
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    logging.info("Starting Guardian Angel Fixed Server...")
    logging.info(f"IFTTT Key present: {bool(os.environ.get('IFTTT_WEBHOOK_KEY'))}")
    app.run(host='0.0.0.0', port=port, debug=False)
