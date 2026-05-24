#!/usr/bin/env python3
"""
🌌 Sacred Trinity Production Verification & Deployment Script
Comprehensive verification of all components for production deployment
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_environment():
    """Check environment variables and dependencies"""
    print("🌍 Checking Environment Configuration...")

    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    optional_vars = ['AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED', 'QUANTUM_TRACING_ENABLED']

    missing_required = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_required.append(var)

    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print("   Please set these in your Railway dashboard or .env file")
        return False

    print("✅ Required environment variables configured")
    for var in optional_vars:
        if os.environ.get(var):
            print(f"✅ {var}: {os.environ.get(var)}")

    return True

def check_dependencies():
    """Check if all Python dependencies can be imported"""
    print("\n📦 Checking Python Dependencies...")

    dependencies = [
        'fastapi', 'uvicorn', 'supabase', 'websockets', 'pydantic',
        'flask', 'flask_cors', 'gradio', 'opentelemetry.sdk',
        'azure.ai.evaluation', 'azure.identity'
    ]

    failed_imports = []
    for dep in dependencies:
        try:
            __import__({
                "fastapi": "fastapi",
                "uvicorn": "uvicorn",
                "supabase": "supabase",
                "websockets": "websockets",
                "pydantic": "pydantic",
                "flask": "flask",
                "flask_cors": "flask_cors",
                "gradio": "gradio",
                "opentelemetry.sdk": "opentelemetry.sdk",
                "azure.ai.evaluation": "azure.ai.evaluation",
                "azure.identity": "azure.identity",
            }.get(dep, dep))
            print(f"✅ {dep}")
        except ImportError:
            failed_imports.append(dep)
            print(f"❌ {dep}")

    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False

    print("✅ All dependencies available")
    return True

def check_file_structure():
    """Check that all required files exist"""
    print("\n📁 Checking File Structure...")

    required_files = [
        'server/main.py',
        'server/app.py',
        'server/canticle_interface.py',
        'server/tracing_system.py',
        'server/requirements.txt',
        'frontend/index.html',
        'frontend/pi-forge-integration.js',
        'Dockerfile',
        'railway.toml'
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")

    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False

    print("✅ All required files present")
    return True

def check_code_syntax():
    """Check Python syntax of all main files"""
    print("\n🐍 Checking Python Syntax...")

    python_files = [
        'server/main.py',
        'server/app.py',
        'server/canticle_interface.py',
        'server/tracing_system.py'
    ]

    syntax_errors = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                compile(f.read(), file_path, 'exec')
            print(f"✅ {file_path}")
        except SyntaxError as e:
            syntax_errors.append(f"{file_path}: {e}")
            print(f"❌ {file_path}: {e}")

    if syntax_errors:
        print(f"\n❌ Syntax errors found: {len(syntax_errors)}")
        return False

    print("✅ All Python files have valid syntax")
    return True

def check_tracing_system():
    """Test tracing system initialization"""
    print("\n🔍 Testing Tracing System...")

    try:
        sys.path.insert(0, str(Path(__file__).parent / "server"))

        from tracing_system import tracing_system, fastapi_tracer, flask_tracer, gradio_tracer
        print("✅ Tracing system imported successfully")

        ft = fastapi_tracer()
        flt = flask_tracer()
        gt = gradio_tracer()

        if ft and flt and gt:
            print("✅ Component tracers initialized")
        else:
            print("❌ Component tracers not initialized")
            return False

        with tracing_system.create_quantum_span(
            ft,
            "test_operation",
            "fastapi",
            quantum_phase="foundation",
        ) as span:
            span.set_attribute("test.success", True)
            print("✅ Quantum span creation working")

        print("✅ Tracing system fully operational")
        return True

    except Exception as e:
        print(f"❌ Tracing system test failed: {e}")
        return False
def check_health_endpoints():
    """Test health endpoints if services are running"""
    print("\n🏥 Testing Health Endpoints...")

    endpoints = [
        ("FastAPI", "http://localhost:8000/health"),
        ("Flask", "http://localhost:5000/health"),
    ]

    working_endpoints = 0
    for service, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service}: {url}")
                working_endpoints += 1
            else:
                print(f"⚠️  {service}: {url} (status: {response.status_code})")
        except requests.exceptions.RequestException:
            print(f"⚠️  {service}: {url} (not reachable)")

    if working_endpoints > 0:
        print(f"✅ {working_endpoints} health endpoints responding")
    else:
        print("ℹ️  No services currently running (expected for production verification)")

    return True

def generate_deployment_report():
    """Generate comprehensive deployment report"""
    print("\n📊 PRODUCTION DEPLOYMENT VERIFICATION REPORT")
    print("=" * 60)

    checks = [
        ("Environment Configuration", check_environment()),
        ("Python Dependencies", check_dependencies()),
        ("File Structure", check_file_structure()),
        ("Python Syntax", check_code_syntax()),
        ("Tracing System", check_tracing_system()),
        ("Health Endpoints", check_health_endpoints()),
    ]

    passed_checks = sum(1 for _, passed in checks if passed)
    total_checks = len(checks)

    for check_name, passed in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {check_name}")

    print(f"\n🎯 OVERALL STATUS: {passed_checks}/{total_checks} checks passed")

    if passed_checks == total_checks:
        print("\n🎉 PRODUCTION READY!")
        print("🌌 Sacred Trinity Quantum Resonance Lattice is fully prepared for deployment")
        print("\n🚀 Deployment Instructions:")
        print("1. Push code to GitHub")
        print("2. Set SUPABASE_URL and SUPABASE_KEY in Railway dashboard")
        print("3. Deploy via Railway (uses Dockerfile)")
        print("4. Monitor health at /health endpoint")
        return True
    else:
        print(f"\n⚠️  {total_checks - passed_checks} issues need to be resolved before production deployment")
        return False

def main():
    """Main verification function"""
    print("🚀 Sacred Trinity Production Verification")
    print("🌌 Quantum Resonance Lattice - Deployment Readiness Check")
    print("=" * 60)

    success = generate_deployment_report()

    if success:
        print("\n✨ Ready for transcendence! The lattice awaits deployment.")
        return 0
    else:
        print("\n🔧 Please resolve the failed checks before deploying.")
        return 1

if __name__ == "__main__":
    exit(main())