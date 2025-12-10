"""
Tests for Spark Integration in Quantum Pi Forge
Tests quantum analytics processor, job orchestrator, and Sacred Trinity integration
"""

import pytest
import sys
import os
from datetime import datetime, timedelta
import random

# Add server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import modules to test
from config.spark_config import SparkQuantumConfig
from server.quantum_spark_processor import QuantumSparkProcessor, get_quantum_spark_processor
from server.spark_job_orchestrator import SparkJobOrchestrator, SparkJob, JobStatus, get_spark_orchestrator


class TestSparkConfiguration:
    """Test Spark configuration module"""
    
    def test_default_config(self):
        """Test default Spark configuration"""
        config = SparkQuantumConfig.get_spark_config()
        
        assert "spark.app.name" in config
        assert config["spark.app.name"] == "QuantumResonanceLattice-Spark"
        assert config["spark.master"] == "local[*]"
        assert config["quantum.component"] == "spark_analytics_engine"
        assert config["quantum.phase"] == "harmony"
    
    def test_custom_config_override(self):
        """Test custom configuration override"""
        custom = {"spark.driver.memory": "4g"}
        config = SparkQuantumConfig.get_spark_config(custom)
        
        assert config["spark.driver.memory"] == "4g"
        assert config["spark.app.name"] == "QuantumResonanceLattice-Spark"
    
    def test_quantum_analytics_config(self):
        """Test quantum analytics specialized config"""
        config = SparkQuantumConfig.get_quantum_analytics_config()
        
        assert config["spark.sql.adaptive.enabled"] == "true"
        assert config["quantum.analytics.mode"] == "resonance_analysis"
        assert config["quantum.processing.phase"] == "transcendence"
    
    def test_streaming_config(self):
        """Test streaming configuration"""
        config = SparkQuantumConfig.get_streaming_config()
        
        assert config["spark.streaming.stopGracefullyOnShutdown"] == "true"
        assert config["quantum.streaming.enabled"] == "true"
        assert config["consciousness.streaming"] == "integrated"


class TestQuantumSparkProcessor:
    """Test Quantum Spark Processor"""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance for testing"""
        return QuantumSparkProcessor()
    
    @pytest.fixture
    def sample_quantum_data(self):
        """Generate sample quantum resonance data"""
        phases = ["foundation", "growth", "harmony", "transcendence"]
        data = []
        
        for i in range(50):
            data.append({
                "transaction_id": f"test_tx_{i}",
                "user_id": f"user_{random.randint(1, 10)}",
                "amount": random.uniform(1.0, 100.0),
                "resonance_level": random.uniform(0.3, 1.0),
                "quantum_phase": random.choice(phases),
                "timestamp": datetime.now() - timedelta(hours=random.randint(0, 24)),
                "ethical_score": random.uniform(300, 900),
                "coherence_score": random.uniform(0.5, 1.0),
            })
        
        return data
    
    @pytest.fixture
    def sample_payment_data(self):
        """Generate sample payment data"""
        data = []
        
        for i in range(30):
            data.append({
                "payment_id": f"pay_{i}",
                "user_id": f"user_{random.randint(1, 10)}",
                "amount": random.uniform(1.0, 50.0),
                "timestamp": datetime.now() - timedelta(hours=random.randint(0, 168)),
                "status": "completed",
            })
        
        return data
    
    @pytest.fixture
    def sample_audit_data(self):
        """Generate sample ethical audit data"""
        data = []
        
        for i in range(20):
            data.append({
                "audit_id": f"audit_{i}",
                "transaction_id": f"tx_{i}",
                "ethical_score": random.uniform(300, 900),
                "verity_score": random.uniform(50, 100),
                "qualia_score": random.uniform(50, 100),
                "timestamp": datetime.now() - timedelta(hours=random.randint(0, 168)),
            })
        
        return data
    
    def test_processor_initialization(self, processor):
        """Test processor initializes correctly"""
        assert processor is not None
        # Processor may or may not be enabled depending on PySpark availability
        # Just verify it doesn't crash
    
    def test_singleton_pattern(self):
        """Test processor singleton pattern"""
        processor1 = get_quantum_spark_processor()
        processor2 = get_quantum_spark_processor()
        assert processor1 is processor2
    
    def test_quantum_schema_creation(self, processor):
        """Test quantum data schema creation"""
        schema = processor.create_quantum_schema()
        assert schema is not None
        
        # Check for expected fields
        field_names = [field.name for field in schema.fields]
        assert "transaction_id" in field_names
        assert "resonance_level" in field_names
        assert "quantum_phase" in field_names
        assert "ethical_score" in field_names
    
    def test_quantum_resonance_analysis(self, processor, sample_quantum_data):
        """Test quantum resonance analysis"""
        results = processor.analyze_quantum_resonance(sample_quantum_data)
        
        assert results is not None
        assert "total_transactions" in results
        assert results["total_transactions"] == len(sample_quantum_data)
        
        # Check for expected metrics
        if processor.enabled:
            assert "average_resonance" in results
            assert "phase_distribution" in results
            assert "resonance_categories" in results
        else:
            # Mock analysis when Spark unavailable
            assert "note" in results or "average_resonance" in results
    
    def test_payment_pattern_analysis(self, processor, sample_payment_data):
        """Test payment pattern analysis"""
        results = processor.analyze_payment_patterns(sample_payment_data)
        
        assert results is not None
        assert "total_payments" in results
        assert results["total_payments"] == len(sample_payment_data)
        
        if processor.enabled:
            assert "total_volume" in results
            assert "average_payment" in results
            assert "unique_users" in results
    
    def test_ethical_coherence_matrix(self, processor, sample_audit_data):
        """Test ethical coherence matrix computation"""
        results = processor.compute_ethical_coherence_matrix(sample_audit_data)
        
        assert results is not None
        assert "total_audits" in results
        assert results["total_audits"] == len(sample_audit_data)
        
        if processor.enabled:
            assert "average_ethical_score" in results
            assert "average_verity_score" in results
            assert "coherence_distribution" in results
    
    def test_sacred_trinity_report(self, processor, sample_quantum_data, 
                                   sample_payment_data, sample_audit_data):
        """Test comprehensive Sacred Trinity report generation"""
        results = processor.generate_sacred_trinity_report(
            quantum_data=sample_quantum_data,
            payment_data=sample_payment_data,
            audit_data=sample_audit_data
        )
        
        assert results is not None
        assert "report_timestamp" in results
        assert "quantum_component" in results
        assert results["quantum_component"] == "spark_analytics_engine"
        assert "sacred_trinity_phase" in results
        
        # Check component analytics
        assert "quantum_resonance" in results
        assert "payment_analytics" in results
        assert "ethical_coherence" in results
        assert "sacred_trinity_insights" in results


class TestSparkJobOrchestrator:
    """Test Spark Job Orchestrator"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance for testing"""
        return SparkJobOrchestrator()
    
    def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initializes with default jobs"""
        assert orchestrator is not None
        assert len(orchestrator.jobs) > 0
        
        # Check default jobs exist
        assert "quantum_resonance_hourly" in orchestrator.jobs
        assert "payment_analytics_daily" in orchestrator.jobs
        assert "ethical_coherence_daily" in orchestrator.jobs
        assert "trinity_report_weekly" in orchestrator.jobs
    
    def test_singleton_pattern(self):
        """Test orchestrator singleton pattern"""
        orch1 = get_spark_orchestrator()
        orch2 = get_spark_orchestrator()
        assert orch1 is orch2
    
    def test_job_registration(self, orchestrator):
        """Test custom job registration"""
        def test_job():
            return {"status": "success"}
        
        job = orchestrator.register_job(
            job_id="test_custom_job",
            name="Test Custom Job",
            job_function=test_job,
            schedule_interval="daily",
            description="Test job description"
        )
        
        assert job is not None
        assert job.job_id == "test_custom_job"
        assert job.name == "Test Custom Job"
        assert job.status == JobStatus.PENDING
        assert "test_custom_job" in orchestrator.jobs
    
    def test_list_jobs(self, orchestrator):
        """Test listing all jobs"""
        jobs = orchestrator.list_jobs()
        
        assert isinstance(jobs, list)
        assert len(jobs) > 0
        
        # Check job structure
        job = jobs[0]
        assert "job_id" in job
        assert "name" in job
        assert "status" in job
        assert "schedule_interval" in job
    
    def test_get_job_status(self, orchestrator):
        """Test getting job status"""
        status = orchestrator.get_job_status("quantum_resonance_hourly")
        
        assert status is not None
        assert status["job_id"] == "quantum_resonance_hourly"
        assert "status" in status
        assert "run_count" in status
        assert "error_count" in status
    
    def test_run_job(self, orchestrator):
        """Test running a job"""
        # Register a simple test job
        def simple_job():
            return {"test": "success"}
        
        orchestrator.register_job(
            job_id="test_run_job",
            name="Test Run Job",
            job_function=simple_job
        )
        
        # Run the job
        result = orchestrator.run_job("test_run_job")
        
        assert result is not None
        assert "status" in result
        assert "execution_time" in result
        
        # Verify job was executed
        status = orchestrator.get_job_status("test_run_job")
        assert status["run_count"] >= 1
    
    def test_run_nonexistent_job(self, orchestrator):
        """Test running a job that doesn't exist"""
        result = orchestrator.run_job("nonexistent_job_id")
        
        assert "error" in result


class TestSparkJob:
    """Test individual Spark job"""
    
    def test_job_creation(self):
        """Test job creation"""
        def test_func():
            return {"result": "success"}
        
        job = SparkJob(
            job_id="test_job",
            name="Test Job",
            job_function=test_func,
            schedule_interval="hourly",
            description="Test description"
        )
        
        assert job.job_id == "test_job"
        assert job.name == "Test Job"
        assert job.status == JobStatus.PENDING
        assert job.run_count == 0
        assert job.error_count == 0
    
    def test_job_execution_success(self):
        """Test successful job execution"""
        def success_func():
            return {"result": "success", "value": 42}
        
        job = SparkJob(
            job_id="success_job",
            name="Success Job",
            job_function=success_func
        )
        
        result = job.execute()
        
        assert result["status"] == "success"
        assert "execution_time" in result
        assert job.status == JobStatus.COMPLETED
        assert job.run_count == 1
        assert job.error_count == 0
    
    def test_job_execution_failure(self):
        """Test failed job execution"""
        def failing_func():
            raise ValueError("Test error")
        
        job = SparkJob(
            job_id="failing_job",
            name="Failing Job",
            job_function=failing_func
        )
        
        result = job.execute()
        
        assert result["status"] == "failed"
        assert "error" in result
        assert job.status == JobStatus.FAILED
        assert job.error_count == 1
    
    def test_job_to_dict(self):
        """Test job serialization to dictionary"""
        def test_func():
            return {}
        
        job = SparkJob(
            job_id="dict_test_job",
            name="Dict Test Job",
            job_function=test_func,
            schedule_interval="daily"
        )
        
        job_dict = job.to_dict()
        
        assert job_dict["job_id"] == "dict_test_job"
        assert job_dict["name"] == "Dict Test Job"
        assert job_dict["schedule_interval"] == "daily"
        assert job_dict["status"] == "pending"
        assert job_dict["run_count"] == 0


class TestSacredTrinityIntegration:
    """Test Sacred Trinity integration"""
    
    def test_quantum_phase_alignment(self):
        """Test that Spark operates in correct quantum phases"""
        config = SparkQuantumConfig.get_spark_config()
        
        # Spark should operate in Harmony phase
        assert config["quantum.phase"] == "harmony"
        assert config["sacred.trinity.layer"] == "analytics"
    
    def test_component_identification(self):
        """Test Sacred Trinity component identification"""
        config = SparkQuantumConfig.get_spark_config()
        
        assert config["quantum.component"] == "spark_analytics_engine"
    
    def test_analytics_report_structure(self):
        """Test Sacred Trinity report includes all components"""
        processor = QuantumSparkProcessor()
        
        # Create minimal sample data
        quantum_data = [{
            "transaction_id": "tx_1",
            "user_id": "user_1",
            "amount": 10.0,
            "resonance_level": 0.8,
            "quantum_phase": "harmony",
            "timestamp": datetime.now(),
            "ethical_score": 700.0,
            "coherence_score": 0.9,
        }]
        
        payment_data = [{
            "payment_id": "pay_1",
            "user_id": "user_1",
            "amount": 10.0,
            "timestamp": datetime.now(),
            "status": "completed",
        }]
        
        audit_data = [{
            "audit_id": "audit_1",
            "transaction_id": "tx_1",
            "ethical_score": 700.0,
            "verity_score": 80.0,
            "qualia_score": 75.0,
            "timestamp": datetime.now(),
        }]
        
        report = processor.generate_sacred_trinity_report(
            quantum_data, payment_data, audit_data
        )
        
        # Verify Sacred Trinity context
        assert report["quantum_component"] == "spark_analytics_engine"
        assert report["sacred_trinity_phase"] == "transcendence"
        assert "sacred_trinity_insights" in report


@pytest.mark.integration
class TestEndToEndWorkflow:
    """End-to-end integration tests"""
    
    def test_complete_analytics_workflow(self):
        """Test complete analytics workflow from job to results"""
        # Get orchestrator
        orchestrator = get_spark_orchestrator()
        
        # Run quantum resonance job
        result = orchestrator.run_job("quantum_resonance_hourly")
        
        # Verify execution
        assert result is not None
        if "error" not in result:
            assert "status" in result
            assert "result" in result or "error" in result
    
    def test_processor_lifecycle(self):
        """Test processor creation, use, and cleanup"""
        processor = QuantumSparkProcessor()
        
        try:
            # Use processor
            data = [{
                "transaction_id": "tx_lifecycle",
                "user_id": "user_lifecycle",
                "amount": 10.0,
                "resonance_level": 0.7,
                "quantum_phase": "harmony",
                "timestamp": datetime.now(),
                "ethical_score": 600.0,
                "coherence_score": 0.8,
            }]
            
            results = processor.analyze_quantum_resonance(data)
            assert results is not None
            
        finally:
            # Cleanup
            processor.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
