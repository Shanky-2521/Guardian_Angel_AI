#!/usr/bin/env python3
"""
Simple Guardian Angel server - guaranteed to work
"""
from flask import Flask
import requests
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert():
    print("ALERT RECEIVED!")
    
    # Get webhook details
    webhook_key = "kouHpRJ7j7LW7l-ssgtTToG7d2Il0zPpjygqNRuDubW"
    event_name = "guardian_alert"
    
    # Send IFTTT webhook
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{webhook_key}"
    payload = {
        "value1": "Guardian Angel Alert",
        "value2": datetime.utcnow().isoformat() + 'Z',
        "value3": "Emergency assistance needed"
    }
    
    print(f"Sending webhook to: {url}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"IFTTT Status: {response.status_code}")
        print(f"IFTTT Response: {response.text}")
        
        if response.status_code == 200:
            return "Alert sent to Alexa!"
        else:
            return f"Alert failed: {response.status_code}"
            
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

@app.route('/checkin', methods=['POST'])
def checkin():
    print("CHECK-IN RECEIVED!")
    return "Check-in logged"

@app.route('/')
def root():
    return 'Simple Guardian Angel Server'

if __name__ == '__main__':
    print("Starting Simple Guardian Angel Server...")
    app.run(host='0.0.0.0', port=5001, debug=True)
