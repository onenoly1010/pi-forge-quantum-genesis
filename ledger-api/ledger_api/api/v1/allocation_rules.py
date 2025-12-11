"""
Allocation Rules API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
import logging

from ledger_api.db import get_db
from ledger_api.models.ledger_models import AllocationRule
from ledger_api.schemas.allocation_rule import (
    AllocationRuleCreate,
    AllocationRuleResponse,
    AllocationRuleListResponse,
    AllocationItem
)
from ledger_api.services.audit import create_audit_log
from ledger_api.utils.jwt_auth import require_guardian_role, JWTPayload

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/allocation-rules", tags=["allocation-rules"])


@router.get("", response_model=AllocationRuleListResponse)
def list_allocation_rules(
    active_only: bool = True,
    db: Session = Depends(get_db)
) -> AllocationRuleListResponse:
    """
    List all allocation rules.
    Public endpoint - no authentication required for viewing.
    """
    query = db.query(AllocationRule)

    if active_only:
        query = query.filter(AllocationRule.is_active == True)

    rules = query.order_by(AllocationRule.priority, AllocationRule.created_at).all()

    # Parse allocation_config JSON for each rule
    parsed_rules = []
    for rule in rules:
        try:
            config = json.loads(rule.allocation_config)
            # Convert to AllocationItem objects
            allocation_items = [
                AllocationItem(
                    account_name=item['account_name'],
                    percentage=item['percentage']
                )
                for item in config
            ]
            
            # Create response object
            rule_response = AllocationRuleResponse(
                id=rule.id,
                rule_name=rule.rule_name,
                is_active=rule.is_active,
                priority=rule.priority,
                allocation_config=allocation_items,
                min_amount=rule.min_amount,
                max_amount=rule.max_amount,
                description=rule.description,
                created_by=rule.created_by,
                created_at=rule.created_at,
                updated_at=rule.updated_at
            )
            parsed_rules.append(rule_response)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing allocation config for rule {rule.id}: {e}")
            # Skip invalid rules
            continue

    return AllocationRuleListResponse(
        rules=parsed_rules,
        total=len(parsed_rules)
    )


@router.get("/{rule_id}", response_model=AllocationRuleResponse)
def get_allocation_rule(
    rule_id: str,
    db: Session = Depends(get_db)
) -> AllocationRuleResponse:
    """
    Get a specific allocation rule by ID.
    Public endpoint - no authentication required for viewing.
    """
    rule = db.query(AllocationRule).filter(AllocationRule.id == rule_id).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Allocation rule not found")

    # Parse allocation_config
    try:
        config = json.loads(rule.allocation_config)
        allocation_items = [
            AllocationItem(
                account_name=item['account_name'],
                percentage=item['percentage']
            )
            for item in config
        ]
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error parsing allocation config: {e}")
        raise HTTPException(status_code=500, detail="Invalid allocation configuration")

    return AllocationRuleResponse(
        id=rule.id,
        rule_name=rule.rule_name,
        is_active=rule.is_active,
        priority=rule.priority,
        allocation_config=allocation_items,
        min_amount=rule.min_amount,
        max_amount=rule.max_amount,
        description=rule.description,
        created_by=rule.created_by,
        created_at=rule.created_at,
        updated_at=rule.updated_at
    )


@router.post("", response_model=AllocationRuleResponse, status_code=201)
def create_allocation_rule(
    rule: AllocationRuleCreate,
    current_user: JWTPayload = Depends(require_guardian_role),
    db: Session = Depends(get_db)
) -> AllocationRuleResponse:
    """
    Create a new allocation rule.
    
    **Requires Guardian JWT authentication.**
    
    Validates that allocation percentages sum to 100%.
    """
    # Convert allocation_config to JSON string
    config_dict = [
        {
            "account_name": item.account_name,
            "percentage": str(item.percentage)
        }
        for item in rule.allocation_config
    ]
    config_json = json.dumps(config_dict)

    # Create the allocation rule
    db_rule = AllocationRule(
        rule_name=rule.rule_name,
        is_active=rule.is_active,
        priority=rule.priority,
        allocation_config=config_json,
        min_amount=rule.min_amount,
        max_amount=rule.max_amount,
        description=rule.description,
        created_by=current_user.sub  # From JWT token
    )

    try:
        db.add(db_rule)
        db.flush()

        # Create audit log
        create_audit_log(
            db=db,
            entity_type="allocation_rule",
            entity_id=db_rule.id,
            action="CREATE",
            old_value=None,
            new_value={
                "rule_name": rule.rule_name,
                "allocation_config": config_dict,
                "is_active": rule.is_active
            },
            performed_by=current_user.sub
        )

        db.commit()
        db.refresh(db_rule)

        # Return with parsed config
        return AllocationRuleResponse(
            id=db_rule.id,
            rule_name=db_rule.rule_name,
            is_active=db_rule.is_active,
            priority=db_rule.priority,
            allocation_config=rule.allocation_config,  # Already validated
            min_amount=db_rule.min_amount,
            max_amount=db_rule.max_amount,
            description=db_rule.description,
            created_by=db_rule.created_by,
            created_at=db_rule.created_at,
            updated_at=db_rule.updated_at
        )

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating allocation rule: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Allocation rule with this name already exists"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating allocation rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{rule_id}", status_code=204)
def delete_allocation_rule(
    rule_id: str,
    current_user: JWTPayload = Depends(require_guardian_role),
    db: Session = Depends(get_db)
):
    """
    Delete (deactivate) an allocation rule.
    
    **Requires Guardian JWT authentication.**
    
    Note: This actually deactivates the rule rather than deleting it,
    to preserve audit history.
    """
    rule = db.query(AllocationRule).filter(AllocationRule.id == rule_id).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Allocation rule not found")

    try:
        # Store old value for audit
        old_value = {
            "rule_name": rule.rule_name,
            "is_active": rule.is_active
        }

        # Deactivate instead of delete
        rule.is_active = False

        # Create audit log
        create_audit_log(
            db=db,
            entity_type="allocation_rule",
            entity_id=rule_id,
            action="DELETE",
            old_value=old_value,
            new_value={"is_active": False},
            performed_by=current_user.sub
        )

        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting allocation rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))
