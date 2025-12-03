"""
Quick test script for Voice API endpoints.
Run this to verify the Voice AI is working.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_voice_engage():
    """Test voice engagement endpoint."""
    print("\n🎤 Testing Voice Engagement...")
    
    payload = {
        "scenario": "predicted_failure",
        "vehicle_data": {
            "vehicle_id": "VEH001",
            "owner_name": "Rahul",
            "model": "Honda Accord",
            "make": "Honda"
        },
        "prediction_data": {
            "component": "brake_system",
            "probability": 0.85,
            "risk_level": "high"
        },
        "booking_data": {
            "workshop_name": "AutoCare Mumbai",
            "recommended_slot": "tomorrow at 10 AM"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/voice/engage", json=payload, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        print("✅ Voice engagement successful!")
        print(f"   Conversation ID: {data.get('conversation_id')}")
        print(f"   Message: {data.get('message', data.get('text', 'N/A'))[:100]}...")
        print(f"   Has Audio: {'audio' in data}")
        
        return data.get('conversation_id')
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Is the backend running?")
        print("   Run: cd backend && python -m uvicorn app.main:app --reload")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_voice_continue(conversation_id):
    """Test conversation continuation."""
    if not conversation_id:
        print("\n⏭️  Skipping continuation test (no conversation ID)")
        return
    
    print("\n💬 Testing Conversation Continuation...")
    
    payload = {
        "conversation_id": conversation_id,
        "user_response": "Yes, please book it"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/voice/continue", json=payload, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        print("✅ Conversation continuation successful!")
        print(f"   Message: {data.get('message', data.get('text', 'N/A'))[:100]}...")
        print(f"   Action: {data.get('action', 'N/A')}")
        print(f"   Complete: {data.get('conversation_complete', False)}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def test_health():
    """Test if backend is running."""
    print("🏥 Testing Backend Health...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        response.raise_for_status()
        print("✅ Backend is running!")
        return True
    except requests.exceptions.Timeout:
        print("❌ Backend connection timeout!")
        print("   Backend may be starting up, please wait...")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running!")
        print("   Start it with: cd backend && python -m uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Voice AI API Test Suite")
    print("=" * 60)
    
    # Test health first
    if not test_health():
        print("\n⚠️  Please start the backend server first!")
        exit(1)
    
    # Test voice engagement
    conversation_id = test_voice_engage()
    
    # Test continuation
    test_voice_continue(conversation_id)
    
    print("\n" + "=" * 60)
    print("✅ Voice AI tests complete!")
    print("=" * 60)
