#!/usr/bin/env python3
"""
Test if environment variables are working in the server context
"""
import os
import requests

def test_env_vars():
    """Test environment variables"""
    print("Testing environment variables...")
    
    ifttt_key = os.environ.get('IFTTT_WEBHOOK_KEY')
    ifttt_event = os.environ.get('IFTTT_EVENT_NAME', 'guardian_alert')
    
    print(f"IFTTT_WEBHOOK_KEY present: {bool(ifttt_key)}")
    if ifttt_key:
        print(f"IFTTT key starts with: {ifttt_key[:10]}...")
    print(f"IFTTT event name: {ifttt_event}")
    
    if ifttt_key:
        print("\nTesting IFTTT webhook...")
        try:
            url = f"https://maker.ifttt.com/trigger/{ifttt_event}/with/key/{ifttt_key}"
            payload = {
                "value1": "Test from server environment",
                "value2": "2025-10-25T13:20:00Z",
                "value3": "Environment test"
            }
            
            response = requests.post(url, json=payload, timeout=5)
            print(f"IFTTT Status: {response.status_code}")
            print(f"IFTTT Response: {response.text}")
            
            if response.status_code == 200:
                print("\nSUCCESS: IFTTT webhook working from server environment!")
                print("Check your Alexa - it should announce the test!")
            else:
                print(f"FAILED: IFTTT returned status {response.status_code}")
                
        except Exception as e:
            print(f"ERROR: {e}")
    else:
        print("ERROR: IFTTT_WEBHOOK_KEY not found!")

if __name__ == "__main__":
    test_env_vars()
