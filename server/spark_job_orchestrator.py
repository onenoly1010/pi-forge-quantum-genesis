"""
Spark Job Orchestrator for Quantum Pi Forge
Manages and schedules Spark analytics jobs within the Sacred Trinity architecture
"""

import logging
import os
import time
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum

try:
    import schedule
    schedule_available = True
except ImportError:
    schedule_available = False

from quantum_spark_processor import get_quantum_spark_processor, QuantumSparkProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobStatus(Enum):
    """Spark job execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SparkJob:
    """Represents a Spark analytics job"""
    
    def __init__(
        self,
        job_id: str,
        name: str,
        job_function: Callable,
        schedule_interval: Optional[str] = None,
        description: str = ""
    ):
        self.job_id = job_id
        self.name = name
        self.job_function = job_function
        self.schedule_interval = schedule_interval
        self.description = description
        self.status = JobStatus.PENDING
        self.last_run = None
        self.last_result = None
        self.run_count = 0
        self.error_count = 0
        
    def execute(self) -> Dict[str, Any]:
        """Execute the Spark job"""
        self.status = JobStatus.RUNNING
        start_time = time.time()
        
        try:
            logger.info(f"🚀 Starting Spark job: {self.name} ({self.job_id})")
            result = self.job_function()
            
            self.status = JobStatus.COMPLETED
            self.last_run = datetime.now()
            self.last_result = result
            self.run_count += 1
            
            execution_time = time.time() - start_time
            logger.info(f"✅ Spark job completed: {self.name} in {execution_time:.2f}s")
            
            return {
                "job_id": self.job_id,
                "status": "success",
                "execution_time": execution_time,
                "result": result,
                "timestamp": self.last_run.isoformat()
            }
            
        except Exception as e:
            self.status = JobStatus.FAILED
            self.error_count += 1
            execution_time = time.time() - start_time
            
            logger.error(f"❌ Spark job failed: {self.name} - {str(e)}")
            
            return {
                "job_id": self.job_id,
                "status": "failed",
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary representation"""
        return {
            "job_id": self.job_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "schedule_interval": self.schedule_interval,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "run_count": self.run_count,
            "error_count": self.error_count,
        }


class SparkJobOrchestrator:
    """
    Orchestrates Spark analytics jobs for Quantum Pi Forge
    
    Manages job scheduling, execution, and monitoring within the Sacred Trinity
    """
    
    def __init__(self):
        self.jobs: Dict[str, SparkJob] = {}
        self.spark_processor = get_quantum_spark_processor()
        self.scheduler_running = False
        self._init_default_jobs()
        
    def _init_default_jobs(self):
        """Initialize default Spark analytics jobs"""
        # Quantum resonance analysis job
        self.register_job(
            job_id="quantum_resonance_hourly",
            name="Hourly Quantum Resonance Analysis",
            job_function=self._quantum_resonance_job,
            schedule_interval="hourly",
            description="Analyzes quantum resonance patterns across the lattice"
        )
        
        # Payment analytics job
        self.register_job(
            job_id="payment_analytics_daily",
            name="Daily Payment Analytics",
            job_function=self._payment_analytics_job,
            schedule_interval="daily",
            description="Analyzes payment transaction patterns and trends"
        )
        
        # Ethical coherence job
        self.register_job(
            job_id="ethical_coherence_daily",
            name="Daily Ethical Coherence Assessment",
            job_function=self._ethical_coherence_job,
            schedule_interval="daily",
            description="Computes ethical coherence matrix from audit data"
        )
        
        # Sacred Trinity report job
        self.register_job(
            job_id="trinity_report_weekly",
            name="Weekly Sacred Trinity Report",
            job_function=self._trinity_report_job,
            schedule_interval="weekly",
            description="Generates comprehensive analytics across all components"
        )
        
        logger.info(f"✅ Initialized {len(self.jobs)} default Spark jobs")
    
    def register_job(
        self,
        job_id: str,
        name: str,
        job_function: Callable,
        schedule_interval: Optional[str] = None,
        description: str = ""
    ) -> SparkJob:
        """
        Register a new Spark job
        
        Args:
            job_id: Unique job identifier
            name: Human-readable job name
            job_function: Function to execute
            schedule_interval: Optional schedule (hourly, daily, weekly)
            description: Job description
            
        Returns:
            Registered SparkJob instance
        """
        job = SparkJob(
            job_id=job_id,
            name=name,
            job_function=job_function,
            schedule_interval=schedule_interval,
            description=description
        )
        
        self.jobs[job_id] = job
        logger.info(f"📝 Registered Spark job: {name} ({job_id})")
        
        return job
    
    def run_job(self, job_id: str) -> Dict[str, Any]:
        """
        Execute a specific job immediately
        
        Args:
            job_id: Job identifier to execute
            
        Returns:
            Job execution result
        """
        if job_id not in self.jobs:
            logger.error(f"❌ Job not found: {job_id}")
            return {"error": f"Job {job_id} not found"}
        
        job = self.jobs[job_id]
        return job.execute()
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific job"""
        if job_id not in self.jobs:
            return None
        return self.jobs[job_id].to_dict()
    
    def list_jobs(self) -> List[Dict[str, Any]]:
        """List all registered jobs"""
        return [job.to_dict() for job in self.jobs.values()]
    
    def start_scheduler(self):
        """Start the job scheduler"""
        if not schedule_available:
            logger.warning("⚠️ schedule library not available - scheduler disabled")
            return
        
        logger.info("🔄 Starting Spark job scheduler...")
        
        # Schedule jobs based on their intervals
        for job in self.jobs.values():
            if job.schedule_interval == "hourly":
                schedule.every().hour.do(lambda j=job: j.execute())
            elif job.schedule_interval == "daily":
                schedule.every().day.at("00:00").do(lambda j=job: j.execute())
            elif job.schedule_interval == "weekly":
                schedule.every().monday.at("00:00").do(lambda j=job: j.execute())
        
        self.scheduler_running = True
        logger.info("✅ Spark job scheduler started")
        
        # Run scheduler loop
        while self.scheduler_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop_scheduler(self):
        """Stop the job scheduler"""
        logger.info("🛑 Stopping Spark job scheduler...")
        self.scheduler_running = False
        if schedule_available:
            schedule.clear()
        logger.info("✅ Spark job scheduler stopped")
    
    # Default job implementations
    
    def _quantum_resonance_job(self) -> Dict[str, Any]:
        """Hourly quantum resonance analysis job"""
        # Generate sample quantum data (in production, fetch from database)
        sample_data = self._generate_sample_quantum_data(100)
        return self.spark_processor.analyze_quantum_resonance(sample_data)
    
    def _payment_analytics_job(self) -> Dict[str, Any]:
        """Daily payment analytics job"""
        # Generate sample payment data (in production, fetch from database)
        sample_data = self._generate_sample_payment_data(50)
        return self.spark_processor.analyze_payment_patterns(sample_data)
    
    def _ethical_coherence_job(self) -> Dict[str, Any]:
        """Daily ethical coherence assessment job"""
        # Generate sample audit data (in production, fetch from database)
        sample_data = self._generate_sample_audit_data(30)
        return self.spark_processor.compute_ethical_coherence_matrix(sample_data)
    
    def _trinity_report_job(self) -> Dict[str, Any]:
        """Weekly Sacred Trinity comprehensive report job"""
        quantum_data = self._generate_sample_quantum_data(500)
        payment_data = self._generate_sample_payment_data(200)
        audit_data = self._generate_sample_audit_data(100)
        
        return self.spark_processor.generate_sacred_trinity_report(
            quantum_data, payment_data, audit_data
        )
    
    # Sample data generators (for testing - replace with database queries in production)
    
    def _generate_sample_quantum_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate sample quantum resonance data"""
        import random
        phases = ["foundation", "growth", "harmony", "transcendence"]
        
        data = []
        for i in range(count):
            data.append({
                "transaction_id": f"tx_{i}_{int(time.time())}",
                "user_id": f"user_{random.randint(1, 20)}",
                "amount": random.uniform(1.0, 100.0),
                "resonance_level": random.uniform(0.3, 1.0),
                "quantum_phase": random.choice(phases),
                "timestamp": datetime.now() - timedelta(hours=random.randint(0, 24)),
                "ethical_score": random.uniform(300, 900),
                "coherence_score": random.uniform(0.5, 1.0),
            })
        return data
    
    def _generate_sample_payment_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate sample payment data"""
        import random
        
        data = []
        for i in range(count):
            data.append({
                "payment_id": f"pay_{i}_{int(time.time())}",
                "user_id": f"user_{random.randint(1, 20)}",
                "amount": random.uniform(1.0, 50.0),
                "timestamp": datetime.now() - timedelta(hours=random.randint(0, 168)),  # Last week
                "status": "completed",
            })
        return data
    
    def _generate_sample_audit_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate sample ethical audit data"""
        import random
        
        data = []
        for i in range(count):
            data.append({
                "audit_id": f"audit_{i}_{int(time.time())}",
                "transaction_id": f"tx_{i}",
                "ethical_score": random.uniform(300, 900),
                "verity_score": random.uniform(50, 100),
                "qualia_score": random.uniform(50, 100),
                "timestamp": datetime.now() - timedelta(hours=random.randint(0, 168)),
            })
        return data
    
    def shutdown(self):
        """Shutdown orchestrator and Spark processor"""
        logger.info("🛑 Shutting down Spark Job Orchestrator...")
        self.stop_scheduler()
        if self.spark_processor:
            self.spark_processor.stop()
        logger.info("✅ Spark Job Orchestrator shutdown complete")


# Singleton instance
_orchestrator: Optional[SparkJobOrchestrator] = None


def get_spark_orchestrator() -> SparkJobOrchestrator:
    """Get or create singleton orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = SparkJobOrchestrator()
    return _orchestrator
