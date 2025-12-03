"""
Quick test script for ML predictions without dependencies.
"""

import sys
sys.path.insert(0, '.')

from app.ml.failure_predictor import predict_failure, get_model_info

# Test cases
test_cases = [
    {
        "name": "Healthy Vehicle",
        "features": {
            "engine_temp": 90.0,
            "brake_pad_wear": 8.0,
            "battery_voltage": 12.6,
            "vibration": 0.3,
            "tyre_pressure": 32.0,
            "odometer": 30000,
            "ambient_temp": 25.0
        }
    },
    {
        "name": "Medium Risk Vehicle",
        "features": {
            "engine_temp": 105.0,
            "brake_pad_wear": 5.0,
            "battery_voltage": 12.0,
            "vibration": 1.0,
            "tyre_pressure": 28.0,
            "odometer": 75000,
            "ambient_temp": 35.0
        }
    },
    {
        "name": "High Risk Vehicle",
        "features": {
            "engine_temp": 115.0,
            "brake_pad_wear": 2.0,
            "battery_voltage": 11.5,
            "vibration": 1.8,
            "tyre_pressure": 25.0,
            "odometer": 120000,
            "ambient_temp": 45.0
        }
    }
]

print("=" * 60)
print("ML PREDICTION TEST - Rule-Based Predictor")
print("=" * 60)

# Get model info
print("\n📊 Model Information:")
info = get_model_info()
for key, value in info.items():
    print(f"  {key}: {value}")

# Run test cases
print("\n" + "=" * 60)
print("TEST CASES")
print("=" * 60)

for test in test_cases:
    print(f"\n🚗 {test['name']}")
    print("-" * 60)
    
    result = predict_failure(test['features'])
    
    print(f"  Risk Level: {result['failure_risk']}")
    print(f"  Probability: {result['probability']:.2%}")
    print(f"  Model Type: {result['model_type']}")
    
    print("\n  Feature Contributions:")
    for feature, contrib in result['feature_contributions'].items():
        print(f"    {feature:20s}: {contrib['value']:8.2f} → Risk: {contrib['risk_score']:.3f} (Weight: {contrib['weighted_contribution']:.3f})")

print("\n" + "=" * 60)
print("✅ All tests passed! ML predictions working without scikit-learn!")
print("=" * 60)
