-- LEDGER SCHEMA v1.0
-- Pi Forge Quantum Genesis - Ledger API
-- Multi-Account Treasury System with Atomic Allocations

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- LOGICAL ACCOUNTS TABLE
-- Represents internal wallet subdivisions
-- ============================================
CREATE TABLE logical_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_name VARCHAR(100) NOT NULL UNIQUE,
    account_type VARCHAR(50) NOT NULL CHECK (account_type IN ('OPERATING', 'RESERVE', 'REWARDS', 'DEVELOPMENT', 'MARKETING', 'CUSTOM')),
    current_balance NUMERIC(20, 8) NOT NULL DEFAULT 0 CHECK (current_balance >= 0),
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_logical_accounts_name ON logical_accounts(account_name);
CREATE INDEX idx_logical_accounts_type ON logical_accounts(account_type);

-- ============================================
-- LEDGER TRANSACTIONS TABLE
-- Records all financial movements
-- ============================================
CREATE TABLE ledger_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_type VARCHAR(50) NOT NULL CHECK (transaction_type IN (
        'EXTERNAL_DEPOSIT',
        'EXTERNAL_WITHDRAWAL', 
        'INTERNAL_ALLOCATION',
        'PAYMENT',
        'REFUND',
        'FEE',
        'NFT_MINT',
        'REWARD'
    )),
    status VARCHAR(30) NOT NULL CHECK (status IN (
        'PENDING',
        'COMPLETED',
        'FAILED',
        'CANCELLED',
        'REFUNDED'
    )),
    amount NUMERIC(20, 8) NOT NULL CHECK (amount >= 0),
    
    -- Account relationships
    from_account_id UUID REFERENCES logical_accounts(id),
    to_account_id UUID REFERENCES logical_accounts(id),
    
    -- Parent/child hierarchy for allocations
    parent_transaction_id UUID REFERENCES ledger_transactions(id),
    
    -- External identifiers
    external_tx_hash VARCHAR(255),
    pi_payment_id VARCHAR(255),
    
    -- Metadata
    description TEXT,
    metadata JSONB,
    
    -- User context
    performed_by VARCHAR(255),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT valid_account_flow CHECK (
        (transaction_type = 'EXTERNAL_DEPOSIT' AND from_account_id IS NULL AND to_account_id IS NOT NULL) OR
        (transaction_type = 'EXTERNAL_WITHDRAWAL' AND from_account_id IS NOT NULL AND to_account_id IS NULL) OR
        (transaction_type IN ('INTERNAL_ALLOCATION', 'PAYMENT', 'REFUND', 'FEE', 'NFT_MINT', 'REWARD') 
         AND from_account_id IS NOT NULL AND to_account_id IS NOT NULL)
    )
);

CREATE INDEX idx_ledger_tx_type ON ledger_transactions(transaction_type);
CREATE INDEX idx_ledger_tx_status ON ledger_transactions(status);
CREATE INDEX idx_ledger_tx_parent ON ledger_transactions(parent_transaction_id);
CREATE INDEX idx_ledger_tx_from_account ON ledger_transactions(from_account_id);
CREATE INDEX idx_ledger_tx_to_account ON ledger_transactions(to_account_id);
CREATE INDEX idx_ledger_tx_external_hash ON ledger_transactions(external_tx_hash);
CREATE INDEX idx_ledger_tx_pi_payment ON ledger_transactions(pi_payment_id);
CREATE INDEX idx_ledger_tx_created ON ledger_transactions(created_at);

-- ============================================
-- ALLOCATION RULES TABLE
-- Defines how EXTERNAL_DEPOSIT funds are split
-- ============================================
CREATE TABLE allocation_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_name VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    priority INTEGER NOT NULL DEFAULT 100,
    
    -- Allocation configuration (array of {account_name, percentage})
    allocation_config JSONB NOT NULL,
    
    -- Conditions for rule application
    min_amount NUMERIC(20, 8),
    max_amount NUMERIC(20, 8),
    
    -- Metadata
    description TEXT,
    created_by VARCHAR(255),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Validation: percentages must sum to 100
    CONSTRAINT valid_allocation_config CHECK (
        jsonb_typeof(allocation_config) = 'array' AND
        jsonb_array_length(allocation_config) > 0
    )
);

CREATE INDEX idx_allocation_rules_active ON allocation_rules(is_active, priority);

-- ============================================
-- AUDIT LOG TABLE
-- Immutable record of all administrative changes
-- ============================================
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(50) NOT NULL CHECK (entity_type IN (
        'ledger_transaction',
        'allocation_rule',
        'logical_account',
        'reconciliation'
    )),
    entity_id UUID NOT NULL,
    action VARCHAR(30) NOT NULL CHECK (action IN (
        'CREATE',
        'UPDATE',
        'DELETE',
        'EXECUTE'
    )),
    
    -- Change tracking
    old_value JSONB,
    new_value JSONB,
    
    -- Actor
    performed_by VARCHAR(255) NOT NULL,
    
    -- Context
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_log_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_log_performed_by ON audit_log(performed_by);
CREATE INDEX idx_audit_log_created ON audit_log(created_at);

-- ============================================
-- RECONCILIATION LOG TABLE
-- Tracks external wallet vs internal balance comparisons
-- ============================================
CREATE TABLE reconciliation_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- External state
    external_wallet_balance NUMERIC(20, 8) NOT NULL,
    external_source VARCHAR(100),
    
    -- Internal state
    internal_total_balance NUMERIC(20, 8) NOT NULL,
    
    -- Comparison
    discrepancy NUMERIC(20, 8) NOT NULL,
    discrepancy_percentage NUMERIC(10, 4),
    
    -- Status
    status VARCHAR(30) NOT NULL CHECK (status IN (
        'BALANCED',
        'MINOR_DISCREPANCY',
        'MAJOR_DISCREPANCY',
        'CRITICAL'
    )),
    
    -- Resolution
    resolution_notes TEXT,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by VARCHAR(255),
    
    -- Context
    performed_by VARCHAR(255) NOT NULL,
    
    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_reconciliation_status ON reconciliation_log(status);
CREATE INDEX idx_reconciliation_created ON reconciliation_log(created_at);

-- ============================================
-- SEED DATA - Default Logical Accounts
-- ============================================
INSERT INTO logical_accounts (account_name, account_type, description) VALUES
    ('main_operating', 'OPERATING', 'Primary operating account for day-to-day transactions'),
    ('reserve_fund', 'RESERVE', 'Emergency reserve and long-term stability'),
    ('rewards_pool', 'REWARDS', 'User rewards and incentive distribution'),
    ('development_fund', 'DEVELOPMENT', 'Platform development and maintenance'),
    ('marketing_fund', 'MARKETING', 'Marketing and community growth initiatives');

-- ============================================
-- SEED DATA - Default Allocation Rule
-- ============================================
INSERT INTO allocation_rules (rule_name, allocation_config, description, created_by) VALUES
    (
        'default_deposit_allocation',
        '[
            {"account_name": "main_operating", "percentage": 50},
            {"account_name": "reserve_fund", "percentage": 20},
            {"account_name": "rewards_pool", "percentage": 15},
            {"account_name": "development_fund", "percentage": 10},
            {"account_name": "marketing_fund", "percentage": 5}
        ]'::jsonb,
        'Default allocation rule for external deposits',
        'system'
    );

-- ============================================
-- TRIGGERS - Auto-update timestamps
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_logical_accounts_updated_at
    BEFORE UPDATE ON logical_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_allocation_rules_updated_at
    BEFORE UPDATE ON allocation_rules
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- VIEWS - Useful aggregations
-- ============================================

-- Current treasury status view
CREATE VIEW treasury_status AS
SELECT 
    account_name,
    account_type,
    current_balance,
    is_active,
    updated_at
FROM logical_accounts
WHERE is_active = TRUE
ORDER BY account_type, account_name;

-- Transaction summary by account
CREATE VIEW account_transaction_summary AS
SELECT 
    la.account_name,
    COUNT(CASE WHEN lt.to_account_id = la.id THEN 1 END) as inbound_count,
    COUNT(CASE WHEN lt.from_account_id = la.id THEN 1 END) as outbound_count,
    SUM(CASE WHEN lt.to_account_id = la.id AND lt.status = 'COMPLETED' THEN lt.amount ELSE 0 END) as total_inbound,
    SUM(CASE WHEN lt.from_account_id = la.id AND lt.status = 'COMPLETED' THEN lt.amount ELSE 0 END) as total_outbound
FROM logical_accounts la
LEFT JOIN ledger_transactions lt ON la.id = lt.to_account_id OR la.id = lt.from_account_id
GROUP BY la.id, la.account_name;

-- Comments
COMMENT ON TABLE logical_accounts IS 'Internal wallet subdivisions for treasury management';
COMMENT ON TABLE ledger_transactions IS 'Complete transaction history with parent-child relationships for allocations';
COMMENT ON TABLE allocation_rules IS 'Configurable rules for automatically splitting external deposits';
COMMENT ON TABLE audit_log IS 'Immutable audit trail of all system changes';
COMMENT ON TABLE reconciliation_log IS 'Balance reconciliation history between external and internal systems';
