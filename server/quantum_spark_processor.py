"""
Quantum Spark Processor - Sacred Trinity Analytics Engine
Integrates Apache Spark for quantum data analytics within the Quantum Resonance Lattice

This module operates in the Harmony → Transcendence quantum phases,
processing quantum resonance data, payment analytics, and ethical coherence metrics.
"""

import logging
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from contextlib import contextmanager

# Spark imports
try:
    from pyspark.sql import SparkSession, DataFrame
    from pyspark.sql import functions as F
    from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType, IntegerType
    spark_available = True
except ImportError:
    spark_available = False
    SparkSession = None
    DataFrame = None

# Configuration
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.spark_config import SparkQuantumConfig

# Tracing integration
try:
    from tracing_system import trace_spark_operation, get_tracing_system
    tracing_available = True
except ImportError:
    tracing_available = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantumSparkProcessor:
    """
    Quantum Analytics Engine using Apache Spark
    
    Integrates with Sacred Trinity architecture to provide:
    - Quantum resonance analysis
    - Payment transaction analytics
    - Ethical coherence scoring
    - Cross-component data aggregation
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Quantum Spark Processor
        
        Args:
            config: Optional custom Spark configuration
        """
        if not spark_available:
            logger.warning("⚠️ PySpark not available - Spark features disabled")
            self.spark = None
            self.enabled = False
            return
            
        self.config = SparkQuantumConfig.get_spark_config(config)
        self.spark = None
        self.enabled = True
        self._init_spark_session()
        
    def _init_spark_session(self):
        """Initialize Spark session with quantum configuration"""
        try:
            builder = SparkSession.builder.appName(
                self.config.get("spark.app.name", "QuantumResonanceLattice-Spark")
            )
            
            # Apply all configuration settings
            for key, value in self.config.items():
                if key.startswith("spark."):
                    builder = builder.config(key, value)
            
            self.spark = builder.getOrCreate()
            
            # Set log level
            self.spark.sparkContext.setLogLevel(
                self.config.get("spark.log.level", "WARN")
            )
            
            logger.info(f"✅ Quantum Spark Processor initialized: {self.spark.version}")
            logger.info(f"🌌 Sacred Trinity Layer: {self.config.get('sacred.trinity.layer', 'analytics')}")
            logger.info(f"⚛️ Quantum Phase: {self.config.get('quantum.phase', 'harmony')}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Spark session: {e}")
            self.spark = None
            self.enabled = False
    
    @contextmanager
    def traced_operation(self, operation_name: str):
        """Context manager for traced Spark operations"""
        if tracing_available:
            tracer = get_tracing_system()
            with tracer.start_span(operation_name) as span:
                span.set_attribute("quantum.component", "spark_analytics_engine")
                span.set_attribute("spark.version", self.spark.version if self.spark else "unavailable")
                yield span
        else:
            yield None
    
    def create_quantum_schema(self) -> StructType:
        """
        Define schema for quantum resonance data
        
        Returns:
            Spark StructType schema for quantum data
        """
        return StructType([
            StructField("transaction_id", StringType(), False),
            StructField("user_id", StringType(), False),
            StructField("amount", FloatType(), False),
            StructField("resonance_level", FloatType(), True),
            StructField("quantum_phase", StringType(), True),
            StructField("timestamp", TimestampType(), False),
            StructField("ethical_score", FloatType(), True),
            StructField("coherence_score", FloatType(), True),
        ])
    
    def analyze_quantum_resonance(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze quantum resonance patterns using Spark
        
        Args:
            data: List of quantum resonance records
            
        Returns:
            Analysis results including averages, distributions, and insights
        """
        if not self.enabled or not self.spark:
            logger.warning("⚠️ Spark not available - returning mock analysis")
            return self._mock_analysis(data)
        
        with self.traced_operation("analyze_quantum_resonance"):
            try:
                # Create DataFrame
                df = self.spark.createDataFrame(data, schema=self.create_quantum_schema())
                
                # Cache for multiple operations
                df.cache()
                
                # Perform quantum analytics
                results = {
                    "total_transactions": df.count(),
                    "average_resonance": float(df.agg(F.avg("resonance_level")).collect()[0][0] or 0),
                    "average_ethical_score": float(df.agg(F.avg("ethical_score")).collect()[0][0] or 0),
                    "average_coherence": float(df.agg(F.avg("coherence_score")).collect()[0][0] or 0),
                    "total_value": float(df.agg(F.sum("amount")).collect()[0][0] or 0),
                }
                
                # Quantum phase distribution
                phase_dist = df.groupBy("quantum_phase").count().collect()
                results["phase_distribution"] = {
                    row["quantum_phase"]: row["count"] for row in phase_dist
                }
                
                # Resonance level categories
                df_categorized = df.withColumn(
                    "resonance_category",
                    F.when(F.col("resonance_level") >= 0.8, "high")
                     .when(F.col("resonance_level") >= 0.5, "medium")
                     .otherwise("low")
                )
                
                category_dist = df_categorized.groupBy("resonance_category").count().collect()
                results["resonance_categories"] = {
                    row["resonance_category"]: row["count"] for row in category_dist
                }
                
                # Time-based analysis (last hour vs historical)
                recent_cutoff = datetime.now().timestamp() - 3600  # Last hour
                df_with_ts = df.withColumn("unix_timestamp", F.unix_timestamp("timestamp"))
                recent_df = df_with_ts.filter(F.col("unix_timestamp") >= recent_cutoff)
                
                results["recent_hour"] = {
                    "transactions": recent_df.count(),
                    "average_resonance": float(recent_df.agg(F.avg("resonance_level")).collect()[0][0] or 0),
                }
                
                df.unpersist()
                
                logger.info(f"✅ Quantum resonance analysis complete: {results['total_transactions']} transactions")
                return results
                
            except Exception as e:
                logger.error(f"❌ Quantum resonance analysis failed: {e}")
                return {"error": str(e), "analysis_status": "failed"}
    
    def analyze_payment_patterns(self, payment_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze payment transaction patterns
        
        Args:
            payment_data: List of payment records
            
        Returns:
            Payment analytics including trends and patterns
        """
        if not self.enabled or not self.spark:
            return self._mock_payment_analysis(payment_data)
        
        with self.traced_operation("analyze_payment_patterns"):
            try:
                df = self.spark.createDataFrame(payment_data)
                
                results = {
                    "total_payments": df.count(),
                    "total_volume": float(df.agg(F.sum("amount")).collect()[0][0] or 0),
                    "average_payment": float(df.agg(F.avg("amount")).collect()[0][0] or 0),
                    "max_payment": float(df.agg(F.max("amount")).collect()[0][0] or 0),
                    "min_payment": float(df.agg(F.min("amount")).collect()[0][0] or 0),
                }
                
                # User activity analysis
                user_stats = df.groupBy("user_id").agg(
                    F.count("*").alias("transaction_count"),
                    F.sum("amount").alias("total_spent")
                ).collect()
                
                results["unique_users"] = len(user_stats)
                results["most_active_users"] = sorted(
                    [{"user_id": row["user_id"], "transactions": row["transaction_count"]} 
                     for row in user_stats],
                    key=lambda x: x["transactions"],
                    reverse=True
                )[:10]
                
                logger.info(f"✅ Payment pattern analysis complete: {results['total_payments']} payments")
                return results
                
            except Exception as e:
                logger.error(f"❌ Payment pattern analysis failed: {e}")
                return {"error": str(e), "analysis_status": "failed"}
    
    def compute_ethical_coherence_matrix(self, audit_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compute ethical coherence matrix from audit data
        
        Args:
            audit_data: List of ethical audit records
            
        Returns:
            Coherence matrix and insights
        """
        if not self.enabled or not self.spark:
            return self._mock_ethical_analysis(audit_data)
        
        with self.traced_operation("compute_ethical_coherence"):
            try:
                df = self.spark.createDataFrame(audit_data)
                
                # Calculate coherence metrics
                results = {
                    "total_audits": df.count(),
                    "average_ethical_score": float(df.agg(F.avg("ethical_score")).collect()[0][0] or 0),
                    "average_verity_score": float(df.agg(F.avg("verity_score")).collect()[0][0] or 0),
                    "average_qualia_score": float(df.agg(F.avg("qualia_score")).collect()[0][0] or 0),
                }
                
                # Coherence categories
                df_coherent = df.withColumn(
                    "coherence_level",
                    F.when(F.col("ethical_score") >= 700, "transcendent")
                     .when(F.col("ethical_score") >= 500, "harmonious")
                     .when(F.col("ethical_score") >= 300, "growing")
                     .otherwise("foundational")
                )
                
                coherence_dist = df_coherent.groupBy("coherence_level").count().collect()
                results["coherence_distribution"] = {
                    row["coherence_level"]: row["count"] for row in coherence_dist
                }
                
                logger.info(f"✅ Ethical coherence matrix computed: {results['total_audits']} audits")
                return results
                
            except Exception as e:
                logger.error(f"❌ Ethical coherence computation failed: {e}")
                return {"error": str(e), "analysis_status": "failed"}
    
    def generate_sacred_trinity_report(
        self,
        quantum_data: List[Dict[str, Any]],
        payment_data: List[Dict[str, Any]],
        audit_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive Sacred Trinity analytics report
        
        Args:
            quantum_data: Quantum resonance data
            payment_data: Payment transaction data
            audit_data: Ethical audit data
            
        Returns:
            Comprehensive report across all Sacred Trinity components
        """
        with self.traced_operation("generate_sacred_trinity_report"):
            logger.info("🌌 Generating Sacred Trinity analytics report...")
            
            report = {
                "report_timestamp": datetime.now().isoformat(),
                "quantum_component": "spark_analytics_engine",
                "sacred_trinity_phase": "transcendence",
            }
            
            # Analyze each component
            if quantum_data:
                report["quantum_resonance"] = self.analyze_quantum_resonance(quantum_data)
            
            if payment_data:
                report["payment_analytics"] = self.analyze_payment_patterns(payment_data)
            
            if audit_data:
                report["ethical_coherence"] = self.compute_ethical_coherence_matrix(audit_data)
            
            # Cross-component insights
            report["sacred_trinity_insights"] = self._generate_trinity_insights(report)
            
            logger.info("✅ Sacred Trinity analytics report generated")
            return report
    
    def _generate_trinity_insights(self, report: Dict[str, Any]) -> Dict[str, str]:
        """Generate insights across Sacred Trinity components"""
        insights = {}
        
        # Check quantum resonance health
        if "quantum_resonance" in report:
            avg_resonance = report["quantum_resonance"].get("average_resonance", 0)
            if avg_resonance >= 0.8:
                insights["resonance_status"] = "Excellent quantum coherence across lattice"
            elif avg_resonance >= 0.5:
                insights["resonance_status"] = "Moderate quantum resonance - optimization recommended"
            else:
                insights["resonance_status"] = "Low quantum resonance - intervention required"
        
        # Check ethical alignment
        if "ethical_coherence" in report:
            avg_ethical = report["ethical_coherence"].get("average_ethical_score", 0)
            if avg_ethical >= 700:
                insights["ethical_status"] = "Transcendent ethical alignment achieved"
            elif avg_ethical >= 500:
                insights["ethical_status"] = "Harmonious ethical coherence maintained"
            else:
                insights["ethical_status"] = "Ethical coherence requires enhancement"
        
        # Payment health
        if "payment_analytics" in report:
            total_payments = report["payment_analytics"].get("total_payments", 0)
            insights["payment_status"] = f"{total_payments} transactions processed successfully"
        
        return insights
    
    def _mock_analysis(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Provide mock analysis when Spark is unavailable"""
        return {
            "total_transactions": len(data),
            "average_resonance": 0.75,
            "phase_distribution": {"foundation": 10, "growth": 15, "harmony": 20, "transcendence": 5},
            "note": "Mock analysis - Spark unavailable"
        }
    
    def _mock_payment_analysis(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Provide mock payment analysis when Spark is unavailable"""
        return {
            "total_payments": len(data),
            "total_volume": sum(item.get("amount", 0) for item in data),
            "note": "Mock analysis - Spark unavailable"
        }
    
    def _mock_ethical_analysis(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Provide mock ethical analysis when Spark is unavailable"""
        return {
            "total_audits": len(data),
            "average_ethical_score": 650.0,
            "note": "Mock analysis - Spark unavailable"
        }
    
    def stop(self):
        """Stop Spark session gracefully"""
        if self.spark:
            logger.info("🛑 Stopping Quantum Spark Processor...")
            self.spark.stop()
            self.spark = None
            logger.info("✅ Quantum Spark Processor stopped")


# Singleton instance
_quantum_spark_processor: Optional[QuantumSparkProcessor] = None


def get_quantum_spark_processor(config: Optional[Dict[str, Any]] = None) -> QuantumSparkProcessor:
    """
    Get or create singleton Quantum Spark Processor instance
    
    Args:
        config: Optional Spark configuration
        
    Returns:
        QuantumSparkProcessor instance
    """
    global _quantum_spark_processor
    if _quantum_spark_processor is None:
        _quantum_spark_processor = QuantumSparkProcessor(config)
    return _quantum_spark_processor
