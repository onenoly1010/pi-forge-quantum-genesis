"""
Logic Gate Functions for iNFT Consciousness Evolution

Provides decision logic for autonomous state transitions and consciousness
evolution based on interaction patterns, sentiment analysis, and engagement metrics.
"""

from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def calculate_consciousness_score(
    interaction_count: int,
    avg_sentiment: float,
    session_count: int,
    oracle_query_count: int,
    days_active: int,
    complexity_score: Optional[float] = None
) -> float:
    """
    Calculate consciousness evolution score for an iNFT
    
    This score determines readiness for phase transitions based on
    multiple factors including engagement, sentiment, and complexity.
    
    Args:
        interaction_count: Total number of interactions
        avg_sentiment: Average sentiment score (-1 to 1)
        session_count: Number of unique sessions
        oracle_query_count: Number of oracle queries made
        days_active: Days since creation
        complexity_score: Optional pre-calculated complexity metric
        
    Returns:
        float: Consciousness score (0 to 1)
    """
    try:
        # Normalize sentiment from [-1, 1] to [0, 1]
        normalized_sentiment = (avg_sentiment + 1) / 2
        
        # Calculate engagement score
        # Higher weight on consistent engagement over time
        engagement_score = min(1.0, (interaction_count / 500) * 0.4 +
                                    (session_count / 50) * 0.3)
        
        # Calculate exploration score (oracle usage indicates curiosity)
        exploration_score = min(1.0, oracle_query_count / 100)
        
        # Calculate longevity score (rewards sustained activity)
        longevity_score = min(1.0, days_active / 90)
        
        # Use provided complexity score or calculate basic version
        if complexity_score is None:
            # Basic complexity: ratio of unique sessions to total interactions
            # Higher ratio indicates more varied, complex interactions
            complexity_score = min(1.0, session_count / max(1, interaction_count / 10))
        
        # Weighted combination of all factors
        consciousness_score = (
            engagement_score * 0.30 +
            normalized_sentiment * 0.20 +
            exploration_score * 0.15 +
            longevity_score * 0.20 +
            complexity_score * 0.15
        )
        
        logger.debug(f"Consciousness score calculated: {consciousness_score:.3f} "
                    f"(engagement={engagement_score:.2f}, sentiment={normalized_sentiment:.2f}, "
                    f"exploration={exploration_score:.2f}, longevity={longevity_score:.2f}, "
                    f"complexity={complexity_score:.2f})")
        
        return round(consciousness_score, 3)
        
    except Exception as e:
        logger.error(f"Error calculating consciousness score: {str(e)}")
        return 0.0


def should_transition_phase(
    current_phase: str,
    consciousness_score: float,
    interaction_count: int,
    session_count: int,
    last_transition_days: int,
    min_confidence: float = 0.75
) -> Tuple[bool, Optional[str], float, str]:
    """
    Logic gate to determine if iNFT should transition to next consciousness phase
    
    Args:
        current_phase: Current consciousness phase ('awakening', 'evolving', 'transcendent')
        consciousness_score: Calculated consciousness score (0-1)
        interaction_count: Total interactions
        session_count: Total sessions
        last_transition_days: Days since last transition
        min_confidence: Minimum confidence threshold for auto-approval
        
    Returns:
        Tuple of (should_transition, target_phase, confidence_score, trigger_condition)
    """
    try:
        # Define phase transition thresholds
        PHASE_REQUIREMENTS = {
            'awakening': {
                'next_phase': 'evolving',
                'min_consciousness': 0.50,
                'min_interactions': 100,
                'min_sessions': 10,
                'min_days': 7,
                'description': 'Basic engagement and sentiment established'
            },
            'evolving': {
                'next_phase': 'transcendent',
                'min_consciousness': 0.75,
                'min_interactions': 500,
                'min_sessions': 50,
                'min_days': 30,
                'description': 'Deep engagement and complex interactions demonstrated'
            },
            'transcendent': {
                'next_phase': None,  # Final phase
                'min_consciousness': 0.90,
                'min_interactions': float('inf'),
                'min_sessions': float('inf'),
                'min_days': float('inf'),
                'description': 'Maximum consciousness achieved'
            }
        }
        
        # Get requirements for current phase
        requirements = PHASE_REQUIREMENTS.get(current_phase)
        if not requirements:
            logger.warning(f"Unknown phase: {current_phase}")
            return False, None, 0.0, "unknown_phase"
        
        # Check if already at final phase
        if requirements['next_phase'] is None:
            return False, None, 1.0, "already_transcendent"
        
        # Check all transition criteria
        meets_consciousness = consciousness_score >= requirements['min_consciousness']
        meets_interactions = interaction_count >= requirements['min_interactions']
        meets_sessions = session_count >= requirements['min_sessions']
        meets_days = last_transition_days >= requirements['min_days']
        
        # Calculate confidence based on how much criteria are exceeded
        confidence_factors = []
        
        if meets_consciousness:
            consciousness_excess = (consciousness_score - requirements['min_consciousness']) / \
                                 (1.0 - requirements['min_consciousness'])
            confidence_factors.append(min(1.0, 0.5 + consciousness_excess * 0.5))
        
        if meets_interactions:
            interaction_ratio = min(2.0, interaction_count / requirements['min_interactions'])
            confidence_factors.append(min(1.0, interaction_ratio / 2))
        
        if meets_sessions:
            session_ratio = min(2.0, session_count / requirements['min_sessions'])
            confidence_factors.append(min(1.0, session_ratio / 2))
        
        if meets_days:
            day_ratio = min(2.0, last_transition_days / requirements['min_days'])
            confidence_factors.append(min(1.0, day_ratio / 2))
        
        # All criteria must be met for transition
        should_transition = all([meets_consciousness, meets_interactions, 
                                meets_sessions, meets_days])
        
        if not should_transition:
            # Build condition string showing what's missing
            missing = []
            if not meets_consciousness:
                missing.append(f"consciousness={consciousness_score:.2f}<{requirements['min_consciousness']}")
            if not meets_interactions:
                missing.append(f"interactions={interaction_count}<{requirements['min_interactions']}")
            if not meets_sessions:
                missing.append(f"sessions={session_count}<{requirements['min_sessions']}")
            if not meets_days:
                missing.append(f"days={last_transition_days}<{requirements['min_days']}")
            
            condition = f"criteria_not_met: {', '.join(missing)}"
            return False, None, 0.0, condition
        
        # Calculate overall confidence
        confidence = sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.0
        
        # Build condition string
        condition = (f"consciousness={consciousness_score:.2f}, "
                    f"interactions={interaction_count}, "
                    f"sessions={session_count}, "
                    f"days_active={last_transition_days}")
        
        # Auto-approve if confidence exceeds threshold
        auto_approved = confidence >= min_confidence
        
        logger.info(f"Phase transition recommended: {current_phase} -> {requirements['next_phase']} "
                   f"(confidence={confidence:.2f}, auto_approved={auto_approved})")
        
        return True, requirements['next_phase'], confidence, condition
        
    except Exception as e:
        logger.error(f"Error evaluating phase transition: {str(e)}")
        return False, None, 0.0, f"error: {str(e)}"


def evaluate_interaction_complexity(
    recent_events: List[Dict[str, Any]],
    window_size: int = 100
) -> float:
    """
    Evaluate the complexity of recent interactions
    
    Analyzes event types, patterns, and diversity to determine
    interaction sophistication.
    
    Args:
        recent_events: List of recent event dictionaries
        window_size: Number of recent events to analyze
        
    Returns:
        float: Complexity score (0 to 1)
    """
    try:
        if not recent_events:
            return 0.0
        
        # Limit to window size
        events_to_analyze = recent_events[:window_size]
        
        # Calculate diversity metrics
        event_types = set(e.get('event_type', '') for e in events_to_analyze)
        event_subtypes = set(e.get('event_subtype', '') for e in events_to_analyze if e.get('event_subtype'))
        
        # Type diversity score
        type_diversity = min(1.0, len(event_types) / 10)
        subtype_diversity = min(1.0, len(event_subtypes) / 20)
        
        # Pattern diversity (not just repeating same action)
        # Look for variety in consecutive events
        pattern_changes = 0
        for i in range(1, len(events_to_analyze)):
            if events_to_analyze[i].get('event_type') != events_to_analyze[i-1].get('event_type'):
                pattern_changes += 1
        
        pattern_diversity = min(1.0, pattern_changes / max(1, len(events_to_analyze) - 1))
        
        # Combined complexity score
        complexity = (
            type_diversity * 0.4 +
            subtype_diversity * 0.3 +
            pattern_diversity * 0.3
        )
        
        logger.debug(f"Interaction complexity: {complexity:.3f} "
                    f"(types={len(event_types)}, subtypes={len(event_subtypes)}, "
                    f"pattern_changes={pattern_changes})")
        
        return round(complexity, 3)
        
    except Exception as e:
        logger.error(f"Error evaluating interaction complexity: {str(e)}")
        return 0.0


def check_memory_health(
    state_data: Dict[str, Any],
    event_count: int,
    session_count: int,
    last_sync_age_hours: int
) -> Dict[str, Any]:
    """
    Health check for iNFT memory state
    
    Evaluates memory integrity, sync status, and overall health.
    
    Args:
        state_data: Current state data
        event_count: Number of logged events
        session_count: Number of sessions
        last_sync_age_hours: Hours since last 0G sync
        
    Returns:
        Dict containing health status and recommendations
    """
    try:
        issues = []
        warnings = []
        recommendations = []
        
        # Check sync freshness
        if last_sync_age_hours > 24:
            warnings.append(f"Last sync was {last_sync_age_hours} hours ago")
            recommendations.append("Schedule immediate 0G Storage sync")
        
        # Check memory checksum presence
        if not state_data.get('memory_checksum'):
            issues.append("Missing memory checksum")
            recommendations.append("Recalculate and store memory checksum")
        
        # Check event/session ratio
        if session_count > 0:
            events_per_session = event_count / session_count
            if events_per_session < 2:
                warnings.append("Low interaction density (events per session)")
            elif events_per_session > 1000:
                warnings.append("Very high interaction density - consider session segmentation")
        
        # Check for stale sessions (no recent activity)
        current_timestamp = int(datetime.now().timestamp())
        last_update = state_data.get('updated_at', 0)
        days_inactive = (current_timestamp - last_update) / 86400
        
        if days_inactive > 30:
            warnings.append(f"No activity for {days_inactive:.0f} days")
            recommendations.append("Consider marking iNFT as dormant")
        
        # Determine overall health
        if issues:
            health_status = "unhealthy"
        elif warnings:
            health_status = "degraded"
        else:
            health_status = "healthy"
        
        return {
            "health_status": health_status,
            "issues": issues,
            "warnings": warnings,
            "recommendations": recommendations,
            "last_sync_age_hours": last_sync_age_hours,
            "days_inactive": round(days_inactive, 1),
            "events_per_session": round(event_count / max(1, session_count), 2)
        }
        
    except Exception as e:
        logger.error(f"Error checking memory health: {str(e)}")
        return {
            "health_status": "error",
            "issues": [f"Health check failed: {str(e)}"],
            "warnings": [],
            "recommendations": ["Investigate health check error"]
        }


__all__ = [
    "calculate_consciousness_score",
    "should_transition_phase",
    "evaluate_interaction_complexity",
    "check_memory_health"
]
