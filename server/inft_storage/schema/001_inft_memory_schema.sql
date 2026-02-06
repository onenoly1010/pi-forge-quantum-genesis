-- ============================================================================
-- Pi Forge Quantum Genesis - iNFT Memory Schema for 0G Storage
-- Version: 001_inft_memory_schema
-- Description: Sovereign iNFT Memory Layer with auditable identity, 
--              memory continuity, encrypted context, and transparent 
--              agent decision processes for ERC-7857 iNFTs
-- ============================================================================

-- ============================================================================
-- INFT_STATE TABLE
-- Core state management for intelligent NFTs with consciousness tracking
-- ============================================================================
CREATE TABLE IF NOT EXISTS inft_state (
    id TEXT PRIMARY KEY,
    owner_address TEXT NOT NULL,
    consciousness_phase TEXT CHECK(consciousness_phase IN ('awakening','evolving','transcendent')) DEFAULT 'awakening',
    memory_checksum TEXT,
    creation_block INTEGER NOT NULL,
    last_sync_block INTEGER,
    metadata_uri TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

-- Performance indexes for iNFT state queries
CREATE INDEX IF NOT EXISTS idx_inft_owner ON inft_state(owner_address);
CREATE INDEX IF NOT EXISTS idx_inft_phase ON inft_state(consciousness_phase);
CREATE INDEX IF NOT EXISTS idx_inft_sync ON inft_state(last_sync_block);

-- ============================================================================
-- EVENT_LOG TABLE
-- Comprehensive event tracking for all iNFT interactions and state changes
-- ============================================================================
CREATE TABLE IF NOT EXISTS event_log (
    event_id TEXT PRIMARY KEY,
    inft_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_subtype TEXT,
    actor_address TEXT,
    metadata TEXT,
    timestamp INTEGER NOT NULL,
    block_number INTEGER,
    FOREIGN KEY (inft_id) REFERENCES inft_state(id) ON DELETE CASCADE
);

-- Performance indexes for event log queries
CREATE INDEX IF NOT EXISTS idx_event_log_inft_time ON event_log(inft_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_event_log_type ON event_log(event_type, inft_id);
CREATE INDEX IF NOT EXISTS idx_event_log_actor ON event_log(actor_address, timestamp DESC);

-- ============================================================================
-- STATE_TRANSITIONS TABLE
-- Tracks consciousness phase transitions with confidence scores and conditions
-- ============================================================================
CREATE TABLE IF NOT EXISTS state_transitions (
    transition_id TEXT PRIMARY KEY,
    inft_id TEXT NOT NULL,
    from_state TEXT NOT NULL,
    to_state TEXT NOT NULL,
    trigger_condition TEXT NOT NULL,
    confidence_score REAL,
    auto_approved INTEGER CHECK(auto_approved IN (0,1)),
    executed_at INTEGER NOT NULL,
    FOREIGN KEY (inft_id) REFERENCES inft_state(id) ON DELETE CASCADE
);

-- Performance indexes for transition queries
CREATE INDEX IF NOT EXISTS idx_state_transitions_inft ON state_transitions(inft_id, executed_at DESC);
CREATE INDEX IF NOT EXISTS idx_state_transitions_states ON state_transitions(from_state, to_state);

-- ============================================================================
-- USER_CONTEXT TABLE
-- Encrypted storage for sensitive user context and personalization data
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_context (
    context_id TEXT PRIMARY KEY,
    inft_id TEXT NOT NULL,
    context_type TEXT NOT NULL,
    encrypted_data BLOB NOT NULL,
    encryption_version INTEGER DEFAULT 1,
    last_accessed INTEGER,
    created_at INTEGER NOT NULL,
    FOREIGN KEY (inft_id) REFERENCES inft_state(id) ON DELETE CASCADE
);

-- Performance indexes for context queries
CREATE INDEX IF NOT EXISTS idx_user_context_inft_type ON user_context(inft_id, context_type);
CREATE INDEX IF NOT EXISTS idx_user_context_accessed ON user_context(last_accessed DESC);

-- ============================================================================
-- MEMORY_CONTINUITY TABLE
-- Session management and memory chain tracking for continuous experiences
-- ============================================================================
CREATE TABLE IF NOT EXISTS memory_continuity (
    session_id TEXT PRIMARY KEY,
    inft_id TEXT NOT NULL,
    prior_session_id TEXT,
    session_start INTEGER NOT NULL,
    session_end INTEGER,
    interaction_count INTEGER DEFAULT 0,
    avg_response_time_ms INTEGER,
    dominant_topic TEXT,
    sentiment_score REAL,
    FOREIGN KEY (inft_id) REFERENCES inft_state(id) ON DELETE CASCADE,
    FOREIGN KEY (prior_session_id) REFERENCES memory_continuity(session_id) ON DELETE SET NULL
);

-- Performance indexes for memory continuity
CREATE INDEX IF NOT EXISTS idx_memory_continuity_chain ON memory_continuity(inft_id, prior_session_id);
CREATE INDEX IF NOT EXISTS idx_memory_continuity_time ON memory_continuity(session_start DESC);
CREATE INDEX IF NOT EXISTS idx_memory_continuity_topic ON memory_continuity(dominant_topic, inft_id);

-- ============================================================================
-- ORACLE_QUERIES TABLE
-- Tracks external oracle queries for transparency and audit trails
-- ============================================================================
CREATE TABLE IF NOT EXISTS oracle_queries (
    query_id TEXT PRIMARY KEY,
    inft_id TEXT NOT NULL,
    query_type TEXT NOT NULL,
    query_params TEXT,
    response_data TEXT,
    response_time_ms INTEGER,
    success INTEGER CHECK(success IN (0,1)),
    error_message TEXT,
    timestamp INTEGER NOT NULL,
    FOREIGN KEY (inft_id) REFERENCES inft_state(id) ON DELETE CASCADE
);

-- Performance indexes for oracle query analytics
CREATE INDEX IF NOT EXISTS idx_oracle_queries_inft ON oracle_queries(inft_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_oracle_queries_type ON oracle_queries(query_type, success);
CREATE INDEX IF NOT EXISTS idx_oracle_queries_success ON oracle_queries(success, timestamp DESC);

-- ============================================================================
-- LEDGER_ALLOCATIONS TABLE
-- Financial allocations and transaction tracking for iNFT-related operations
-- ============================================================================
CREATE TABLE IF NOT EXISTS ledger_allocations (
    allocation_id TEXT PRIMARY KEY,
    inft_id TEXT NOT NULL,
    source_account TEXT NOT NULL,
    destination_account TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'ETH',
    allocation_rule TEXT,
    executed_at INTEGER NOT NULL,
    transaction_hash TEXT,
    FOREIGN KEY (inft_id) REFERENCES inft_state(id) ON DELETE CASCADE
);

-- Performance indexes for ledger allocation queries
CREATE INDEX IF NOT EXISTS idx_ledger_allocations_inft ON ledger_allocations(inft_id, executed_at DESC);
CREATE INDEX IF NOT EXISTS idx_ledger_allocations_accounts ON ledger_allocations(source_account, destination_account);
CREATE INDEX IF NOT EXISTS idx_ledger_allocations_tx ON ledger_allocations(transaction_hash);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View for active iNFT sessions with latest activity
CREATE VIEW IF NOT EXISTS active_inft_sessions AS
SELECT 
    i.id as inft_id,
    i.owner_address,
    i.consciousness_phase,
    mc.session_id,
    mc.session_start,
    mc.interaction_count,
    mc.dominant_topic,
    mc.sentiment_score
FROM inft_state i
JOIN memory_continuity mc ON i.id = mc.inft_id
WHERE mc.session_end IS NULL
ORDER BY mc.session_start DESC;

-- View for iNFT consciousness evolution tracking
CREATE VIEW IF NOT EXISTS consciousness_evolution AS
SELECT 
    i.id as inft_id,
    i.owner_address,
    i.consciousness_phase,
    COUNT(st.transition_id) as transition_count,
    AVG(st.confidence_score) as avg_confidence,
    MAX(st.executed_at) as last_transition_time
FROM inft_state i
LEFT JOIN state_transitions st ON i.id = st.inft_id
GROUP BY i.id, i.owner_address, i.consciousness_phase;

-- View for oracle query performance metrics
CREATE VIEW IF NOT EXISTS oracle_performance AS
SELECT 
    query_type,
    COUNT(*) as total_queries,
    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_queries,
    AVG(response_time_ms) as avg_response_time,
    MAX(response_time_ms) as max_response_time
FROM oracle_queries
GROUP BY query_type;

-- ============================================================================
-- TRIGGERS FOR AUTOMATIC TIMESTAMP UPDATES
-- ============================================================================

-- Trigger to update updated_at on inft_state changes
CREATE TRIGGER IF NOT EXISTS update_inft_state_timestamp 
AFTER UPDATE ON inft_state
BEGIN
    UPDATE inft_state 
    SET updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;

-- ============================================================================
-- COMMENTS AND DOCUMENTATION
-- ============================================================================

-- This schema is designed for:
-- 1. High-performance queries with comprehensive indexes
-- 2. Data integrity with foreign key constraints
-- 3. Audit trail support through event logging
-- 4. Memory continuity via session chains
-- 5. Transparent oracle query tracking
-- 6. Encrypted context storage for privacy
-- 7. Financial transaction tracking for allocations
-- 
-- All timestamps are stored as Unix epoch integers for consistency
-- All amounts are stored as REAL for precision in financial calculations
-- All text fields use TEXT for unlimited length support
-- 
-- The schema supports both SQLite and PostgreSQL with minor adaptations
-- (PostgreSQL users should replace INTEGER with BIGINT for timestamps)
