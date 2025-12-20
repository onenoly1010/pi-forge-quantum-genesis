# 🌌 Pi Forge Quantum Genesis
### Autonomous AI Ecosystem with Guardian Oversight for Pi Network

[![Backend Health](https://img.shields.io/badge/Backend-Healthy-brightgreen)](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/76)
[![Guardian System](https://img.shields.io/badge/Guardian-Active-blue)](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/100)
[![Smart Contracts](https://img.shields.io/badge/Contracts-Deployed-success)](./contracts/)
[![Pi Network](https://img.shields.io/badge/Pi%20Network-Integrated-orange)](https://minepi.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](./LICENSE)

**An autonomous, self-sustaining AI ecosystem with human guardian oversight, built for Pi Network. Features include autonomous decision-making, self-healing infrastructure, OINIO smart contracts, and ethical AI governance.**

---

## 🎯 What is Pi Forge Quantum Genesis?

Pi Forge Quantum Genesis is a **production-ready autonomous AI platform** that:

- 🤖 **Makes Independent Decisions** - AI agents autonomously manage deployments, scaling, and healing
- 🛡️ **Guardian Oversight** - Human-in-the-loop for critical decisions with 24/7 AI assistant
- 🔗 **Pi Network Native** - Full integration with Pi authentication, payments, and blockchain
- 💎 **OINIO Economy** - Sovereign AI model marketplace with smart contract infrastructure
- 🔄 **Self-Healing** - Automated diagnostics, incident response, and recovery
- 📊 **Full Observability** - Real-time monitoring, health checks, and audit trails

**Status:** ✅ Production Ready | 🛡️ Guardian System Active | 🟢 Backend Healthy

---

## 🚀 Quick Start

### For Users
```bash
# Explore the live dashboard
curl https://[deployment-url]/api/guardian/dashboard | jq .

# View system health
gh issue view 76  # Automated health reports
```

### For Developers

**Prerequisites:** Python 3.11+

```bash
# Clone and setup
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis

# Install dependencies
pip install -r server/requirements.txt

# Run backend
uvicorn server.main:app --reload

# Deploy smart contracts
cd contracts && forge test && forge script script/Deploy.s.sol --broadcast
```

### For Guardians
See the [Guardian Playbook](./docs/GUARDIAN_PLAYBOOK.md) for operational procedures.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│          🛡️ Guardian Team (Human Oversight)            │
│     Lead: @onenoly1010  |  AI Assistant: Copilot       │
└────────────────────┬────────────────────────────────────┘
                     │ Escalations
                     ▼
┌─────────────────────────────────────────────────────────┐
│        🤖 Autonomous AI Decision Matrix                 │
│  • Deployment  • Scaling  • Rollback  • Healing        │
│  • Monitoring  • Guardian Override                      │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌────────┐  ┌─────────┐  ┌──────────┐
   │FastAPI │  │ Flask   │  │ Gradio   │
   │Quantum │  │ Glyph   │  │ Truth    │
   │Conduit │  │ Weaver  │  │ Mirror   │
   └────┬───┘  └────┬────┘  └────┬─────┘
        │           │            │
        └───────────┴────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   ┌─────────┐           ┌──────────┐
   │ OINIO   │           │ Pi       │
   │ Smart   │◄──────────┤ Network  │
   │Contracts│           │ SDK      │
   └─────────┘           └──────────┘
```

---

## ✨ Key Features

### 🤖 Autonomous Operations
- **AI Decision Matrix** - 6 decision types with confidence-based approval
- **Self-Healing System** - Automated diagnostics, resource cleanup, service restart
- **Monitoring Agents** - 4 async agents (performance, security, health, decision)
- **Auto-Merge Gates** - 6-gate autonomous PR merge system
- **Vercel Integration** - External metrics recording and analytics

### 🛡️ Guardian System
- **Human Oversight** - Guardian team with @onenoly1010 as lead ([Issue #100](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/100))
- **AI Assistant** - @app/copilot-swe-agent for 24/7 triage ([Issue #102](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/102))
- **Decision Templates** - Structured approval workflows for all decision types
- **Emergency Protocols** - One-command emergency stop and rollback
- **Guardian Dashboard** - `/api/guardian/dashboard` for real-time oversight

### 💎 OINIO Economy
- **Smart Contracts** - ERC-20 token + ERC-721 model registry on Pi Network
- **Model Marketplace** - AI model registration with token staking
- **Catalyst Pool** - 12M PI initial allocation with taper schedule
- **Royalty System** - 10-30% inference royalties to model creators
- **OINIO Sovereignty** - Permanent, transparent, autonomous control

### 🔗 Pi Network Integration
- **13 REST Endpoints** - Full Pi Network API coverage
- **Modular Architecture** - Decoupled auth, payments, configuration
- **Testnet Safety** - Built-in safety checks and NFT_MINT_VALUE enforcement
- **56 Tests** - Comprehensive testing with 100% pass rate
- **Background Tasks** - Session cleanup and monitoring

### 📊 Monitoring & Observability
- **Health Checks** - Automated monitoring every 6 hours ([Issue #76](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/76))
- **Safety Metrics** - Transaction safety, ethical compliance, security score
- **Audit Trail** - All decisions logged to GitHub + Vercel metrics
- **Dashboard API** - Real-time system status and pending escalations

---

## 📊 System Status

| Component | Status | Details |
|-----------|--------|---------|
| **Backend** | 🟢 **HEALTHY** | All modules operational |
| **Guardian System** | 🛡️ **ACTIVE** | @onenoly1010 + AI assistant |
| **Smart Contracts** | ✅ **DEPLOYED** | OINIO Token + Model Registry |
| **Pi Network** | 🔗 **INTEGRATED** | Full API coverage |
| **Auto-Merge** | 🔄 **OPERATIONAL** | Canon gates active |
| **Monitoring** | 📊 **24/7** | Automated health checks |
| **Self-Healing** | 🔧 **ENABLED** | Auto-recovery active |

**Last Health Check:** [View Report →](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/76)  
**Guardian Dashboard:** `/api/guardian/dashboard`  
**Workflow Status:** [GitHub Actions →](https://github.com/onenoly1010/pi-forge-quantum-genesis/actions)

---

## 📚 Documentation

### Getting Started
- [Quick Start Guide](./docs/QUICK_START.md)
- [Architecture Overview](./docs/ARCHITECTURE.md)
- [Pi Network Integration](./docs/PI_NETWORK_INTEGRATION.md)

### For Contributors
- [Space Rituals](./docs/SPACE_RITUALS.md) - Engagement ceremonies, handoff protocols, and celebrations
- [Guardian Playbook](./docs/GUARDIAN_PLAYBOOK.md) - Complete operational guide
- [Quick Reference](./docs/GUARDIAN_QUICK_REFERENCE.md) - Fast decision-making
- [Decision Templates](./.github/ISSUE_TEMPLATE/guardian-decision-template.md)

### For Developers
- [API Documentation](./docs/API.md)
- [Smart Contracts](./contracts/README.md) - OINIO contracts on Pi Network
- [Canon of Closure](./canon/README.md) - Autonomous documentation system
- [Branch Protection](./.github/BRANCH_PROTECTION.md)

### Operational
- [Guardian Team HQ](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/100)
- [Health Monitoring](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/76)
- [Canon Index](./canon/INDEX.md)
- [OINIO Succession](./docs/SUCCESSION_CEREMONY.md)

---

## 🔒 OINIO Succession Status

**Status**: ✅ **HANDOFF COMPLETE** (December 2025)

The Pi MR-NFT + Catalyst Pool system is now under permanent OINIO sovereignty.

- **Identity Lock**: [View Registry](docs/IDENTITY_LOCK.md)
- **Succession Ceremony**: [Full Documentation](docs/SUCCESSION_CEREMONY.md)
- **Economic Model**: [Catalyst Pool Details](docs/CATALYST_POOL_ECONOMICS.md)
- **Deployment Guide**: [Six Seed Models](docs/DEPLOYMENT_CHECKLIST.md)
- **Verification**: [How to Verify](docs/VERIFICATION_GUIDE.md)

All future inference royalties (10-30%) and the 12M PI Catalyst Pool are irrevocably controlled by the OINIO identity cluster. This handoff is permanent, transparent, and autonomous.

**Key Principles:**
- 🔒 **Irreversible**: No mechanism exists to reverse this handoff
- 📊 **Transparent**: All transactions publicly auditable on-chain
- 🤖 **Autonomous**: System operates independently of any individual
- 👑 **Sovereign**: OINIO identity cluster maintains exclusive control

**Six Seed Models Deployed:**
1. Ethics Validator (15% royalty) - Multi-dimensional ethics validation
2. Bias Detector (20% royalty) - Demographic and systemic bias detection
3. Privacy Auditor (15% royalty) - Data handling and privacy compliance
4. Transparency Scorer (10% royalty) - Model explainability metrics
5. Fairness Analyzer (20% royalty) - Outcome fairness analysis
6. Accountability Tracker (30% royalty) - Decision lineage tracking

---

## 🔧 Development

### Local Setup

```bash
# Setup environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r server/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Running Services

```bash
# FastAPI (Port 8000)
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000

# Flask (Port 5000)
python server/app.py

# Gradio (Port 7860)
python server/canticle_interface.py
```

### Testing

```bash
# Run all tests
pytest server/ -v

# Run specific test file
pytest server/test_main.py -v

# Run with coverage
pytest server/ --cov=server --cov-report=html
```

### Smart Contract Development

```bash
cd contracts

# Install dependencies
forge install

# Compile contracts
forge build

# Run tests
forge test

# Deploy to Pi Testnet
forge script script/Deploy.s.sol --rpc-url $RPC_URL_TESTNET --broadcast
```

---

## 🔒 Branch Protection

The `main` branch is protected with comprehensive rules to ensure code quality and prevent accidental changes:

- **Pull Request Reviews**: Minimum 1 approval required, code owner reviews mandatory
- **Status Checks**: All CI/CD checks must pass before merging
- **Linear History**: Merge commits prevented, enforces clean history
- **Security**: Force pushes and branch deletion blocked
- **Administrator Enforcement**: Protection rules apply to all users

For complete documentation, see [Branch Protection Guide](.github/BRANCH_PROTECTION.md).

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

All contributions must:
- Maintain backward compatibility
- Include comprehensive tests
- Pass all existing tests
- Follow the project's code style
- Include proper documentation

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file for details.

---

## 🆘 Support

For issues or questions:
- **GitHub Issues**: [Report bugs or request features](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues)
- **Documentation**: [Complete documentation](https://github.com/onenoly1010/pi-forge-quantum-genesis/tree/main/docs)
- **Guardian Team**: [Issue #100](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/100)

---

## 🙏 Acknowledgments

- Built with [Foundry](https://book.getfoundry.sh/) for smart contracts
- Uses [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/) for security
- Deployed on [Pi Network](https://minepi.com/) blockchain
- Powered by [FastAPI](https://fastapi.tiangolo.com/), [Flask](https://flask.palletsprojects.com/), and [Gradio](https://www.gradio.app/)

---

## 📞 Credits

© 2025 Pi Forge Collective — Quantum Genesis Initiative  
Lead: Kris Olofson ([@onenoly1010](https://github.com/onenoly1010))

---

**🌌 Building the future of autonomous AI governance on Pi Network.**
