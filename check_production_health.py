#!/usr/bin/env python3
"""
Simple Production Health Check
Checks Railway and Vercel deployments after environment variables are configured
"""

import requests
import time

def check_production_health():
    """Check production health endpoints"""
    print("🏥 Checking Production Health Endpoints...")
    print("=" * 50)

    endpoints = [
        ("Railway API", "https://pi-forge-quantum-genesis.railway.app/health"),
        ("Vercel Frontend", "https://quantum-resonance-clean.vercel.app"),
    ]

    results = []
    for service, url in endpoints:
        print(f"Checking {service}: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {service}: {response.status_code} OK")
                results.append(True)
            else:
                print(f"⚠️  {service}: {response.status_code} {response.reason}")
                results.append(False)
        except requests.exceptions.RequestException as e:
            print(f"❌ {service}: Connection failed - {e}")
            results.append(False)
        print()

    print("🎯 RESULTS:")
    print(f"Railway API: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"Vercel Frontend: {'✅ PASS' if results[1] else '❌ FAIL'}")

    if all(results):
        print("\n🎉 ALL PRODUCTION SERVICES ARE HEALTHY!")
        print("🌌 Sacred Trinity Quantum Resonance Lattice is live!")
        return True
    else:
        print(f"\n⚠️  {len(results) - sum(results)} services need attention")
        print("Check Railway/Vercel logs for deployment issues")
        return False

if __name__ == "__main__":
    success = check_production_health()
    exit(0 if success else 1)