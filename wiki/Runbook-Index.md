# 📖 Runbook Index - Operational Procedures

**Last Updated**: December 2025

Complete operational procedures following the [[Canon of Closure]] framework.

---

## 🔄 Canon of Closure Operations

### 1. 🧹 Lint - Syntax Closure
```bash
black .
flake8 .
pre-commit run --all-files
```

### 2. 🏠 Host - Environment Closure
```bash
python -m venv .venv
source .venv/bin/activate
docker-compose up -d
```

### 3. 🧪 Test - Validation Closure
```bash
pytest --maxfail=1 --disable-warnings -q
pytest tests/test_health.py -v
```

### 4. 📊 Pre-aggregate - Telemetry Closure
```bash
docker-compose up -d otel-collector
ENABLE_TELEMETRY=true python server/main.py
```

### 5. 📦 Release - Version Closure
```bash
git tag v1.0.0
git push origin v1.0.0
```

### 6. 🚀 Deploy - Launch Closure
```bash
railway up
# or
vercel --prod
```

### 7. 🔄 Rollback - Recovery Closure
```bash
git checkout $(git describe --tags --abbrev=0)
railway up
```

### 8. 📡 Monitor - Observation Closure
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

### 9. 📊 Visualize - Insight Closure
- View dashboards in Grafana
- Generate reports

### 10. 🚨 Alert - Response Closure
- Check Slack/email notifications
- Respond to guardian alerts

---

## 🚨 Emergency Procedures

### System Down
```bash
# Check health
curl https://your-app.railway.app/health

# View logs
railway logs --follow

# Restart service
railway restart
```

### Database Issues
```bash
# Check connection
psql $DATABASE_URL -c "SELECT 1"

# Run migrations
psql $DATABASE_URL < supabase_migrations/001_*.sql
```

### Payment Failures
```bash
# Check Pi Network status
curl https://your-app/api/pi-network/status

# Review payment logs
railway logs | grep "payment"
```

---

## See Also

- [[Canon of Closure]] - Framework details
- [[Deployment Guide]] - Deployment procedures
- [[Troubleshooting]] - Common issues
- [[Monitoring Observability]] - Monitoring setup

---

[[Home]] | [[Canon of Closure]] | [[Troubleshooting]]
