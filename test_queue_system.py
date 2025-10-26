#!/usr/bin/env python3
"""
Test Fish Audio Queue System
Demonstrates sequential playback with no overlap
"""

import requests
import time

BASE_URL = "http://localhost:5000"

def test_queue_system():
    print("🎬" * 30)
    print("  Fish Audio QUEUE System Test")
    print("🎬" * 30)
    print()
    
    # Step 1: Create alert
    print("1️⃣  Creating alert...")
    alert_resp = requests.post(f"{BASE_URL}/api/alert", 
                               json={"description": "Queue system test"})
    alert_id = alert_resp.json()['event']['id']
    print(f"   ✅ Alert: {alert_id}")
    print()
    
    # Step 2: Send multiple OMI transcripts quickly
    print("2️⃣  Sending multiple transcripts quickly...")
    print("   (Each will generate audio and add to queue)")
    print()
    
    transcripts = [
        "Help me please!",
        "Someone is following me down the street",
        "I'm scared and need help urgently",
        "They're getting closer to me",
        "Please send help immediately"
    ]
    
    for i, text in enumerate(transcripts, 1):
        print(f"   📝 Transcript {i}: '{text}'")
        requests.post(
            f"{BASE_URL}/api/omi/webhook?session_id=queue_test&uid=test",
            json={"segments": [{"text": text, "speaker": "SPEAKER_00"}]}
        )
        time.sleep(0.5)  # Small delay between transcripts
    
    print()
    print(f"   ✅ {len(transcripts)} transcripts sent!")
    print()
    
    # Step 3: Explain what's happening
    print("3️⃣  What's happening now:")
    print()
    print("   🐟 Fish Audio processing:")
    print("      - Each transcript → Smart summary")
    print("      - Each summary → Fish Audio TTS API")
    print("      - Each audio → Added to queue")
    print()
    print("   🔊 Queue Player:")
    print("      - Playing audio #1 (waits until finished)...")
    print("      - Then plays audio #2 (waits until finished)...")
    print("      - Then plays audio #3 (waits until finished)...")
    print("      - etc.")
    print()
    print("   ✅ NO OVERLAP! Sequential playback only!")
    print()
    
    # Step 4: Wait for processing
    print("4️⃣  Waiting for Fish Audio processing...")
    print("   (Check backend console for detailed logs)")
    print()
    
    time.sleep(10)
    
    print("=" * 70)
    print("🎯 Test Complete!")
    print()
    print("📊 What You Should Observe:")
    print("   ✅ 5 audio files generated")
    print("   ✅ Playing one at a time (sequential)")
    print("   ✅ No audio overlap")
    print("   ✅ Clear start/end for each message")
    print()
    print("💰 API Cost:")
    print(f"   5 TTS calls × $0.015 = ~$0.075")
    print()
    print("🔍 Check Backend Logs:")
    print("   tail -50 backend.log | grep -A 5 'QUEUE\\|🔊'")
    print()

if __name__ == '__main__':
    try:
        # Check backend
        resp = requests.get(f"{BASE_URL}/api/status")
        if resp.status_code == 200:
            test_queue_system()
        else:
            print("❌ Backend error")
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running!")
        print("Start it with: FISH_AUDIO_API_KEY='your_key' python3 backend/app.py")
