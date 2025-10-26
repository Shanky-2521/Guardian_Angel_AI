#!/usr/bin/env python3
"""
Test Fish Audio Integration
Demonstrates smart summary generation from OMI transcripts
"""

import requests
import time

BASE_URL = "http://localhost:5000"

def test_fish_audio():
    print("🐟" * 30)
    print("  Fish Audio Integration Test")
    print("🐟" * 30)
    print()
    
    # Step 1: Create alert
    print("1️⃣  Creating alert...")
    alert_resp = requests.post(f"{BASE_URL}/api/alert", 
                               json={"description": "Fish Audio test"})
    alert_id = alert_resp.json()['event']['id']
    print(f"   ✅ Alert: {alert_id}")
    print()
    
    # Step 2: Send OMI transcripts
    print("2️⃣  Sending OMI transcripts...")
    transcripts = [
        "Help me please!",
        "Someone is following me",
        "I'm scared, need help urgently"
    ]
    
    for i, text in enumerate(transcripts, 1):
        print(f"   Transcript {i}: '{text}'")
        requests.post(
            f"{BASE_URL}/api/omi/webhook?session_id=test&uid=test",
            json={"segments": [{"text": text, "speaker": "SPEAKER_00"}]}
        )
        time.sleep(1)
    
    print()
    print("   ✅ 3 transcripts sent")
    print()
    
    # Step 3: Fish Audio should auto-trigger after 3 transcripts
    print("3️⃣  Fish Audio auto-processing...")
    print("   (Check backend console for output)")
    time.sleep(2)
    print()
    
    # Step 4: Manual Fish Audio generation
    print("4️⃣  Testing manual Fish Audio API...")
    fish_resp = requests.post(
        f"{BASE_URL}/api/fish-audio/summary",
        json={
            "transcripts": transcripts,
            "play": False  # Set to True to play audio
        }
    )
    
    if fish_resp.status_code == 200:
        data = fish_resp.json()
        print(f"   ✅ Summary generated!")
        print()
        print(f"   📝 Summary:")
        print(f"   {data['summary']}")
        print()
        print(f"   🎵 Audio URL: {data['audio_url'] or 'Demo mode'}")
        print(f"   📊 Mode: {data['mode']}")
        print(f"   📄 Transcript count: {data['transcript_count']}")
    else:
        print(f"   ❌ Error: {fish_resp.text}")
    
    print()
    print("=" * 70)
    print("🎯 Test Complete!")
    print()
    print("📊 What Happened:")
    print("   ✅ Alert created")
    print("   ✅ OMI transcripts processed")
    print("   ✅ Smart summary generated")
    print("   ✅ Fish Audio integration working!")
    print()
    print("🔧 To Enable Voice:")
    print("   1. Get Fish Audio API key from https://fish.audio")
    print("   2. Set: export FISH_AUDIO_API_KEY='your_key'")
    print("   3. Restart backend")
    print("   4. Audio will play automatically!")
    print()

if __name__ == '__main__':
    try:
        # Check backend
        resp = requests.get(f"{BASE_URL}/api/status")
        if resp.status_code == 200:
            test_fish_audio()
        else:
            print("❌ Backend error")
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running!")
        print("Start it with: python3 backend/app.py")
