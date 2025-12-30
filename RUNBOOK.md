# 🧾 RUNBOOK: Pi-Forge Quantum Genesis

This runbook provides **step-by-step operational commands** for maintaining, testing, releasing, and recovering the system.  
It complements `HANDOFF.md` by offering executable instructions.

---

## 🔍 Syntax Closure
**Purpose:** Ensure code is clean and free of syntax errors.

```bash
# Format code
black .

# Lint code
flake8 .

# Run pre-commit hooks
pre-commit run --all-files
```

---

## 🧪 Healthcheck Alignment
**Purpose:** Verify endpoints and system health.

```bash
# Run health tests
pytest tests/test_health.py -q

# Check metrics endpoint manually
curl http://localhost:8000/api/metrics
```

---

## 🌐 Production Endpoints

| Service | Local Development | Production | Status |
|---------|-------------------|------------|--------|
| **Core API** | `http://localhost:8000` | `https://pi-forge-quantum-genesis.railway.app` | ✅ Live |
| **Resonance** | `http://localhost:8001` | `https://quantum-resonance-clean.vercel.app` | ⚠️ Exposed |
| **Site** | `http://localhost:3000` | `https://onenoly1010.github.io/quantum-pi-forge-site/` | ✅ Live |

> **Full deployment status:** See [docs/DEPLOYMENT_STATUS.md](./docs/DEPLOYMENT_STATUS.md)

---

## 📡 Telemetry Ceremony
**Purpose:** Control OpenTelemetry collector in local vs CI environments.

### Local Development with Full Observability Stack

```bash
# Start OpenTelemetry Collector, Prometheus, and Grafana
docker-compose up -d

# Verify services are running
docker-compose ps

# View logs
docker-compose logs -f otel-collector

# Stop all services
docker-compose down
```

**Access Points:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)
- OTLP HTTP Receiver: http://localhost:4318
- OTLP gRPC Receiver: http://localhost:4317

### Run Application with Telemetry Control

```bash
# Run with telemetry enabled (connects to docker-compose stack)
ENABLE_TELEMETRY=true python server/main.py

# Run with telemetry disabled (for CI or offline testing)
ENABLE_TELEMETRY=false python server/main.py

# Run tests with telemetry disabled (prevents connection errors)
ENABLE_TELEMETRY=false pytest
```

### Configuration Files

- `docker-compose.yml` - Full observability stack configuration
- `otel-collector-config.yaml` - OpenTelemetry Collector configuration
- `prometheus.yml` - Prometheus scrape configuration

---

## ⚙️ CI/CD Rituals

### Lint & Test Workflow (local validation)
```bash
pytest --maxfail=1 --disable-warnings -q
```

### Release Ritual (manual trigger)
```bash
# Tag release
git tag v1.0.0
git push origin v1.0.0
```

### Vercel Deployment Ritual
```bash
# Deploy to Vercel (requires secrets configured)
vercel --prod
```

---

## 🔄 Rollback Ritual
**Purpose:** Revert to last stable release if deployment fails.

```bash
# Checkout last stable tag
git checkout $(git describe --tags --abbrev=0)

# Rebuild and redeploy
npm run build
vercel --prod
```

---

## 📡 Monitoring Ritual
**Purpose:** Observe failures and rollbacks.

- Grafana Dashboard: `http://localhost:3000`
- Prometheus Metrics: `http://localhost:9090`

---

## 📊 Visualization Ritual
**Purpose:** Import dashboards.

1. Go to Grafana → Dashboards → Import.
2. Upload `pi-forge-dashboard.json`.

---

## 🚨 Alert Ritual
**Purpose:** Ensure alerts propagate.

- Slack webhook: stored in `SLACK_WEBHOOK_URL` (format: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`)
- Email credentials: stored in `EMAIL_USERNAME` / `EMAIL_PASSWORD`

---

## 📜 Canonical Circle
**Lint → Test → Release → Deploy → Rollback → Monitor → Visualize → Alert → Pre‑aggregate**

---

✨ This runbook is the **operational script**: follow it step by step to maintain closure and resilience.
