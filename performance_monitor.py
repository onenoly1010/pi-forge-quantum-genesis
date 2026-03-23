#!/usr/bin/env python3
"""
Quantum Resonance Lattice Performance Monitor
Monitors Sacred Trinity performance with tracing system integration
"""

import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests

# Add server directory to path
sys.path.insert(0, str(Path(__file__).parent / "server"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor Sacred Trinity performance and tracing"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.metrics_history: List[Dict] = []
        self.start_time = datetime.now()

    async def check_health(self) -> Dict:
        """Check system health"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response.raise_for_status()
            return {
                "status": "healthy",
                "response_time": response.elapsed.total_seconds(),
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_evaluation_performance(self) -> Dict:
        """Test evaluation system performance"""
        test_payloads = [
            {"query": "Hello world", "response": "This is a test response"},
            {"query": "Complex quantum query", "response": "Advanced response with multiple components"},
            {"query": "Authentication test", "response": "JWT token validation successful"}
        ]

        results = []
        for payload in test_payloads:
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/evaluate",
                    json=payload,
                    timeout=30
                )
                response_time = time.time() - start_time

                results.append({
                    "query_length": len(payload["query"]),
                    "response_length": len(payload["response"]),
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                })

            except Exception as e:
                results.append({
                    "error": str(e),
                    "success": False
                })

        return {
            "evaluation_tests": results,
            "average_response_time": sum(r.get("response_time", 0) for r in results if r.get("success")) / len([r for r in results if r.get("success")]) if any(r.get("success") for r in results) else 0,
            "success_rate": len([r for r in results if r.get("success")]) / len(results)
        }

    async def monitor_tracing(self) -> Dict:
        """Monitor tracing system performance"""
        try:
            # This would integrate with actual tracing endpoints
            # For now, return mock data
            return {
                "traces_collected": 0,
                "spans_created": 0,
                "error_rate": 0.0,
                "average_trace_duration": 0.0
            }
        except Exception as e:
            return {
                "tracing_error": str(e)
            }

    async def collect_metrics(self) -> Dict:
        """Collect comprehensive performance metrics"""
        timestamp = datetime.now()

        health = await self.check_health()
        evaluation = await self.test_evaluation_performance()
        tracing = await self.monitor_tracing()

        metrics = {
            "timestamp": timestamp.isoformat(),
            "uptime_seconds": (timestamp - self.start_time).total_seconds(),
            "health": health,
            "evaluation_performance": evaluation,
            "tracing_metrics": tracing
        }

        self.metrics_history.append(metrics)
        return metrics

    def generate_report(self) -> str:
        """Generate performance report"""
        if not self.metrics_history:
            return "No metrics collected yet"

        latest = self.metrics_history[-1]
        uptime_hours = latest["uptime_seconds"] / 3600

        report = f"""
🌌 Quantum Resonance Lattice Performance Report
{'='*50}
📊 Uptime: {uptime_hours:.2f} hours
🏥 Health Status: {latest['health']['status']}
⚡ Evaluation Success Rate: {latest['evaluation_performance']['success_rate']:.2%}
⏱️  Average Response Time: {latest['evaluation_performance']['average_response_time']:.3f}s

📈 Recent Metrics:
"""

        # Show last 5 metrics
        for i, metric in enumerate(self.metrics_history[-5:]):
            health_status = "✅" if metric["health"]["status"] == "healthy" else "❌"
            eval_success = metric["evaluation_performance"]["success_rate"]
            response_time = metric["evaluation_performance"]["average_response_time"]

            report += f"   {i+1}. {health_status} {eval_success:.0%} success, {response_time:.3f}s avg\n"

        return report

async def main():
    """Main monitoring function"""
    import argparse

    parser = argparse.ArgumentParser(description="Monitor Quantum Resonance Lattice Performance")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL to monitor")
    parser.add_argument("--interval", type=int, default=60, help="Monitoring interval in seconds")
    parser.add_argument("--duration", type=int, default=300, help="Monitoring duration in seconds")

    args = parser.parse_args()

    print("🌌 Quantum Resonance Lattice Performance Monitor")
    print(f"📊 Monitoring: {args.url}")
    print(f"⏱️  Interval: {args.interval}s")
    print(f"🕐 Duration: {args.duration}s")
    print("=" * 50)

    monitor = PerformanceMonitor(args.url)
    end_time = time.time() + args.duration

    try:
        while time.time() < end_time:
            metrics = await monitor.collect_metrics()

            # Print current status
            health_icon = "✅" if metrics["health"]["status"] == "healthy" else "❌"
            eval_success = metrics["evaluation_performance"]["success_rate"]
            response_time = metrics["evaluation_performance"]["average_response_time"]

            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {health_icon} Health: {metrics['health']['status']} | "
                  f"Eval: {eval_success:.0%} | "
                  f"Response: {response_time:.3f}s")

            await asyncio.sleep(args.interval)

        # Generate final report
        print("\n" + monitor.generate_report())

    except KeyboardInterrupt:
        print("\n" + monitor.generate_report())
    except Exception as e:
        logger.error(f"Monitoring failed: {e}")
        print(f"\n❌ Monitoring failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())