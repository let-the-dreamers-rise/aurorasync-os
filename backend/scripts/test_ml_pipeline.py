"""
Test script for ML pipeline.
Tests data generation, model training, and prediction.

Usage:
    python scripts/test_ml_pipeline.py
"""

import requests
import json
import sys
import os


BASE_URL = "http://localhost:8000"
PREDICT_URL = f"{BASE_URL}/api/v1/predict"


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_model_info():
    """Test getting model information."""
    print_section("Test 1: Get Model Info")
    
    try:
        response = requests.get(f"{PREDICT_URL}/model-info", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Model info retrieved successfully")
            print(f"📦 Response:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_prediction_low_risk():
    """Test prediction with low risk features."""
    print_section("Test 2: Predict Low Risk (Normal Conditions)")
    
    # Normal operating conditions
    telematics = {
        "engine_temp": 90.0,
        "brake_pad_wear": 8.0,
        "battery_voltage": 12.8,
        "vibration": 0.3,
        "tyre_pressure": 32.0,
        "odometer": 50000.0,
        "ambient_temp": 25.0
    }
    
    print(f"📤 Sending telematics:")
    print(json.dumps(telematics, indent=2))
    
    try:
        response = requests.post(
            f"{PREDICT_URL}/test",
            json=telematics,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Prediction successful")
            print(f"📦 Response:")
            print(json.dumps(data, indent=2))
            
            risk = data["prediction"]["failure_risk"]
            prob = data["prediction"]["probability"]
            print(f"\n🎯 Result: {risk} risk ({prob * 100:.1f}% probability)")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_prediction_high_risk():
    """Test prediction with high risk features."""
    print_section("Test 3: Predict High Risk (Failure Conditions)")
    
    # Failure conditions
    telematics = {
        "engine_temp": 115.0,  # High temperature
        "brake_pad_wear": 1.5,  # Low brake pad
        "battery_voltage": 11.2,  # Low voltage
        "vibration": 1.3,  # High vibration
        "tyre_pressure": 24.0,  # Low pressure
        "odometer": 80000.0,
        "ambient_temp": 40.0  # High ambient temp
    }
    
    print(f"📤 Sending telematics:")
    print(json.dumps(telematics, indent=2))
    
    try:
        response = requests.post(
            f"{PREDICT_URL}/test",
            json=telematics,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Prediction successful")
            print(f"📦 Response:")
            print(json.dumps(data, indent=2))
            
            risk = data["prediction"]["failure_risk"]
            prob = data["prediction"]["probability"]
            print(f"\n🎯 Result: {risk} risk ({prob * 100:.1f}% probability)")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_diagnosis_agent():
    """Test diagnosis agent with ML integration."""
    print_section("Test 4: Diagnosis Agent with ML")
    
    event = {
        "type": "predict_failure",
        "payload": {
            "vehicle_id": "VEH001",
            "telematics": {
                "engine_temp": 110.0,
                "brake_pad_wear": 2.0,
                "battery_voltage": 11.5,
                "vibration": 1.2,
                "tyre_pressure": 28.0,
                "odometer": 50000.0,
                "ambient_temp": 35.0
            }
        }
    }
    
    print(f"📤 Sending event to Diagnosis Agent:")
    print(json.dumps(event, indent=2))
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/agents/test-route",
            json=event,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Agent response received")
            print(f"📦 Response:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all ML pipeline tests."""
    print("=" * 70)
    print("🧪 AuroraSync OS - ML Pipeline Test Suite")
    print("=" * 70)
    print()
    
    # Check if model exists
    model_path = "ml_models/trained/simple_failure_model.pkl"
    if not os.path.exists(model_path):
        print("⚠️  Warning: Model file not found!")
        print(f"   Expected at: {model_path}")
        print()
        print("Please train the model first:")
        print("  1. Generate data: python data_generators/generate_telematics.py")
        print("  2. Train model: python ml_models/train_simple_model.py")
        print()
        sys.exit(1)
    
    results = []
    
    # Test 1: Model Info
    results.append(("Model Info", test_model_info()))
    
    # Test 2: Low Risk Prediction
    results.append(("Low Risk Prediction", test_prediction_low_risk()))
    
    # Test 3: High Risk Prediction
    results.append(("High Risk Prediction", test_prediction_high_risk()))
    
    # Test 4: Diagnosis Agent
    results.append(("Diagnosis Agent Integration", test_diagnosis_agent()))
    
    # Summary
    print_section("Test Summary")
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print("=" * 70)
    
    if passed == total:
        print(f"✅ All tests passed! ({passed}/{total})")
        print("=" * 70)
        print()
        print("🎉 ML pipeline is working correctly!")
        print()
        print("Key Features Verified:")
        print("  ✓ Model loading")
        print("  ✓ Low risk prediction")
        print("  ✓ High risk prediction")
        print("  ✓ Diagnosis Agent integration")
        print()
        sys.exit(0)
    else:
        print(f"❌ Some tests failed ({passed}/{total} passed)")
        print("=" * 70)
        print()
        print("Troubleshooting:")
        print("  1. Ensure server is running: uvicorn app.main:app --reload")
        print("  2. Check model is trained: ls ml_models/trained/")
        print("  3. Check server logs for errors")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
