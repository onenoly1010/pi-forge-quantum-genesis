-- =============================================================================
-- HEPHAESTUS GUARDIAN COORDINATOR - DATABASE SCHEMA
-- =============================================================================
-- PostgreSQL/Supabase compatible schema for guardian governance system
-- Apply this schema using: psql -U user -d dbname -f schema.sql
-- Or paste into Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- GUARDIANS TABLE
-- =============================================================================
-- Stores guardian identity, credentials, and status

CREATE TABLE IF NOT EXISTS guardians (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    guardian_id VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    public_key TEXT,
    discord_user_id VARCHAR(255) UNIQUE,
    wallet_address VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    role VARCHAR(50) DEFAULT 'guardian' CHECK (role IN ('guardian', 'admin', 'observer')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for guardians
CREATE INDEX IF NOT EXISTS idx_guardians_guardian_id ON guardians(guardian_id);
CREATE INDEX IF NOT EXISTS idx_guardians_discord_user_id ON guardians(discord_user_id);
CREATE INDEX IF NOT EXISTS idx_guardians_status ON guardians(status);
CREATE INDEX IF NOT EXISTS idx_guardians_wallet_address ON guardians(wallet_address);

-- =============================================================================
-- GUARDIAN_PROPOSALS TABLE
-- =============================================================================
-- Tracks governance proposals, votes, and execution status

CREATE TABLE IF NOT EXISTS guardian_proposals (
    id SERIAL PRIMARY KEY,
    proposal_id VARCHAR(255) UNIQUE NOT NULL,
    action VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    params JSONB DEFAULT '{}'::jsonb,
    proposer VARCHAR(255) NOT NULL,
    proposer_id UUID REFERENCES guardians(id),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'executed', 'expired')),
    votes JSONB DEFAULT '[]'::jsonb,
    votes_approve INTEGER DEFAULT 0,
    votes_reject INTEGER DEFAULT 0,
    quorum_required INTEGER DEFAULT 3,
    quorum_met BOOLEAN DEFAULT FALSE,
    executed BOOLEAN DEFAULT FALSE,
    executed_at TIMESTAMP WITH TIME ZONE,
    executed_by VARCHAR(255),
    execution_result JSONB,
    discord_thread_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '7 days'),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for guardian_proposals
CREATE INDEX IF NOT EXISTS idx_proposals_proposal_id ON guardian_proposals(proposal_id);
CREATE INDEX IF NOT EXISTS idx_proposals_status ON guardian_proposals(status);
CREATE INDEX IF NOT EXISTS idx_proposals_proposer ON guardian_proposals(proposer);
CREATE INDEX IF NOT EXISTS idx_proposals_action ON guardian_proposals(action);
CREATE INDEX IF NOT EXISTS idx_proposals_executed ON guardian_proposals(executed);
CREATE INDEX IF NOT EXISTS idx_proposals_created_at ON guardian_proposals(created_at DESC);

-- =============================================================================
-- GUARDIAN_VOTES TABLE (optional - for detailed vote tracking)
-- =============================================================================
-- Individual vote records (alternative to storing votes as JSONB array)

CREATE TABLE IF NOT EXISTS guardian_votes (
    id SERIAL PRIMARY KEY,
    proposal_id INTEGER REFERENCES guardian_proposals(id) ON DELETE CASCADE,
    guardian_id UUID REFERENCES guardians(id) ON DELETE CASCADE,
    vote VARCHAR(20) NOT NULL CHECK (vote IN ('approve', 'reject', 'abstain')),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(proposal_id, guardian_id)
);

-- Indexes for guardian_votes
CREATE INDEX IF NOT EXISTS idx_votes_proposal_id ON guardian_votes(proposal_id);
CREATE INDEX IF NOT EXISTS idx_votes_guardian_id ON guardian_votes(guardian_id);

-- =============================================================================
-- AUDIT_LOG TABLE (optional - for security and compliance)
-- =============================================================================
-- Track all critical actions for security auditing

CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    actor VARCHAR(255) NOT NULL,
    actor_id UUID REFERENCES guardians(id),
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    action VARCHAR(100) NOT NULL,
    details JSONB DEFAULT '{}'::jsonb,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for audit_log
CREATE INDEX IF NOT EXISTS idx_audit_event_type ON audit_log(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_log(actor);
CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_log(created_at DESC);

-- =============================================================================
-- FUNCTIONS AND TRIGGERS
-- =============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_guardians_updated_at BEFORE UPDATE ON guardians
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_proposals_updated_at BEFORE UPDATE ON guardian_proposals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to update vote counts
CREATE OR REPLACE FUNCTION update_proposal_vote_counts()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE guardian_proposals
    SET 
        votes_approve = (
            SELECT COUNT(*) FROM guardian_votes 
            WHERE proposal_id = NEW.proposal_id AND vote = 'approve'
        ),
        votes_reject = (
            SELECT COUNT(*) FROM guardian_votes 
            WHERE proposal_id = NEW.proposal_id AND vote = 'reject'
        ),
        quorum_met = (
            SELECT COUNT(*) FROM guardian_votes 
            WHERE proposal_id = NEW.proposal_id AND vote = 'approve'
        ) >= quorum_required
    WHERE id = NEW.proposal_id;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to update vote counts when vote is inserted/updated
CREATE TRIGGER update_vote_counts AFTER INSERT OR UPDATE ON guardian_votes
    FOR EACH ROW EXECUTE FUNCTION update_proposal_vote_counts();

-- =============================================================================
-- SEED DATA (optional - for development/testing)
-- =============================================================================

-- Insert sample guardians (ONLY FOR DEVELOPMENT)
-- Comment out or remove for production

-- INSERT INTO guardians (guardian_id, display_name, status, role) VALUES
-- ('guardian_alpha', 'Guardian Alpha', 'active', 'admin'),
-- ('guardian_beta', 'Guardian Beta', 'active', 'guardian'),
-- ('guardian_gamma', 'Guardian Gamma', 'active', 'guardian'),
-- ('guardian_delta', 'Guardian Delta', 'active', 'guardian'),
-- ('guardian_epsilon', 'Guardian Epsilon', 'active', 'guardian');

-- =============================================================================
-- COMMENTS
-- =============================================================================

COMMENT ON TABLE guardians IS 'Guardian identities and credentials';
COMMENT ON TABLE guardian_proposals IS 'Governance proposals requiring multisig approval';
COMMENT ON TABLE guardian_votes IS 'Individual guardian votes on proposals';
COMMENT ON TABLE audit_log IS 'Security and compliance audit trail';

COMMENT ON COLUMN guardians.guardian_id IS 'Unique guardian identifier';
COMMENT ON COLUMN guardians.public_key IS 'Guardian public key for cryptographic verification';
COMMENT ON COLUMN guardians.discord_user_id IS 'Discord user ID for bot integration';
COMMENT ON COLUMN guardians.metadata IS 'Additional guardian metadata as JSON';

COMMENT ON COLUMN guardian_proposals.proposal_id IS 'Unique proposal identifier';
COMMENT ON COLUMN guardian_proposals.action IS 'Type of action to execute (deploy_contract, transfer_funds, etc)';
COMMENT ON COLUMN guardian_proposals.params IS 'Action-specific parameters as JSON';
COMMENT ON COLUMN guardian_proposals.votes IS 'Vote records as JSON array (if not using guardian_votes table)';
COMMENT ON COLUMN guardian_proposals.quorum_met IS 'Whether required quorum has been reached';
COMMENT ON COLUMN guardian_proposals.executed IS 'Whether proposal has been executed';

-- =============================================================================
-- GRANTS (configure based on your security requirements)
-- =============================================================================

-- Example: Grant appropriate permissions to application user
-- GRANT SELECT, INSERT, UPDATE ON guardians TO guardian_app_user;
-- GRANT SELECT, INSERT, UPDATE ON guardian_proposals TO guardian_app_user;
-- GRANT SELECT, INSERT, UPDATE ON guardian_votes TO guardian_app_user;
-- GRANT INSERT ON audit_log TO guardian_app_user;

-- =============================================================================
-- SCHEMA VERSION
-- =============================================================================

CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    description TEXT
);

INSERT INTO schema_version (version, description) VALUES 
(1, 'Initial guardian coordinator schema');

-- End of schema
