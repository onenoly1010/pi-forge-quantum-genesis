# 📊 Telemetry

**Project Telemetry & Dashboards — Pi Forge Quantum Genesis**

This document describes the monitoring, metrics, and observability setup for the Quantum Pi Forge.

---

## Dashboard Overview

### Railway Dashboard (Primary)
- **URL**: https://railway.app/dashboard
- **Services Monitored**:
  - FastAPI Production (Port 8000)
  - Flask Dashboard (Port 5000)
  - Gradio Ethical Audit (Port 7860)

### Metrics Categories

| Category           | Metrics                                      | Alert Threshold        |
|--------------------|---------------------------------------------|------------------------|
| Latency            | Request response time, WebSocket latency    | > 5 ns for critical    |
| Throughput         | Requests/second, WebSocket connections      | < 100 req/s warning    |
| Error Rate         | 4xx/5xx responses, failed authentications   | > 1% critical          |
| Resource Usage     | CPU, Memory, Network I/O                    | > 80% warning          |
| Resonance State    | Phase transitions, audit scores             | Deviation > 10%        |

---

## Health Endpoints

### FastAPI (Production)
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy", "service": "FastAPI", "supabase": "connected"}
```

### Flask (Dashboard)
```bash
curl http://localhost:5000/health
# Response: {"status": "healthy", "message": "Pi Forge Quantum Genesis"}
```

### Gradio (Ethical Audit)
```bash
# Access UI directly
open http://localhost:7860
```

---

## Logging Configuration

### Log Levels

| Level   | Usage                                    |
|---------|------------------------------------------|
| DEBUG   | Development troubleshooting              |
| INFO    | Standard operational logs                |
| WARNING | Non-critical issues, degraded state      |
| ERROR   | Failures requiring attention             |
| CRITICAL| System-wide failures, immediate action   |

### Log Format
```
[TIMESTAMP] [LEVEL] [SERVICE] [MESSAGE] [CONTEXT]
```

Example:
```
[2025-12-01T12:00:00Z] [INFO] [FastAPI] Payment verified [tx_hash=abc123, user_id=xyz789]
```

---

## Alerting Rules

### Critical Alerts (Immediate Action)
- Service down for > 1 minute
- Error rate > 5%
- Latency breach > 6 ns sustained
- Authentication service unavailable

### Warning Alerts (Review within 1 hour)
- Error rate > 1%
- Memory usage > 80%
- Resonance state deviation > 10%
- Slow query detection (> 100ms)

---

## Dashboard Setup (Future)

### Prometheus + Grafana Stack
```yaml
# prometheus.yml (proposed)
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'pi-forge-fastapi'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /metrics
    
  - job_name: 'pi-forge-flask'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: /metrics
```

### Key Grafana Panels (Proposed)
1. **Quantum Resonance Overview**: Real-time phase distribution
2. **Payment Flow**: Transaction success rate, latency
3. **Ethical Audit Score**: Rolling average, trend analysis
4. **System Health**: CPU, Memory, Active connections

---

## Resonance Metrics

### Phase Distribution Tracking
```python
# Metrics exported from main.py
resonance_phase_counter = Counter(
    'resonance_phase_total',
    'Total phase transitions',
    ['phase']  # foundation, growth, harmony, transcendence
)
```

### Ethical Scoring
```python
# Metrics from canticle_interface.py
audit_score_histogram = Histogram(
    'ethical_audit_score',
    'Distribution of ethical audit scores',
    buckets=[0.0, 0.25, 0.5, 0.75, 0.9, 0.95, 1.0]
)
```

---

## External Service Status

| Service    | Status Page                           | Integration    |
|------------|--------------------------------------|----------------|
| Supabase   | https://status.supabase.com          | Auth + DB      |
| Railway    | https://status.railway.app           | Deployment     |
| Pi Network | https://minepi.com/status            | Payments       |

---

*© 2025 Pi Forge Collective — Quantum Genesis Initiative*
