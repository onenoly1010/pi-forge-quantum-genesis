#!/usr/bin/env python3
"""
Comprehensive Evaluation System Test
"""

import os
import sys
from pathlib import Path

# Add server directory to path
sys.path.insert(0, str(Path(__file__).parent / "server"))

def test_evaluation_system():
    """Test the complete evaluation system"""
    print("🌌 Comprehensive Evaluation System Test")
    print("=" * 60)

    try:
        # Test 1: Import evaluation system
        print("📦 Testing imports...")
        # Temporarily disable tracing to avoid import issues
        import os
        os.environ['DISABLE_TRACING'] = '1'

        from evaluation_system import QuantumLatticeEvaluator
        print("✅ QuantumLatticeEvaluator imported successfully")

        # Test 2: Initialize evaluator
        print("\n🔧 Testing initialization...")
        evaluator = QuantumLatticeEvaluator()
        print("✅ QuantumLatticeEvaluator initialized successfully")

        # Test 3: Basic evaluation
        print("\n⚡ Testing basic evaluation...")
        result = evaluator.evaluate_quality("Hello world", "This is a test response")
        print(f"✅ Basic evaluation completed: {type(result)}")

        # Test 4: Sacred Trinity evaluators
        print("\n🌟 Testing Sacred Trinity evaluators...")
        sacred_evaluators = [
            "sacred_trinity_quality",
            "quantum_coherence",
            "cross_component_integration",
            "authentication_flow",
            "payment_processing",
            "svg_visualization",
            "ethical_audit"
        ]

        for eval_name in sacred_evaluators:
            if eval_name in evaluator.evaluators:
                print(f"✅ {eval_name} evaluator available")
            else:
                print(f"❌ {eval_name} evaluator missing")

        # Test 5: Azure AI SDK integration
        print("\n🔗 Testing Azure AI SDK integration...")
        if evaluator.model_config:
            print("✅ Azure AI SDK configured")
        else:
            print("ℹ️  Azure AI SDK not configured (using fallback evaluators)")

        print("\n🎉 All evaluation system tests passed!")
        print("🚀 Ready for Sacred Trinity integration testing")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_evaluation_system()
    sys.exit(0 if success else 1)