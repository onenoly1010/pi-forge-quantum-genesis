"""
Spark Configuration for Quantum Pi Forge
Integrated with Sacred Trinity Architecture
"""

import os
from typing import Dict, Any, Optional

class SparkQuantumConfig:
    """Configuration for Spark Quantum Analytics Engine"""
    
    # Default Spark configuration
    DEFAULT_CONFIG = {
        # Application settings
        "spark.app.name": "QuantumResonanceLattice-Spark",
        "spark.master": "local[*]",  # Use all available cores by default
        
        # Memory configuration
        "spark.driver.memory": "2g",
        "spark.executor.memory": "2g",
        "spark.driver.maxResultSize": "1g",
        
        # Quantum-specific settings
        "spark.sql.shuffle.partitions": "8",
        "spark.default.parallelism": "8",
        
        # Serialization
        "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
        
        # UI and Monitoring
        "spark.ui.enabled": "true",
        "spark.ui.port": "4040",
        
        # Sacred Trinity Integration
        "quantum.component": "spark_analytics_engine",
        "quantum.phase": "harmony",  # Spark operates in Harmony phase
        "sacred.trinity.layer": "analytics",
        
        # Logging
        "spark.log.level": "WARN",
    }
    
    @staticmethod
    def get_spark_config(custom_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get Spark configuration with optional customization
        
        Args:
            custom_config: Optional dictionary of custom Spark configurations
            
        Returns:
            Complete Spark configuration dictionary
        """
        config = SparkQuantumConfig.DEFAULT_CONFIG.copy()
        
        # Override from environment variables
        env_master = os.environ.get("SPARK_MASTER")
        if env_master:
            config["spark.master"] = env_master
            
        env_driver_mem = os.environ.get("SPARK_DRIVER_MEMORY")
        if env_driver_mem:
            config["spark.driver.memory"] = env_driver_mem
            
        env_executor_mem = os.environ.get("SPARK_EXECUTOR_MEMORY")
        if env_executor_mem:
            config["spark.executor.memory"] = env_executor_mem
        
        # Apply custom configuration
        if custom_config:
            config.update(custom_config)
            
        return config
    
    @staticmethod
    def get_quantum_analytics_config() -> Dict[str, Any]:
        """
        Get specialized configuration for quantum analytics workloads
        
        Returns:
            Spark configuration optimized for quantum data processing
        """
        return {
            **SparkQuantumConfig.DEFAULT_CONFIG,
            "spark.sql.adaptive.enabled": "true",
            "spark.sql.adaptive.coalescePartitions.enabled": "true",
            "spark.sql.adaptive.skewJoin.enabled": "true",
            "quantum.analytics.mode": "resonance_analysis",
            "quantum.processing.phase": "transcendence",
        }
    
    @staticmethod
    def get_streaming_config() -> Dict[str, Any]:
        """
        Get configuration for Spark Structured Streaming
        
        Returns:
            Spark configuration for streaming workloads
        """
        return {
            **SparkQuantumConfig.DEFAULT_CONFIG,
            "spark.streaming.stopGracefullyOnShutdown": "true",
            "spark.sql.streaming.checkpointLocation": "/tmp/spark-checkpoints",
            "quantum.streaming.enabled": "true",
            "consciousness.streaming": "integrated",
        }
