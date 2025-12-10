# 🔐 Hephaestus Guardian Coordinator

A semi-autonomous Guardian Coordination system for Pi Forge Quantum Genesis, enabling secure multisig governance, human-in-the-loop approval flows, and Discord-based guardian coordination.

## 🌟 Overview

The Guardian Coordinator implements a robust governance framework with:

- **Discord Bot Interface**: Slash commands for proposal creation and voting
- **FastAPI Backend**: REST API for proposal management and vote recording
- **Multi-signature Support**: Quorum-based approval system
- **Database Integration**: Supabase/PostgreSQL compatible schema
- **Pi Network Integration**: Testnet NFT minting and authentication stubs

## 🏗️ Architecture

```
guardian-coordinator/
├── src/
│   ├── bot/              # Discord bot with slash commands
│   ├── api/              # FastAPI backend endpoints
│   ├── models/           # Pydantic data models
│   └── utils/            # Multisig and auth utilities
├── scripts/              # CLI tools for guardian operations
├── tests/                # Pytest unit tests
├── docker/               # Docker configuration
└── db/                   # Database schema
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (or Supabase account)
- Discord Bot Token
- Pi Network Testnet API Key (for full integration)

### Local Development Setup

1. **Clone and navigate to the guardian-coordinator directory:**

```bash
cd guardian-coordinator
```

2. **Create virtual environment and install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables:**

```bash
cp .env.example .env
# Edit .env with your actual credentials
```

4. **Initialize the database:**

```bash
# Apply the schema to your PostgreSQL/Supabase instance
psql -U your_user -d your_database -f db/schema.sql

# Or use Supabase SQL Editor to run db/schema.sql
```

5. **Run the FastAPI backend:**

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
```

6. **In a separate terminal, run the Discord bot:**

```bash
python src/bot/discord_bot.py
```

### Docker Deployment

Run all services with Docker Compose:

```bash
docker-compose -f docker-compose.guardian.yml up --build
```

This starts:
- **guardian-api**: FastAPI backend on port 8001
- **guardian-bot**: Discord bot service
- **guardian-db**: PostgreSQL database on port 5433

## 📋 Environment Variables

Configure these in your `.env` file (see `.env.example` for template):

### Required

- `DATABASE_URL`: PostgreSQL connection string (or use Supabase settings)
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Supabase anonymous/service key
- `DISCORD_BOT_TOKEN`: Discord bot token from Discord Developer Portal
- `DISCORD_GUARDIAN_CHANNEL_ID`: Channel ID where guardian commands work
- `GUARDIAN_JWT_SECRET`: Secret for JWT token signing (generate with `openssl rand -hex 32`)

### Optional

- `PI_TESTNET_API_KEY`: Pi Network testnet API key
- `API_HOST`: API hostname (default: localhost)
- `API_PORT`: API port (default: 8001)

## 🎮 Usage

### Creating a Proposal via Discord

1. In your Discord server's guardian channel, use:

```
/guardian_propose action:deploy_contract description:Deploy NFT minting contract params:{"contract":"GuardianNFT"}
```

2. Guardians vote using:

```
/guardian_vote proposal_id:1 vote:approve
```

3. Once quorum is reached, the proposal auto-executes

### Creating a Proposal via API

```bash
curl -X POST http://localhost:8001/api/guardian/proposal \
  -H "Content-Type: application/json" \
  -d '{
    "action": "deploy_contract",
    "description": "Deploy Guardian NFT contract",
    "params": {"contract": "GuardianNFT"},
    "proposer": "guardian1"
  }'
```

### Voting via API

```bash
curl -X POST http://localhost:8001/api/guardian/vote/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "guardian_id": "guardian1",
    "vote": "approve"
  }'
```

### CLI Tools

**Onboard a new guardian via CLI:**

```bash
python scripts/guardian_onboard.py --guardian-id guardian1 --description "Add new guardian"
```

**Check quorum status:**

```bash
python scripts/quorum_check.py --proposal-id 1
```

**Simulate NFT mint (testnet):**

```bash
python scripts/nft_mint.py --recipient guardian1 --token-uri ipfs://...
```

## 🔑 API Endpoints

### Proposals

- `POST /api/guardian/proposal` - Create a new proposal
- `GET /api/guardian/proposals` - List active proposals
- `GET /api/guardian/proposals/{id}` - Get proposal details

### Voting

- `POST /api/guardian/vote/{proposal_id}` - Submit a vote
- `GET /api/guardian/vote/{proposal_id}` - Get voting status

### Execution

- `POST /api/guardian/execute` - Execute approved proposal (admin only)

### Health Check

- `GET /health` - Service health status

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_guardian_flows.py -v
```

## 🔒 Security Notes

**⚠️ CRITICAL SECURITY GUIDELINES:**

1. **Never commit secrets**: All sensitive data must be in `.env` (gitignored)
2. **Use environment variables**: Load all credentials from environment at runtime
3. **JWT secrets**: Generate strong secrets with `openssl rand -hex 32`
4. **Testnet only**: All blockchain operations are stubs for testnet only
5. **Database migrations**: Use Supabase migrations or controlled SQL scripts
6. **Discord permissions**: Restrict bot commands to designated guardian roles
7. **API authentication**: All endpoints require valid JWT tokens in production
8. **Rate limiting**: Implement rate limiting in production deployments

### Generating Test JWT Tokens

For local testing, you can generate test tokens:

```python
import jwt
import os
from datetime import datetime, timedelta

secret = os.getenv("GUARDIAN_JWT_SECRET")
payload = {
    "guardian_id": "test_guardian",
    "exp": datetime.utcnow() + timedelta(hours=1)
}
token = jwt.encode(payload, secret, algorithm="HS256")
print(f"Test token: {token}")
```

## 📊 Database Schema

The system uses two main tables:

### `guardians`
- Stores guardian identity, public keys, and status

### `guardian_proposals`
- Tracks proposals, votes, and execution status

See `db/schema.sql` for complete schema.

## 🔄 Workflow Example

1. Guardian creates proposal via Discord `/guardian_propose`
2. Bot calls API to create proposal record
3. Bot creates Discord thread for discussion
4. Guardians vote via `/guardian_vote` in thread
5. Each vote is recorded via API
6. When quorum reached (e.g., 3/5 guardians), proposal auto-executes
7. Results posted to Discord thread

## 🚧 Roadmap

Future enhancements planned:

- [ ] Supabase real-time subscriptions for vote updates
- [ ] On-chain multisig contract integration
- [ ] NFT-based guardian proof of authority
- [ ] Discord role-based permission enforcement
- [ ] Automated CI/CD pipeline with tests
- [ ] Enhanced security auditing and logging
- [ ] WebSocket notifications for real-time updates
- [ ] Guardian reputation scoring system

## 📝 Development Notes

### Adding New Actions

To add a new proposal action type:

1. Update the action enum in `src/models/approval.py`
2. Add execution logic in `src/api/approval_flows.py`
3. Add Discord command help text in `src/bot/guardian_commands.py`
4. Add tests in `tests/test_guardian_flows.py`

### Debugging

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python src/bot/discord_bot.py
```

## 🤝 Contributing

This is an internal component of Pi Forge Quantum Genesis. For issues or enhancements, coordinate with the core development team.

## 📜 License

Part of Pi Forge Quantum Genesis - (c) 2025 Pi Forge Collective

## 👥 Maintainers

- Lead: Kris Olofson (onenoly11)
- Guardian Coordinator: Hephaestus Protocol Team

---

**Note**: This system is in active development. All on-chain operations are stubs for testnet/development only. Never use mainnet credentials or private keys in configuration files.
