# Ledger API v1.0

Multi-Account Treasury System with Atomic Allocations for Pi Forge Quantum Genesis

## Overview

The Ledger API is a standalone FastAPI service that implements a sophisticated multi-account treasury system with:

- **Atomic Allocations**: Automatically split external deposits according to configurable rules
- **Idempotent Operations**: Safe to retry without creating duplicates
- **Audit Trail**: Complete immutable record of all changes
- **Reconciliation**: Compare external wallet balances with internal accounts
- **Guardian Security**: JWT-based authentication for administrative operations

## Architecture

```
ledger-api/
├── sql/schema/           # SQL schema definitions
├── migrations/           # Alembic database migrations
├── ledger_api/
│   ├── main.py          # FastAPI application entry point
│   ├── db.py            # Database connection and session management
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic request/response models
│   ├── services/        # Business logic (allocation, audit, reconciliation)
│   ├── api/v1/          # API endpoint handlers
│   ├── utils/           # JWT auth, Pi Network stubs
│   └── tests/           # Pytest unit and integration tests
├── Dockerfile
├── docker-compose.yml   # Development environment
├── docker-compose.test.yml  # CI test environment
└── requirements.txt
```

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone repository and navigate to ledger-api
cd ledger-api

# Copy environment template
cp .env.example .env

# Edit .env and set GUARDIAN_JWT_SECRET (at least 32 characters)
nano .env

# Start services (PostgreSQL + Ledger API)
docker-compose up -d

# View logs
docker-compose logs -f ledger-api

# API will be available at http://localhost:8001
```

### Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://ledger_user:ledger_password@localhost:5432/ledger_db"
export GUARDIAN_JWT_SECRET="your-secure-secret-at-least-32-characters-long"
export NFT_MINT_VALUE=0
export APP_ENVIRONMENT=testnet

# Run database migrations
# Option 1: Use Alembic (production)
alembic upgrade head

# Option 2: Auto-create tables (development only)
export AUTO_CREATE_TABLES=true

# Start the API
uvicorn ledger_api.main:app --reload --port 8001
```

## Database Setup

### Using Docker Compose

The `docker-compose.yml` automatically initializes PostgreSQL with the schema from `sql/schema/001_initial_ledger.sql`.

### Manual PostgreSQL Setup

```bash
# Create database
createdb ledger_db

# Create user
psql -c "CREATE USER ledger_user WITH PASSWORD 'ledger_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE ledger_db TO ledger_user;"

# Apply schema
psql -U ledger_user -d ledger_db -f sql/schema/001_initial_ledger.sql
```

## API Endpoints

### Transactions

**POST /api/v1/transactions** - Create a transaction
- When creating a COMPLETED EXTERNAL_DEPOSIT, allocations are automatically applied
- Request body:
  ```json
  {
    "transaction_type": "EXTERNAL_DEPOSIT",
    "status": "COMPLETED",
    "amount": "100.00000000",
    "to_account_id": "account-uuid",
    "external_tx_hash": "0xabc123",
    "description": "External deposit",
    "performed_by": "user@example.com"
  }
  ```

**GET /api/v1/transactions** - List transactions
- Query params: `transaction_type`, `status`, `from_account_id`, `to_account_id`, `page`, `page_size`

**GET /api/v1/transactions/{id}** - Get specific transaction

**GET /api/v1/transactions/{id}/allocations** - Get allocation results for a transaction

### Treasury

**GET /api/v1/treasury/status** - Get current treasury status
- Returns all account balances and total

**POST /api/v1/treasury/reconcile** - Perform reconciliation
- Request body:
  ```json
  {
    "external_wallet_balance": "1000.50000000",
    "external_source": "Pi Network Wallet",
    "performed_by": "admin@example.com"
  }
  ```

### Allocation Rules

**GET /api/v1/allocation-rules** - List allocation rules (public)
- Query params: `active_only` (default: true)

**GET /api/v1/allocation-rules/{id}** - Get specific rule (public)

**POST /api/v1/allocation-rules** - Create allocation rule (requires Guardian JWT)
- Request body:
  ```json
  {
    "rule_name": "custom_allocation",
    "is_active": true,
    "priority": 100,
    "allocation_config": [
      {"account_name": "main_operating", "percentage": 50},
      {"account_name": "reserve_fund", "percentage": 30},
      {"account_name": "rewards_pool", "percentage": 20}
    ],
    "description": "Custom allocation rule"
  }
  ```
- **Important**: Percentages must sum to exactly 100%
- Requires: `Authorization: Bearer <guardian-jwt-token>`

**DELETE /api/v1/allocation-rules/{id}** - Deactivate rule (requires Guardian JWT)

## Authentication

### Guardian JWT

Protected endpoints require a JWT token with `role: "guardian"`.

**Generate a Guardian Token (Development/Testing)**

```python
from ledger_api.utils.jwt_auth import create_jwt_token

token = create_jwt_token(
    sub="guardian@example.com",
    role="guardian"
)
print(token)
```

**Using the Token**

```bash
curl -X POST http://localhost:8001/api/v1/allocation-rules \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## Example Workflows

### Complete Deposit and Allocation Flow

```bash
# 1. Check treasury status before deposit
curl http://localhost:8001/api/v1/treasury/status

# 2. Create a COMPLETED EXTERNAL_DEPOSIT (triggers automatic allocation)
curl -X POST http://localhost:8001/api/v1/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "EXTERNAL_DEPOSIT",
    "status": "COMPLETED",
    "amount": "100.00000000",
    "to_account_id": "YOUR_ACCOUNT_ID",
    "external_tx_hash": "0xabc123",
    "description": "Deposit from Pi wallet",
    "performed_by": "user@pi.network"
  }'

# 3. Check allocation results (save transaction ID from step 2)
curl http://localhost:8001/api/v1/transactions/{TRANSACTION_ID}/allocations

# 4. Verify treasury status after allocation
curl http://localhost:8001/api/v1/treasury/status

# 5. Perform reconciliation
curl -X POST http://localhost:8001/api/v1/treasury/reconcile \
  -H "Content-Type: application/json" \
  -d '{
    "external_wallet_balance": "100.00000000",
    "external_source": "Pi Network Wallet",
    "performed_by": "admin@example.com"
  }'
```

### Create Custom Allocation Rule

```bash
# Generate guardian token first (see Authentication section)
TOKEN="your-guardian-jwt-token"

# Create allocation rule
curl -X POST http://localhost:8001/api/v1/allocation-rules \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rule_name": "large_deposit_allocation",
    "is_active": true,
    "priority": 50,
    "allocation_config": [
      {"account_name": "main_operating", "percentage": 40},
      {"account_name": "reserve_fund", "percentage": 35},
      {"account_name": "rewards_pool", "percentage": 15},
      {"account_name": "development_fund", "percentage": 10}
    ],
    "min_amount": "1000.00000000",
    "description": "Special allocation for deposits > 1000 Pi"
  }'
```

## Testing

### Run Unit Tests

```bash
# Using pytest directly
pytest ledger_api/tests/ -v

# With coverage
pytest ledger_api/tests/ -v --cov=ledger_api --cov-report=html

# Run specific test file
pytest ledger_api/tests/test_allocation.py -v
```

### Run Integration Tests with Docker

```bash
# Run tests in PostgreSQL environment
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# Cleanup
docker-compose -f docker-compose.test.yml down -v
```

## Atomic Allocation Engine

The allocation engine implements the following guarantees:

1. **Atomicity**: All child allocations are created in a single database transaction. If any allocation fails, the entire operation is rolled back.

2. **Idempotency**: Calling the allocation engine multiple times with the same parent transaction ID returns the same results without creating duplicates.

3. **Balance Updates**: Account balances are updated atomically with the transaction creation.

4. **Audit Trail**: All allocations are logged in the audit_log table.

### Allocation Flow

```
EXTERNAL_DEPOSIT (COMPLETED) created
    ↓
Allocation engine triggered automatically
    ↓
Find applicable allocation rule (by amount, priority)
    ↓
For each allocation in rule:
    - Create INTERNAL_ALLOCATION child transaction
    - Update source account balance (deduct)
    - Update target account balance (add)
    - Create audit log entry
    ↓
Commit all changes atomically
```

## Security

### Environment Variables

**Required**:
- `GUARDIAN_JWT_SECRET` - JWT secret for guardian authentication (min 32 chars)
- `DATABASE_URL` - PostgreSQL connection string

**Security Constraints**:
- `NFT_MINT_VALUE` must be `0` for testnet/development
- `APP_ENVIRONMENT` must be set correctly (development, testnet, mainnet)

### No Secrets in Repository

This repository contains **NO secrets**. All sensitive configuration is in `.env.example` as templates.

**Never commit**:
- Actual JWT secrets
- Database credentials
- Private keys
- API keys

### Pi Network Integration

Pi wallet verification is currently stubbed in `utils/pi_auth.py`. Future implementation will include:
- Signature verification for Pi wallet addresses
- Payment validation against Pi Network API
- Balance queries from Pi Network

## Deployment

### Testnet Deployment

1. Set up PostgreSQL database
2. Configure environment variables
3. Run Alembic migrations: `alembic upgrade head`
4. Deploy with Docker or directly with uvicorn
5. Verify health: `GET /health`

### Mainnet Deployment

**IMPORTANT**: Mainnet deployment requires:
- 5/5 Guardian approvals
- Separate mainnet PR and review process
- Production-grade database setup
- Proper secret management
- On-chain integration testing

## Monitoring

### Health Checks

```bash
# Basic health
curl http://localhost:8001/health

# API info
curl http://localhost:8001/
```

### Logs

```bash
# Docker Compose
docker-compose logs -f ledger-api

# Direct run (logs to stdout)
# Configure LOG_LEVEL environment variable
```

## Future Enhancements

### Planned Features

1. **Streamlit Dashboard**: Visual interface for treasury management
2. **On-chain Integration**: Full Pi Network payment verification
3. **Advanced Reconciliation**: Automated discrepancy resolution
4. **Multi-currency Support**: Support for multiple token types
5. **Scheduled Allocations**: Time-based automatic allocations
6. **Webhook Notifications**: Real-time alerts for transactions

### Pi Network Integration Roadmap

- [ ] Implement signature verification
- [ ] Integrate Pi Network SDK
- [ ] Add payment status polling
- [ ] Implement wallet balance queries
- [ ] Add smart contract interaction

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps

# Check database logs
docker-compose logs postgres

# Test connection
psql -U ledger_user -d ledger_db -h localhost
```

### JWT Authentication Errors

- Ensure `GUARDIAN_JWT_SECRET` is set and at least 32 characters
- Verify token includes both `sub` and `role` claims
- Check token hasn't expired (if exp claim is set)

### Allocation Not Triggering

- Verify transaction has `transaction_type: "EXTERNAL_DEPOSIT"`
- Ensure status is `"COMPLETED"`
- Check an active allocation rule exists for the amount range
- Review logs for error messages

## Contributing

See the main repository [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

See the main repository [LICENSE](../LICENSE) file.

## Support

For issues and questions:
- GitHub Issues: [pi-forge-quantum-genesis/issues](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues)
- Tag issues with `ledger-api` label

---

**Version**: 1.0.0  
**Status**: Testnet Ready  
**Last Updated**: 2025-12-11
