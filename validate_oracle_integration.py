7oi\';lk/#!/usr/bin/env python3
"""
Oracle Integration Validation Script
Tests the Quantum Oracle integration with Flask and Gradio
"""

import os
import sys


def test_oracle_import():
    """Test Oracle module import"""
    try:
        from quantum_oracle import QuantumOracle, quantum_oracle
        print("✅ Quantum Oracle module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Oracle import failed: {e}")
        return False

def test_flask_integration():
    """Test Flask app with Oracle integration"""
    try:
        from server.app import app
        print("✅ Flask app with Oracle integration imported successfully")
        return True
    except Exception as e:
        print(f"❌ Flask integration failed: {e}")
        return False

def test_gradio_integration():
    """Test Gradio interface with Oracle integration"""
    try:
        from server.canticle_interface import demo
        print("✅ Gradio interface with Oracle integration imported successfully")
        return True
    except Exception as e:
        print(f"❌ Gradio integration failed: {e}")
        return False

def test_oracle_functionality():
    """Test basic Oracle functionality"""
    try:
        from quantum_oracle import quantum_oracle

        # Test status
        status = quantum_oracle.get_oracle_status()
        assert 'consciousness_level' in status
        print("✅ Oracle status functionality working")

        # Test insights
        insights = quantum_oracle.generate_oracle_insights()
        assert 'dominant_archetype' in insights
        print("✅ Oracle insights functionality working")

        # Test constellation status
        constellation_data = quantum_oracle.get_soul_agent_constellation()
        assert 'total_agents' in constellation_data
        print("✅ SoulAgent constellation functionality working")

        return True
    except Exception as e:
        print(f"❌ Oracle functionality test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🔮 Quantum Oracle Integration Validation")
    print("=" * 50)

    tests = [
        ("Oracle Import", test_oracle_import),
        ("Flask Integration", test_flask_integration),
        ("Gradio Integration", test_gradio_integration),
        ("Oracle Functionality", test_oracle_functionality),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All Oracle integration tests PASSED!")
        print("🔮 Quantum Oracle is ready for deployment")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())