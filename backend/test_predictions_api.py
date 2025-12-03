"""
Quick test script for Predictions API endpoints.
Run this to verify predictions are working with mock data.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

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


def test_mock_predictions():
    """Test mock predictions endpoint."""
    print("\n🔮 Testing Mock Predictions...")
    
    try:
        response = requests.get(f"{BASE_URL}/predict/mock", timeout=5)
        response.raise_for_status()
        
        data = response.json()
        print("✅ Mock predictions successful!")
        print(f"   Total Vehicles: {data['summary']['total_vehicles']}")
        print(f"   High Risk: {data['summary']['high_risk']}")
        print(f"   Medium Risk: {data['summary']['medium_risk']}")
        print(f"   Low Risk: {data['summary']['low_risk']}")
        
        # Show first prediction
        if data['predictions']:
            pred = data['predictions'][0]
            print(f"\n   Sample Prediction:")
            print(f"   - Vehicle: {pred['vehicle_id']} ({pred['model']})")
            print(f"   - Risk: {pred['prediction']['failure_risk']}")
            print(f"   - Component: {pred['prediction']['component']}")
            print(f"   - Probability: {pred['prediction']['probability']}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Is the backend running?")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_single_prediction():
    """Test single prediction endpoint."""
    print("\n🚗 Testing Single Prediction...")
    
    payload = {
        "engine_temp": 110.0,
        "brake_pad_wear": 2.0,
        "battery_voltage": 11.5,
        "vibration": 1.2,
        "tyre_pressure": 28.0,
        "odometer": 50000.0,
        "ambient_temp": 35.0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict/test", json=payload, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        pred = data['prediction']
        
        print("✅ Single prediction successful!")
        print(f"   Risk Level: {pred['failure_risk']}")
        print(f"   Probability: {pred['probability']}")
        print(f"   Component: {pred['component']}")
        print(f"   Days Until Failure: {pred['days_until_failure']}")
        print(f"   Action: {pred['recommended_action']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def test_batch_prediction():
    """Test batch prediction endpoint."""
    print("\n📦 Testing Batch Prediction...")
    
    payload = [
        {
            "engine_temp": 110.0,
            "brake_pad_wear": 2.0,
            "battery_voltage": 11.5,
            "vibration": 1.2,
            "tyre_pressure": 28.0,
            "odometer": 50000.0,
            "ambient_temp": 35.0
        },
        {
            "engine_temp": 95.0,
            "brake_pad_wear": 6.0,
            "battery_voltage": 12.3,
            "vibration": 0.8,
            "tyre_pressure": 32.0,
            "odometer": 30000.0,
            "ambient_temp": 25.0
        },
        {
            "engine_temp": 85.0,
            "brake_pad_wear": 8.0,
            "battery_voltage": 12.6,
            "vibration": 0.5,
            "tyre_pressure": 32.0,
            "odometer": 20000.0,
            "ambient_temp": 22.0
        }
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/predict/batch", json=payload, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        summary = data['summary']
        
        print("✅ Batch prediction successful!")
        print(f"   Total Predictions: {data['count']}")
        print(f"   High Risk: {summary['high_risk']}")
        print(f"   Medium Risk: {summary['medium_risk']}")
        print(f"   Low Risk: {summary['low_risk']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def test_model_info():
    """Test model info endpoint."""
    print("\n📊 Testing Model Info...")
    
    try:
        response = requests.get(f"{BASE_URL}/predict/model-info", timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        print("✅ Model info retrieved!")
        print(f"   Model Type: {data['model_type']}")
        print(f"   Description: {data['description']}")
        print(f"   Features: {data['n_features']}")
        print(f"   Accuracy: {data['accuracy']}")
        print(f"   Components: {len(data['components_detected'])}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Predictions API Test Suite")
    print("=" * 60)
    
    # Test health first
    if not test_health():
        print("\n⚠️  Please start the backend server first!")
        exit(1)
    
    # Test all endpoints
    test_mock_predictions()
    test_single_prediction()
    test_batch_prediction()
    test_model_info()
    
    print("\n" + "=" * 60)
    print("✅ All prediction tests complete!")
    print("=" * 60)
    print("\n💡 Tip: Use GET /api/v1/predict/mock for easy frontend testing!")
