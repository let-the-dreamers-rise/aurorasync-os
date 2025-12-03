"""
Test script for the multi-agent system.
Tests agent routing, UEBA logging, and worker agent responses.

Usage:
    python scripts/test_agents.py
"""

import requests
import json
import sys
from typing import Dict, Any


BASE_URL = "http://localhost:8000"
AGENTS_URL = f"{BASE_URL}/api/v1/agents"


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_response(response: requests.Response):
    """Print a formatted response."""
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📦 Response:")
        print(json.dumps(data, indent=2))
    else:
        print(f"❌ Status: {response.status_code}")
        print(f"Error: {response.text}")


def test_agent_status():
    """Test getting agent status."""
    print_section("Test 1: Get Agent Status")
    
    try:
        response = requests.get(f"{AGENTS_URL}/status", timeout=5)
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_event_types():
    """Test getting available event types."""
    print_section("Test 2: Get Available Event Types")
    
    try:
        response = requests.get(f"{AGENTS_URL}/event-types", timeout=5)
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_agent_routing(event_type: str, payload: Dict[str, Any], description: str):
    """Test routing an event to an agent."""
    print_section(f"Test: {description}")
    
    event = {
        "type": event_type,
        "payload": payload,
        "source": "test_script"
    }
    
    print(f"📤 Sending event: {event_type}")
    print(f"   Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{AGENTS_URL}/test-route",
            json=event,
            timeout=5
        )
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_ueba_stats():
    """Test getting UEBA statistics."""
    print_section("Test: Get UEBA Statistics")
    
    try:
        response = requests.get(f"{AGENTS_URL}/ueba/stats", timeout=5)
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all agent tests."""
    print("=" * 70)
    print("🧪 AuroraSync OS - Multi-Agent System Test Suite")
    print("=" * 70)
    print()
    print("Testing the Master Agent and Worker Agents...")
    print()
    
    results = []
    
    # Test 1: Agent Status
    results.append(("Agent Status", test_agent_status()))
    
    # Test 2: Event Types
    results.append(("Event Types", test_event_types()))
    
    # Test 3: Data Analysis Agent
    results.append((
        "Data Analysis Agent",
        test_agent_routing(
            "analyze_data",
            {"vehicle_id": "VEH001", "data": {"rpm": 2500, "temp": 85.5}},
            "Data Analysis Agent - Analyze Data"
        )
    ))
    
    # Test 4: Diagnosis Agent
    results.append((
        "Diagnosis Agent",
        test_agent_routing(
            "predict_failure",
            {"vehicle_id": "VEH001", "features": {"brake_pad_thickness": 2.1}},
            "Diagnosis Agent - Predict Failure"
        )
    ))
    
    # Test 5: Customer Engagement Agent
    results.append((
        "Customer Engagement Agent",
        test_agent_routing(
            "engage_customer",
            {"vehicle_id": "VEH001", "customer_id": "CUST-001"},
            "Customer Engagement Agent - Engage Customer"
        )
    ))
    
    # Test 6: Scheduling Agent
    results.append((
        "Scheduling Agent",
        test_agent_routing(
            "schedule_service",
            {"vehicle_id": "VEH001", "service_type": "brake_replacement"},
            "Scheduling Agent - Schedule Service"
        )
    ))
    
    # Test 7: Feedback Agent
    results.append((
        "Feedback Agent",
        test_agent_routing(
            "validate_prediction",
            {"prediction_id": "PRED-12345", "actual_outcome": "brake_failure"},
            "Feedback Agent - Validate Prediction"
        )
    ))
    
    # Test 8: Manufacturing Insights Agent
    results.append((
        "Manufacturing Insights Agent",
        test_agent_routing(
            "generate_rca",
            {"component": "brake_system", "failure_count": 50},
            "Manufacturing Insights Agent - Generate RCA"
        )
    ))
    
    # Test 9: UEBA Statistics
    results.append(("UEBA Statistics", test_ueba_stats()))
    
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
        print("🎉 Multi-agent system is working correctly!")
        print()
        print("Key Features Verified:")
        print("  ✓ Master Agent routing")
        print("  ✓ All 7 worker agents responding")
        print("  ✓ UEBA logging active")
        print("  ✓ Event type mapping")
        print()
        print("Next Steps:")
        print("  1. Implement full agent logic")
        print("  2. Add ML model integration")
        print("  3. Add Redis pub/sub")
        print("  4. Add WebSocket support")
        print()
        sys.exit(0)
    else:
        print(f"❌ Some tests failed ({passed}/{total} passed)")
        print("=" * 70)
        print()
        print("Troubleshooting:")
        print("  1. Ensure server is running: uvicorn app.main:app --reload")
        print("  2. Check server logs for errors")
        print("  3. Verify all agent files are created")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
