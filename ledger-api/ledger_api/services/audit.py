"""
Audit logging service for tracking all administrative changes
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import json
import logging

from ledger_api.models.ledger_models import AuditLog

logger = logging.getLogger(__name__)


def create_audit_log(
    db: Session,
    entity_type: str,
    entity_id: str,
    action: str,
    old_value: Optional[Dict[str, Any]],
    new_value: Optional[Dict[str, Any]],
    performed_by: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> AuditLog:
    """
    Create an audit log entry for tracking changes.
    
    Args:
        db: Database session
        entity_type: Type of entity ('ledger_transaction', 'allocation_rule', etc.)
        entity_id: ID of the entity
        action: Action performed ('CREATE', 'UPDATE', 'DELETE', 'EXECUTE')
        old_value: Previous state (None for CREATE)
        new_value: New state (None for DELETE)
        performed_by: User who performed the action
        ip_address: IP address of the user
        user_agent: User agent string
        
    Returns:
        Created AuditLog instance
    """
    # Validate entity type
    valid_entity_types = ['ledger_transaction', 'allocation_rule', 'logical_account', 'reconciliation']
    if entity_type not in valid_entity_types:
        raise ValueError(f"entity_type must be one of {valid_entity_types}")

    # Validate action
    valid_actions = ['CREATE', 'UPDATE', 'DELETE', 'EXECUTE']
    if action not in valid_actions:
        raise ValueError(f"action must be one of {valid_actions}")

    # Convert values to JSON strings for storage
    old_value_json = json.dumps(old_value) if old_value is not None else None
    new_value_json = json.dumps(new_value) if new_value is not None else None

    # Create audit log entry
    audit_entry = AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        old_value=old_value_json,
        new_value=new_value_json,
        performed_by=performed_by,
        ip_address=ip_address,
        user_agent=user_agent
    )

    db.add(audit_entry)
    db.flush()

    logger.info(f"Created audit log: {action} on {entity_type} {entity_id} by {performed_by}")

    return audit_entry


def get_audit_trail(
    db: Session,
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    performed_by: Optional[str] = None,
    limit: int = 100
) -> list:
    """
    Retrieve audit trail with optional filters.
    
    Args:
        db: Database session
        entity_type: Filter by entity type
        entity_id: Filter by entity ID
        performed_by: Filter by user
        limit: Maximum number of records to return
        
    Returns:
        List of AuditLog entries
    """
    query = db.query(AuditLog)

    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    
    if entity_id:
        query = query.filter(AuditLog.entity_id == entity_id)
    
    if performed_by:
        query = query.filter(AuditLog.performed_by == performed_by)

    # Order by newest first
    query = query.order_by(AuditLog.created_at.desc())

    # Apply limit
    query = query.limit(limit)

    return query.all()
