#!/usr/bin/env python3
"""
Spark Job Runner for Quantum Pi Forge
Launch and manage Spark analytics jobs within the Sacred Trinity architecture
"""

import os
import sys
import logging
import argparse
from typing import Optional

# Add server directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from spark_job_orchestrator import get_spark_orchestrator, SparkJobOrchestrator
from quantum_spark_processor import get_quantum_spark_processor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_single_job(job_id: str):
    """Run a single Spark job immediately"""
    logger.info(f"🚀 Running Spark job: {job_id}")
    
    orchestrator = get_spark_orchestrator()
    result = orchestrator.run_job(job_id)
    
    if result.get("status") == "success":
        logger.info(f"✅ Job completed successfully in {result.get('execution_time', 0):.2f}s")
        print("\n📊 Job Results:")
        print(result.get("result", {}))
    else:
        logger.error(f"❌ Job failed: {result.get('error', 'Unknown error')}")
    
    return result


def list_available_jobs():
    """List all available Spark jobs"""
    logger.info("📋 Listing available Spark jobs...")
    
    orchestrator = get_spark_orchestrator()
    jobs = orchestrator.list_jobs()
    
    print("\n🌌 Quantum Pi Forge - Spark Analytics Jobs")
    print("=" * 70)
    
    for job in jobs:
        status_emoji = {
            "pending": "⏳",
            "running": "▶️",
            "completed": "✅",
            "failed": "❌",
            "cancelled": "🚫"
        }.get(job["status"], "❓")
        
        print(f"\n{status_emoji} {job['name']}")
        print(f"   ID: {job['job_id']}")
        print(f"   Description: {job['description']}")
        print(f"   Schedule: {job['schedule_interval'] or 'Manual'}")
        print(f"   Status: {job['status']}")
        print(f"   Runs: {job['run_count']} | Errors: {job['error_count']}")
        if job['last_run']:
            print(f"   Last Run: {job['last_run']}")
    
    print("\n" + "=" * 70)


def run_test_analytics():
    """Run a quick test of Spark analytics capabilities"""
    logger.info("🧪 Running Spark analytics test...")
    
    processor = get_quantum_spark_processor()
    
    if not processor.enabled:
        logger.error("❌ Spark processor not available")
        return
    
    # Generate sample data
    from datetime import datetime, timedelta
    import random
    
    sample_quantum_data = []
    for i in range(50):
        sample_quantum_data.append({
            "transaction_id": f"test_tx_{i}",
            "user_id": f"user_{random.randint(1, 10)}",
            "amount": random.uniform(1.0, 100.0),
            "resonance_level": random.uniform(0.3, 1.0),
            "quantum_phase": random.choice(["foundation", "growth", "harmony", "transcendence"]),
            "timestamp": datetime.now() - timedelta(hours=random.randint(0, 24)),
            "ethical_score": random.uniform(300, 900),
            "coherence_score": random.uniform(0.5, 1.0),
        })
    
    # Run analysis
    logger.info("📊 Analyzing quantum resonance patterns...")
    results = processor.analyze_quantum_resonance(sample_quantum_data)
    
    print("\n🌌 Quantum Resonance Analysis Results")
    print("=" * 70)
    print(f"Total Transactions: {results.get('total_transactions', 0)}")
    print(f"Average Resonance: {results.get('average_resonance', 0):.3f}")
    print(f"Average Ethical Score: {results.get('average_ethical_score', 0):.2f}")
    print(f"Average Coherence: {results.get('average_coherence', 0):.3f}")
    print(f"Total Value: {results.get('total_value', 0):.2f} Pi")
    
    print("\n📈 Quantum Phase Distribution:")
    for phase, count in results.get('phase_distribution', {}).items():
        print(f"   {phase}: {count}")
    
    print("\n🎯 Resonance Categories:")
    for category, count in results.get('resonance_categories', {}).items():
        print(f"   {category}: {count}")
    
    print("\n" + "=" * 70)
    
    logger.info("✅ Spark analytics test completed")


def start_scheduler():
    """Start the Spark job scheduler"""
    logger.info("🔄 Starting Spark job scheduler...")
    print("\n🌌 Quantum Pi Forge - Spark Job Scheduler")
    print("Press Ctrl+C to stop\n")
    
    orchestrator = get_spark_orchestrator()
    
    try:
        orchestrator.start_scheduler()
    except KeyboardInterrupt:
        logger.info("\n🛑 Received shutdown signal")
        orchestrator.shutdown()
        logger.info("✅ Scheduler stopped")


def get_job_status(job_id: str):
    """Get status of a specific job"""
    orchestrator = get_spark_orchestrator()
    status = orchestrator.get_job_status(job_id)
    
    if status:
        print(f"\n📊 Job Status: {job_id}")
        print("=" * 70)
        for key, value in status.items():
            print(f"{key}: {value}")
        print("=" * 70)
    else:
        logger.error(f"❌ Job not found: {job_id}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Quantum Pi Forge - Spark Analytics Job Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available jobs
  python scripts/run_spark_jobs.py --list
  
  # Run a specific job
  python scripts/run_spark_jobs.py --run quantum_resonance_hourly
  
  # Test Spark analytics
  python scripts/run_spark_jobs.py --test
  
  # Start the job scheduler
  python scripts/run_spark_jobs.py --scheduler
  
  # Get job status
  python scripts/run_spark_jobs.py --status quantum_resonance_hourly
        """
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available Spark jobs'
    )
    
    parser.add_argument(
        '--run', '-r',
        metavar='JOB_ID',
        help='Run a specific job by ID'
    )
    
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Run Spark analytics test with sample data'
    )
    
    parser.add_argument(
        '--scheduler', '-s',
        action='store_true',
        help='Start the job scheduler (runs until stopped)'
    )
    
    parser.add_argument(
        '--status',
        metavar='JOB_ID',
        help='Get status of a specific job'
    )
    
    args = parser.parse_args()
    
    # Display banner
    print("\n" + "=" * 70)
    print("🌌 Quantum Pi Forge - Spark Analytics Engine")
    print("Sacred Trinity Analytics Layer")
    print("=" * 70 + "\n")
    
    # Execute requested action
    if args.list:
        list_available_jobs()
    elif args.run:
        run_single_job(args.run)
    elif args.test:
        run_test_analytics()
    elif args.scheduler:
        start_scheduler()
    elif args.status:
        get_job_status(args.status)
    else:
        parser.print_help()
        print("\nℹ️  No action specified. Use --help for available options.")


if __name__ == "__main__":
    main()
