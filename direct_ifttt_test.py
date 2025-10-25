#!/usr/bin/env python3
"""
Direct IFTTT webhook test to bypass server issues
"""
import requests
import json

def test_ifttt_direct():
    """Test IFTTT webhook directly"""
    webhook_key = "kouHpRJ7j7LW7l-ssgtTToG7d2Il0zPpjygqNRuDubW"
    event_name = "guardian_alert"
    
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{webhook_key}"
    
    payload = {
        "value1": "Guardian Angel Alert",
        "value2": "2025-10-25T13:16:00Z",
        "value3": "Emergency assistance needed"
    }
    
    print("Testing IFTTT webhook directly...")
    print(f"URL: {url}")
    print(f"Payload: {payload}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("\nIFTTT webhook sent successfully!")
            print("Check your Alexa device - it should announce the alert!")
            print("Also check IFTTT app activity to confirm it was received")
        else:
            print(f"\nIFTTT webhook failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Error sending webhook: {e}")

if __name__ == "__main__":
    test_ifttt_direct()
