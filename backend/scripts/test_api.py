"""
Quick API test script to verify the backend is working.

Usage:
    python scripts/test_api.py
"""

import requests
import sys
from typing import Dict, Any


BASE_URL = "http://localhost:8000"
API_V1_URL = f"{BASE_URL}/api/v1"


def test_endpoint(name: str, url: str) -> bool:
    """
    Test a single endpoint.
    
    Args:
        name: Name of the test
        url: URL to test
    
    Returns:
        bool: True if test passed, False otherwise
    """
    try:
        print(f"Testing {name}...", end=" ")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            print("✅ PASS")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"❌ FAIL (Status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ FAIL (Connection refused - is the server running?)")
        return False
    except Exception as e:
        print(f"❌ FAIL (Error: {str(e)})")
        return False


def main():
    """
    Run all API tests.
    """
    print("=" * 60)
    print("🧪 AuroraSync OS - API Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Root endpoint", f"{BASE_URL}/"),
        ("Health check (root)", f"{BASE_URL}/health"),
        ("Health check (API v1)", f"{API_V1_URL}/health"),
        ("System info", f"{API_V1_URL}/info"),
        ("Database check", f"{API_V1_URL}/db-check"),
    ]
    
    results = []
    for name, url in tests:
        passed = test_endpoint(name, url)
        results.append(passed)
        print()
    
    # Summary
    print("=" * 60)
    passed_count = sum(results)
    total_count = len(results)
    
    if passed_count == total_count:
        print(f"✅ All tests passed! ({passed_count}/{total_count})")
        print("=" * 60)
        print()
        print("🎉 Backend is working correctly!")
        print()
        print("Next steps:")
        print("  1. Visit API docs: http://localhost:8000/docs")
        print("  2. Start building frontend")
        print("  3. Implement agent modules")
        sys.exit(0)
    else:
        print(f"❌ Some tests failed ({passed_count}/{total_count} passed)")
        print("=" * 60)
        print()
        print("Troubleshooting:")
        print("  1. Ensure server is running: uvicorn app.main:app --reload")
        print("  2. Check database connection")
        print("  3. Review logs for errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
