#!/usr/bin/env python3
"""
Test script for Guardian Angel IFTTT integration
"""
import requests
import time

def test_alert():
    """Test the alert endpoint"""
    try:
        print("Testing Guardian Angel alert endpoint...")
        response = requests.post("http://127.0.0.1:5001/alert", timeout=10)
        print(f"Alert sent! Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        print("\nCheck your Alexa device - it should announce the alert!")
        print("If you don't hear anything, check:")
        print("1. IFTTT applet is enabled")
        print("2. Virtual Buttons skill is enabled in Alexa")
        print("3. Alexa routine is set up for 'Virtual Button 01'")
        
    except Exception as e:
        print(f"Error: {e}")

def test_checkin():
    """Test the checkin endpoint"""
    try:
        print("\nTesting Guardian Angel checkin endpoint...")
        response = requests.post("http://127.0.0.1:5001/checkin", timeout=10)
        print(f"Check-in sent! Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Guardian Angel Integration Test")
    print("=" * 40)
    
    test_alert()
    time.sleep(2)
    test_checkin()
    
    print("\n" + "=" * 40)
    print("Test complete!")
    print("\nNext steps:")
    print("1. Set up Virtual Buttons skill in Alexa app")
    print("2. Create Alexa routine for 'Virtual Button 01'")
    print("3. Test with your physical Guardian Angel device")
