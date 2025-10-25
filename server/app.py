from datetime import datetime
from flask import Flask, request, jsonify
import logging
import os
import json

import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Optional Chroma
USE_CHROMA = os.environ.get('CHROMA_ENABLE', '0') == '1'
CHROMA_COLLECTION = 'guardian_events'

if USE_CHROMA:
    import chromadb
    from chromadb.config import Settings
    client = chromadb.Client(Settings(persist_directory=os.path.join(os.getcwd(), 'chroma_data')))
    try:
        collection = client.get_collection(CHROMA_COLLECTION)
    except Exception:
        collection = client.create_collection(CHROMA_COLLECTION)
else:
    client = None
    collection = None


def log_and_store(event_type: str):
    ts = datetime.utcnow().isoformat() + 'Z'
    logging.info(f"{event_type.upper()} received at {ts}")
    if collection:
        collection.add(documents=[{"type": event_type, "timestamp": ts}], ids=[f"{event_type}-{ts}"])
    return ts


@app.route('/checkin', methods=['POST'])
def checkin():
    ts = log_and_store('checkin')
    
    # Optional: Send check-in to IFTTT (can trigger Alexa confirmation)
    ifttt_key = os.environ.get('IFTTT_WEBHOOK_KEY')
    ifttt_checkin_event = os.environ.get('IFTTT_CHECKIN_EVENT', 'guardian_checkin')
    if ifttt_key and os.environ.get('IFTTT_ENABLE_CHECKIN', '0') == '1':
        try:
            ifttt_url = f"https://maker.ifttt.com/trigger/{ifttt_checkin_event}/with/key/{ifttt_key}"
            payload = {
                "value1": "Guardian Angel Check-in",
                "value2": ts,
                "value3": "All is well"
            }
            r = requests.post(ifttt_url, json=payload, timeout=5)
            logging.info(f"IFTTT check-in webhook sent - Status: {r.status_code}")
        except Exception as e:
            logging.warning(f"IFTTT check-in webhook failed: {e}")
    
    return jsonify({"ok": True, "timestamp": ts})


@app.route('/alert', methods=['POST'])
def alert():
    ts = log_and_store('alert')

    # Method 1: IFTTT Webhook Integration (Recommended)
    ifttt_key = os.environ.get('IFTTT_WEBHOOK_KEY')
    ifttt_event = os.environ.get('IFTTT_EVENT_NAME', 'guardian_alert')
    if ifttt_key:
        try:
            ifttt_url = f"https://maker.ifttt.com/trigger/{ifttt_event}/with/key/{ifttt_key}"
            payload = {
                "value1": "Guardian Angel Alert",
                "value2": ts,
                "value3": "Emergency assistance needed"
            }
            r = requests.post(ifttt_url, json=payload, timeout=5)
            logging.info(f"IFTTT webhook sent - Status: {r.status_code}")
        except Exception as e:
            logging.warning(f"IFTTT webhook failed: {e}")

    # Method 2: Keep HA-Bridge as backup (Optional)
    habridge_host = os.environ.get('HABRIDGE_HOST')  # e.g., 'http://10.65.219.95:80'
    habridge_light_id = os.environ.get('HABRIDGE_LIGHT_ID')  # e.g., '1'
    if habridge_host and habridge_light_id:
        try:
            url = f"{habridge_host}/api/newdeveloper/lights/{habridge_light_id}/state"
            payload = {"on": True}
            r = requests.put(url, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=2)
            logging.info(f"HA-Bridge trigger status {r.status_code}: {r.text[:120]}")
        except Exception as e:
            logging.warning(f"HA-Bridge trigger failed: {e}")

    return jsonify({"ok": True, "timestamp": ts})


@app.route('/')
def root():
    return 'Guardian Angel Logging Server running', 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port)
