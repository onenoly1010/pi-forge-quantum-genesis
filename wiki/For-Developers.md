# 💻 For Developers - Developer Onboarding & Workflow

**Last Updated**: December 2025

Welcome, developer! This guide will help you contribute to the Quantum Pi Forge ecosystem.

---

## 🎯 Developer Quick Start

### 1. Understand the Foundation

Read these first:
- [[Genesis Declaration]] - Core principles
- [[Ecosystem Overview]] - Repository constellation  
- [[Canon of Closure]] - Development workflow
- [[Autonomous Agents]] - Agent system

### 2. Set Up Your Environment

```bash
# Clone repository
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis

# Install dependencies
pip install -r server/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

**Full setup**: [[Installation]]

### 3. Verify Your Setup

```bash
# Run tests
pytest

# Start development server
uvicorn server.main:app --reload

# Check health
curl http://localhost:8000/health
```

---

## 🏗️ Architecture Overview

### The Sacred Trinity

Three core services work together:

1. **FastAPI (Quantum Conduit)** - Port 8000
   - REST APIs
   - WebSocket connections
   - Pi Network authentication
   - Payment processing

2. **Flask (Glyph Weaver)** - Port 5000
   - Dynamic dashboards
   - SVG visualizations
   - Template rendering

3. **Gradio (Truth Mirror)** - Port 7860
   - AI interface
   - Model evaluation
   - Ethical AI tools

**Details**: [[Sacred Trinity]]

### Repository Structure

```
pi-forge-quantum-genesis/
├── server/              # Backend services
│   ├── main.py         # FastAPI application
│   ├── routes/         # API routes
│   ├── models/         # Data models
│   └── services/       # Business logic
├── api/                # Vercel serverless functions
├── contracts/          # Smart contracts
├── docs/               # Documentation
├── tests/              # Test suites
├── scripts/            # Utility scripts
└── wiki/               # This wiki (for manual transfer)
```

---

## 🔄 Development Workflow

### Following the Canon of Closure

We use the [[Canon of Closure]] 10-step cycle:

1. **Lint** - Clean code
2. **Host** - Isolated environment
3. **Test** - Verify behavior
4. **Pre-aggregate** - Telemetry
5. **Release** - Version tag
6. **Deploy** - Push live
7. **Rollback** - Recovery
8. **Monitor** - Observe
9. **Visualize** - Insights
10. **Alert** - Notifications

### Daily Development

```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Make changes
# ... code ...

# 3. Lint
black .
flake8 .

# 4. Test
pytest

# 5. Commit
git add .
git commit -m "feat: add your feature"

# 6. Push
git push origin feature/your-feature

# 7. Open Pull Request
# Use GitHub UI
```

---

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_api.py -v

# With coverage
pytest --cov=server --cov-report=html

# Integration tests
./scripts/test_pi_integration.sh
```

### Writing Tests

```python
# tests/test_feature.py
import pytest

def test_my_feature():
    """Test description following style."""
    # Arrange
    input_data = {"key": "value"}
    
    # Act
    result = my_function(input_data)
    
    # Assert
    assert result == expected
```

### Test Requirements

- ✅ All new code must have tests
- ✅ Maintain or improve coverage
- ✅ Follow existing test patterns
- ✅ Test edge cases
- ✅ Include integration tests for APIs

---

## 📝 Code Style

### Python Style

Follow PEP 8 with these tools:

```bash
# Format code
black .

# Check style
flake8 .

# Type checking (if using)
mypy server/
```

### Docstrings

```python
def process_payment(user_id: str, amount: float) -> dict:
    """
    Process a Pi Network payment.
    
    Args:
        user_id: User's Pi Network ID
        amount: Payment amount in Pi
        
    Returns:
        Payment record with transaction ID
        
    Raises:
        ValueError: If amount below minimum
        PaymentError: If payment processing fails
    """
    # Implementation
```

### Naming Conventions

- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

---

## 🔌 API Development

### Adding New Endpoints

```python
# server/routes/my_routes.py
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/myfeature", tags=["myfeature"])

@router.get("/items")
async def get_items():
    """Get all items."""
    return {"items": []}

@router.post("/items")
async def create_item(item: ItemModel):
    """Create new item."""
    return {"id": "123", "created": True}
```

Register route in `server/main.py`:

```python
from routes import my_routes

app.include_router(my_routes.router)
```

### API Documentation

- FastAPI auto-generates docs at `/docs`
- Add clear docstrings
- Include request/response examples
- Document error cases

**Reference**: [[API Reference]]

---

## 💰 Pi Network Integration

### Payment Flow

```python
from pi_network import PiNetwork

# Initialize
pi = PiNetwork(api_key=settings.PI_API_KEY)

# Create payment
payment = await pi.create_payment(
    user_id=user.pi_id,
    amount=1.5,
    memo="Service payment"
)

# Verify webhook
is_valid = pi.verify_webhook(
    signature=request.headers["x-pi-signature"],
    payload=request.body
)
```

### Testing Payments

1. Use sandbox mode: `PI_NETWORK_MODE=testnet`
2. Use sandbox credentials
3. Test webhook locally with ngrok
4. Verify database records

**Details**: [[Payment API]]

---

## 🤖 Working with Agents

### Agent Coordination

Autonomous agents handle routine tasks:
- Code review
- Testing
- Documentation
- Deployment

### Triggering Agents

Agents work via:
- GitHub Actions
- Issue labels
- PR comments
- Scheduled tasks

### Agent Guidelines

- Let agents handle routine work
- Review agent outputs
- Override when necessary
- Report agent issues

**Learn more**: [[Autonomous Agents]]

---

## 🗂️ Database

### Migrations

```bash
# Create migration
# Edit supabase_migrations/00X_description.sql

# Apply migration
# Run in Supabase SQL Editor or:
psql $DATABASE_URL < supabase_migrations/00X_description.sql
```

### Models

```python
# server/models/my_model.py
from pydantic import BaseModel
from datetime import datetime

class Payment(BaseModel):
    id: str
    user_id: str
    amount: float
    status: str
    created_at: datetime
```

---

## 🚀 Deployment

### Local Development

```bash
# Start all services
docker-compose up -d

# Or individual services:
uvicorn server.main:app --reload --port 8000
python server/flask_app.py --port 5000
python server/gradio_app.py --port 7860
```

### Staging Deployment

```bash
# Railway
railway up

# Vercel
vercel deploy
```

### Production Deployment

```bash
# Railway production
railway up --environment production

# Vercel production
vercel --prod
```

**Full guide**: [[Deployment Guide]]

---

## 🔍 Debugging

### Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Interactive Debugging

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or with ipdb
import ipdb; ipdb.set_trace()
```

### Remote Debugging

```bash
# Check logs
railway logs

# Stream logs
railway logs --follow

# Vercel logs
vercel logs
```

---

## 📊 Monitoring

### Local Monitoring

```bash
# Start observability stack
docker-compose up -d

# Access:
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000
```

### Production Monitoring

- Check deployment dashboards
- Review error logs
- Monitor performance metrics
- Set up alerts

**Details**: [[Monitoring Observability]]

---

## 🛡️ Security

### Best Practices

- ✅ Never commit secrets
- ✅ Use environment variables
- ✅ Validate all inputs
- ✅ Sanitize outputs
- ✅ Use parameterized queries
- ✅ Implement rate limiting
- ✅ Follow least privilege

### Security Review

All code undergoes:
1. Automated security scanning
2. Agent review
3. Guardian approval (if critical)

---

## 📚 Documentation

### Code Documentation

- Write clear docstrings
- Comment complex logic
- Keep README updated
- Update wiki pages

### API Documentation

- Use FastAPI docstrings
- Provide examples
- Document errors
- Include authentication

### Wiki Contributions

Edit pages in `/wiki/` directory:
```bash
# Edit page
nano wiki/My-Page.md

# Follow wiki style guide
# Use [[Wiki Links]]
# Add "Last Updated" date
```

---

## 🤝 Contributing

### Contribution Process

1. **Read** [[Contribution Guide]]
2. **Fork** repository
3. **Branch** from main
4. **Code** with tests
5. **Commit** with clear messages
6. **Push** to your fork
7. **PR** with description

### PR Guidelines

- Clear title and description
- Link related issues
- Include tests
- Pass all checks
- Request reviews

### Code Review

- Be respectful
- Be constructive
- Learn and teach
- Align with [[Genesis Declaration]]

**Full guide**: [[Contribution Guide]]

---

## 🎓 Learning Resources

### Essential Reading

- [[Genesis Declaration]] - Foundation
- [[Canon of Closure]] - Workflow
- [[Sacred Trinity]] - Architecture
- [[API Reference]] - API docs

### Advanced Topics

- [[Smart Contracts]] - Blockchain
- [[Guardian Playbook]] - Governance
- [[Monitoring Observability]] - Ops
- [[Verification System]] - Multi-chain

### External Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pi Network Docs](https://developers.pi/)
- [Python Best Practices](https://docs.python-guide.org/)

---

## 🆘 Getting Help

### Resources

- [[Troubleshooting]] - Common issues
- [[API Reference]] - API documentation
- [[Runbook Index]] - Operational commands

### Community

- GitHub Issues
- Pull Request discussions
- Contact @onenoly1010

---

## 🌟 Thank You!

Thank you for contributing to Quantum Pi Forge. Your work helps build an ethical, transparent, and inclusive AI platform.

**Welcome to the developer constellation.** 💻⚛️🔥

---

## See Also

- [[Installation]] - Setup guide
- [[Quick Start]] - Quick setup
- [[API Reference]] - API docs
- [[Deployment Guide]] - Deploy guide
- [[Contribution Guide]] - Contributing
- [[Troubleshooting]] - Common issues

---

[[Home]] | [[For Users]] | [[For Guardians]] | [[Contribution Guide]]
