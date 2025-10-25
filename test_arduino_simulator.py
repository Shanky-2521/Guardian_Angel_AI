#!/usr/bin/env python3
"""
Arduino Simulator - Sends dummy data to backend as if from Arduino
This simulates the touch sensor behavior without actual hardware.
"""

import requests
import time
import random
from datetime import datetime

API_BASE_URL = "http://localhost:5000"

def send_checkin():
    """Simulate a check-in event (short touch)"""
    try:
        response = requests.post(f"{API_BASE_URL}/api/checkin")
        if response.status_code == 200:
            print(f"✓ [{datetime.now().strftime('%H:%M:%S')}] Check-in sent successfully")
            return True
        else:
            print(f"✗ Check-in failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error sending check-in: {e}")
        return False

def send_alert(description="Simulated emergency alert - Touch sensor held 3 seconds"):
    """Simulate an alert event (long touch)"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/alert",
            json={"description": description}
        )
        if response.status_code == 200:
            print(f"🚨 [{datetime.now().strftime('%H:%M:%S')}] ALERT sent successfully")
            return True
        else:
            print(f"✗ Alert failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error sending alert: {e}")
        return False

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Backend is online")
            print(f"  - Total events: {data.get('total_events', 0)}")
            print(f"  - ChromaDB: {'Connected' if data.get('chroma_connected') else 'Disconnected'}")
            print(f"  - Claude AI: {'Available' if data.get('claude_available') else 'Not configured'}")
            return True
        return False
    except Exception as e:
        print(f"✗ Backend not reachable: {e}")
        return False

def run_demo_sequence():
    """Run a demo sequence of events"""
    print("\n" + "="*60)
    print("🎬 Running Demo Sequence")
    print("="*60 + "\n")
    
    scenarios = [
        ("Check-in", lambda: send_checkin(), 2),
        ("Check-in", lambda: send_checkin(), 2),
        ("Alert", lambda: send_alert("Emergency detected!"), 3),
        ("Check-in", lambda: send_checkin(), 2),
        ("Alert", lambda: send_alert("Fall detected!"), 3),
        ("Check-in", lambda: send_checkin(), 2),
    ]
    
    for i, (event_type, action, wait) in enumerate(scenarios, 1):
        print(f"\n[{i}/{len(scenarios)}] Simulating {event_type}...")
        action()
        if i < len(scenarios):
            print(f"   Waiting {wait} seconds...")
            time.sleep(wait)
    
    print("\n" + "="*60)
    print("✅ Demo sequence complete!")
    print("="*60)

def interactive_mode():
    """Interactive mode for manual testing"""
    print("\n" + "="*60)
    print("🎮 Interactive Arduino Simulator")
    print("="*60)
    print("\nCommands:")
    print("  1 or c - Send check-in")
    print("  2 or a - Send alert")
    print("  d - Run demo sequence")
    print("  s - Check backend status")
    print("  q - Quit")
    print("\n")
    
    while True:
        try:
            cmd = input("Enter command: ").strip().lower()
            
            if cmd in ['q', 'quit', 'exit']:
                print("👋 Goodbye!")
                break
            elif cmd in ['1', 'c', 'checkin']:
                send_checkin()
            elif cmd in ['2', 'a', 'alert']:
                send_alert()
            elif cmd == 'd':
                run_demo_sequence()
            elif cmd == 's':
                check_backend()
            else:
                print("Unknown command. Try: 1, 2, d, s, or q")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    print("🛡️  Guardian Angel - Arduino Simulator")
    print("=" * 60)
    
    # Check backend first
    print("\n📡 Checking backend connection...")
    if not check_backend():
        print("\n❌ Backend is not running!")
        print("   Start it with: ./start.sh")
        print("   Or manually: cd backend && python app.py")
        return
    
    print("\n" + "="*60)
    print("Choose mode:")
    print("  1 - Run automated demo sequence")
    print("  2 - Interactive mode (manual control)")
    print("="*60)
    
    choice = input("\nYour choice (1 or 2): ").strip()
    
    if choice == '1':
        run_demo_sequence()
    elif choice == '2':
        interactive_mode()
    else:
        print("Invalid choice. Running demo sequence...")
        run_demo_sequence()

if __name__ == "__main__":
    main()
