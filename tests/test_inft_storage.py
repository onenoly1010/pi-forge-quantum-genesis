"""
Tests for iNFT Memory Schema and Services

Tests the database schema, logic gates, sync services, and API endpoints
for the intelligent NFT memory layer.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add server directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))

from inft_storage.services.logic_gates import (
    calculate_consciousness_score,
    should_transition_phase,
    evaluate_interaction_complexity,
    check_memory_health
)


class TestConsciousnessCalculation:
    """Tests for consciousness score calculation"""
    
    def test_basic_consciousness_score(self):
        """Test basic consciousness score calculation"""
        score = calculate_consciousness_score(
            interaction_count=150,
            avg_sentiment=0.7,
            session_count=15,
            oracle_query_count=25,
            days_active=14
        )
        
        assert 0 <= score <= 1, "Score should be between 0 and 1"
        assert isinstance(score, float), "Score should be a float"
        assert score > 0, "Score should be positive with activity"
    
    def test_zero_activity_consciousness(self):
        """Test consciousness score with no activity"""
        score = calculate_consciousness_score(
            interaction_count=0,
            avg_sentiment=0.0,
            session_count=0,
            oracle_query_count=0,
            days_active=0
        )
        
        assert score >= 0.0, "Score should be non-negative"
        assert score <= 0.2, "Score should be very low with no activity"
    
    def test_high_activity_consciousness(self):
        """Test consciousness score with high activity"""
        high_score = calculate_consciousness_score(
            interaction_count=1000,
            avg_sentiment=0.9,
            session_count=100,
            oracle_query_count=200,
            days_active=365
        )
        
        low_score = calculate_consciousness_score(
            interaction_count=10,
            avg_sentiment=0.1,
            session_count=1,
            oracle_query_count=0,
            days_active=1
        )
        
        assert high_score > low_score, "High activity should score higher"
        assert high_score > 0.7, "High activity should achieve high score"
    
    def test_negative_sentiment_handling(self):
        """Test consciousness score with negative sentiment"""
        score = calculate_consciousness_score(
            interaction_count=100,
            avg_sentiment=-0.5,  # Negative sentiment
            session_count=10,
            oracle_query_count=10,
            days_active=10
        )
        
        assert 0 <= score <= 1, "Negative sentiment should still give valid score"
    
    def test_custom_complexity_score(self):
        """Test consciousness score with custom complexity"""
        score_with_complexity = calculate_consciousness_score(
            interaction_count=100,
            avg_sentiment=0.5,
            session_count=10,
            oracle_query_count=10,
            days_active=10,
            complexity_score=0.9
        )
        
        score_without_complexity = calculate_consciousness_score(
            interaction_count=100,
            avg_sentiment=0.5,
            session_count=10,
            oracle_query_count=10,
            days_active=10
        )
        
        assert score_with_complexity != score_without_complexity


class TestPhaseTransitions:
    """Tests for phase transition logic"""
    
    def test_awakening_to_evolving_not_ready(self):
        """Test transition from awakening that's not ready"""
        should_trans, target, confidence, condition = should_transition_phase(
            current_phase="awakening",
            consciousness_score=0.3,  # Below threshold
            interaction_count=50,     # Below threshold
            session_count=5,          # Below threshold
            last_transition_days=3    # Below threshold
        )
        
        assert should_trans is False, "Should not transition with low metrics"
        assert target is None, "No target phase when not ready"
        assert confidence == 0.0, "Confidence should be 0 when not ready"
        assert "criteria_not_met" in condition
    
    def test_awakening_to_evolving_ready(self):
        """Test successful transition from awakening to evolving"""
        should_trans, target, confidence, condition = should_transition_phase(
            current_phase="awakening",
            consciousness_score=0.6,   # Above threshold (0.5)
            interaction_count=150,     # Above threshold (100)
            session_count=15,          # Above threshold (10)
            last_transition_days=10    # Above threshold (7)
        )
        
        assert should_trans is True, "Should transition with sufficient metrics"
        assert target == "evolving", "Target phase should be evolving"
        assert 0 <= confidence <= 1, "Confidence should be valid"
        assert "consciousness" in condition
    
    def test_evolving_to_transcendent_ready(self):
        """Test transition from evolving to transcendent"""
        should_trans, target, confidence, condition = should_transition_phase(
            current_phase="evolving",
            consciousness_score=0.8,   # Above threshold (0.75)
            interaction_count=600,     # Above threshold (500)
            session_count=60,          # Above threshold (50)
            last_transition_days=35    # Above threshold (30)
        )
        
        assert should_trans is True, "Should transition to transcendent"
        assert target == "transcendent", "Target should be transcendent"
    
    def test_transcendent_no_further_transition(self):
        """Test that transcendent is final phase"""
        should_trans, target, confidence, condition = should_transition_phase(
            current_phase="transcendent",
            consciousness_score=0.95,
            interaction_count=1000,
            session_count=100,
            last_transition_days=100
        )
        
        assert should_trans is False, "Transcendent should not transition further"
        assert target is None, "No target phase from transcendent"
        assert condition == "already_transcendent"
    
    def test_high_confidence_auto_approval(self):
        """Test that high confidence enables auto-approval"""
        should_trans, target, confidence, condition = should_transition_phase(
            current_phase="awakening",
            consciousness_score=0.8,   # Well above threshold
            interaction_count=300,     # Well above threshold
            session_count=40,          # Well above threshold
            last_transition_days=20,   # Well above threshold
            min_confidence=0.75
        )
        
        assert should_trans is True
        assert confidence >= 0.75, "High metrics should give high confidence"
    
    def test_unknown_phase_handling(self):
        """Test handling of unknown phase"""
        should_trans, target, confidence, condition = should_transition_phase(
            current_phase="unknown_phase",
            consciousness_score=0.8,
            interaction_count=200,
            session_count=20,
            last_transition_days=10
        )
        
        assert should_trans is False, "Unknown phase should not transition"
        assert condition == "unknown_phase"


class TestInteractionComplexity:
    """Tests for interaction complexity evaluation"""
    
    def test_empty_events(self):
        """Test complexity with no events"""
        complexity = evaluate_interaction_complexity([])
        assert complexity == 0.0, "No events should give 0 complexity"
    
    def test_single_event_type(self):
        """Test complexity with single event type (low diversity)"""
        events = [
            {"event_type": "click", "event_subtype": "button"},
            {"event_type": "click", "event_subtype": "button"},
            {"event_type": "click", "event_subtype": "button"},
        ]
        
        complexity = evaluate_interaction_complexity(events)
        assert complexity < 0.5, "Single type should have low complexity"
    
    def test_diverse_events(self):
        """Test complexity with diverse event types"""
        events = [
            {"event_type": "interaction", "event_subtype": "message"},
            {"event_type": "state_change", "event_subtype": "phase"},
            {"event_type": "oracle_query", "event_subtype": "price"},
            {"event_type": "allocation", "event_subtype": "transfer"},
            {"event_type": "interaction", "event_subtype": "reaction"},
        ]
        
        complexity = evaluate_interaction_complexity(events)
        assert complexity > 0.3, "Diverse events should have higher complexity"
    
    def test_pattern_diversity(self):
        """Test that pattern changes increase complexity"""
        varied_events = [
            {"event_type": "type1"},
            {"event_type": "type2"},
            {"event_type": "type3"},
            {"event_type": "type1"},
            {"event_type": "type2"},
        ]
        
        repetitive_events = [
            {"event_type": "type1"},
            {"event_type": "type1"},
            {"event_type": "type1"},
            {"event_type": "type1"},
            {"event_type": "type1"},
        ]
        
        varied_complexity = evaluate_interaction_complexity(varied_events)
        repetitive_complexity = evaluate_interaction_complexity(repetitive_events)
        
        assert varied_complexity > repetitive_complexity, "Varied patterns should be more complex"


class TestMemoryHealth:
    """Tests for memory health checking"""
    
    def test_healthy_memory(self):
        """Test health check with healthy memory state"""
        state_data = {
            "id": "inft_test",
            "memory_checksum": "abc123",
            "updated_at": int(datetime.now().timestamp())
        }
        
        health = check_memory_health(
            state_data=state_data,
            event_count=100,
            session_count=10,
            last_sync_age_hours=1
        )
        
        assert health["health_status"] == "healthy", "Should be healthy"
        assert len(health["issues"]) == 0, "Should have no issues"
        assert len(health["warnings"]) == 0, "Should have no warnings"
    
    def test_stale_sync_warning(self):
        """Test warning for stale 0G sync"""
        state_data = {
            "id": "inft_test",
            "memory_checksum": "abc123",
            "updated_at": int(datetime.now().timestamp())
        }
        
        health = check_memory_health(
            state_data=state_data,
            event_count=100,
            session_count=10,
            last_sync_age_hours=48  # 2 days old
        )
        
        assert health["health_status"] == "degraded", "Should be degraded"
        assert len(health["warnings"]) > 0, "Should have warnings"
        assert any("sync" in w.lower() for w in health["warnings"])
    
    def test_missing_checksum_issue(self):
        """Test issue detection for missing checksum"""
        state_data = {
            "id": "inft_test",
            # No memory_checksum
            "updated_at": int(datetime.now().timestamp())
        }
        
        health = check_memory_health(
            state_data=state_data,
            event_count=100,
            session_count=10,
            last_sync_age_hours=1
        )
        
        assert health["health_status"] == "unhealthy", "Should be unhealthy"
        assert len(health["issues"]) > 0, "Should have issues"
        assert any("checksum" in i.lower() for i in health["issues"])
    
    def test_inactive_warning(self):
        """Test warning for inactive iNFT"""
        old_timestamp = int(datetime.now().timestamp()) - (40 * 86400)  # 40 days ago
        state_data = {
            "id": "inft_test",
            "memory_checksum": "abc123",
            "updated_at": old_timestamp
        }
        
        health = check_memory_health(
            state_data=state_data,
            event_count=100,
            session_count=10,
            last_sync_age_hours=1
        )
        
        assert len(health["warnings"]) > 0, "Should have inactivity warning"
        assert health["days_inactive"] > 30, "Should detect inactivity"
    
    def test_events_per_session_calculation(self):
        """Test events per session metric"""
        state_data = {
            "id": "inft_test",
            "memory_checksum": "abc123",
            "updated_at": int(datetime.now().timestamp())
        }
        
        health = check_memory_health(
            state_data=state_data,
            event_count=200,
            session_count=10,
            last_sync_age_hours=1
        )
        
        assert health["events_per_session"] == 20.0, "Should calculate ratio correctly"


class TestSchemaValidation:
    """Tests for schema structure validation"""
    
    def test_sql_schema_file_exists(self):
        """Test that SQL schema file exists"""
        schema_path = Path(__file__).parent.parent / "server" / "inft_storage" / "schema" / "001_inft_memory_schema.sql"
        assert schema_path.exists(), "SQL schema file should exist"
    
    def test_sql_schema_has_all_tables(self):
        """Test that SQL schema contains all required tables"""
        schema_path = Path(__file__).parent.parent / "server" / "inft_storage" / "schema" / "001_inft_memory_schema.sql"
        schema_content = schema_path.read_text()
        
        required_tables = [
            "inft_state",
            "event_log",
            "state_transitions",
            "user_context",
            "memory_continuity",
            "oracle_queries",
            "ledger_allocations"
        ]
        
        for table in required_tables:
            assert f"CREATE TABLE IF NOT EXISTS {table}" in schema_content, \
                f"Schema should include {table} table"
    
    def test_sql_schema_has_indexes(self):
        """Test that SQL schema includes indexes"""
        schema_path = Path(__file__).parent.parent / "server" / "inft_storage" / "schema" / "001_inft_memory_schema.sql"
        schema_content = schema_path.read_text()
        
        assert "CREATE INDEX" in schema_content, "Schema should include indexes"
        assert schema_content.count("CREATE INDEX") >= 10, "Should have multiple indexes"
    
    def test_sql_schema_has_foreign_keys(self):
        """Test that SQL schema includes foreign keys"""
        schema_path = Path(__file__).parent.parent / "server" / "inft_storage" / "schema" / "001_inft_memory_schema.sql"
        schema_content = schema_path.read_text()
        
        assert "FOREIGN KEY" in schema_content, "Schema should include foreign keys"
        assert schema_content.count("FOREIGN KEY") >= 6, "Multiple tables should have foreign keys"


class TestModels:
    """Tests for Pydantic models"""
    
    def test_inft_state_model_validation(self):
        """Test INFTState model validation"""
        from inft_storage.models import INFTState
        
        state = INFTState(
            id="inft_test",
            owner_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
            consciousness_phase="awakening",
            creation_block=1000000,
            created_at=1704067200,
            updated_at=1704067200
        )
        
        assert state.id == "inft_test"
        assert state.consciousness_phase == "awakening"
        assert state.owner_address == "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1"
    
    def test_event_log_model_validation(self):
        """Test EventLog model validation"""
        from inft_storage.models import EventLog
        
        event = EventLog(
            event_id="evt_test",
            inft_id="inft_test",
            event_type="interaction",
            timestamp=1704067200
        )
        
        assert event.event_id == "evt_test"
        assert event.event_type == "interaction"
    
    def test_consciousness_phase_validation(self):
        """Test consciousness phase enum validation"""
        from inft_storage.models import INFTState
        from pydantic import ValidationError
        
        # Valid phases
        for phase in ["awakening", "evolving", "transcendent"]:
            state = INFTState(
                id="test",
                owner_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
                consciousness_phase=phase,
                creation_block=1,
                created_at=1,
                updated_at=1
            )
            assert state.consciousness_phase == phase


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
