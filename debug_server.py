#!/usr/bin/env python3
"""
Debug version of Guardian Angel server to troubleshoot IFTTT integration
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
    
    # Debug: Check environment variables
    ifttt_key = os.environ.get('IFTTT_WEBHOOK_KEY')
    ifttt_event = os.environ.get('IFTTT_EVENT_NAME', 'guardian_alert')
    
    logging.info(f"DEBUG: IFTTT_WEBHOOK_KEY present: {bool(ifttt_key)}")
    if ifttt_key:
        logging.info(f"DEBUG: IFTTT key starts with: {ifttt_key[:10]}...")
    logging.info(f"DEBUG: IFTTT event name: {ifttt_event}")
    
    if ifttt_key:
        try:
            ifttt_url = f"https://maker.ifttt.com/trigger/{ifttt_event}/with/key/{ifttt_key}"
            logging.info(f"DEBUG: Sending to URL: {ifttt_url}")
            
            payload = {
                "value1": "Guardian Angel Alert",
                "value2": ts,
                "value3": "Emergency assistance needed"
            }
            logging.info(f"DEBUG: Payload: {payload}")
            
            r = requests.post(ifttt_url, json=payload, timeout=5)
            logging.info(f"IFTTT webhook sent - Status: {r.status_code}")
            logging.info(f"IFTTT response: {r.text}")
            
        except Exception as e:
            logging.error(f"IFTTT webhook failed: {e}")
    else:
        logging.error("IFTTT_WEBHOOK_KEY not found in environment variables!")
    
    return jsonify({"ok": True, "timestamp": ts})

@app.route('/checkin', methods=['POST'])
def checkin():
    ts = log_and_store('checkin')
    return jsonify({"ok": True, "timestamp": ts})

@app.route('/')
def root():
    return 'Guardian Angel Debug Server running', 200

@app.route('/debug')
def debug():
    """Debug endpoint to check environment"""
    env_vars = {
        'IFTTT_WEBHOOK_KEY': bool(os.environ.get('IFTTT_WEBHOOK_KEY')),
        'IFTTT_EVENT_NAME': os.environ.get('IFTTT_EVENT_NAME', 'guardian_alert'),
        'PORT': os.environ.get('PORT', '5000')
    }
    return jsonify(env_vars)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    logging.info("Starting Guardian Angel Debug Server...")
    logging.info(f"IFTTT Key present: {bool(os.environ.get('IFTTT_WEBHOOK_KEY'))}")
    app.run(host='0.0.0.0', port=port, debug=True)
