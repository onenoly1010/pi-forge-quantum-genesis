# 📊 Monitoring & Observability - OpenTelemetry, Prometheus, Grafana

**Last Updated**: December 2025

Complete observability stack for monitoring system health, performance, and distributed tracing.

---

## 🎯 Stack Overview

- **OpenTelemetry** - Distributed tracing
- **Prometheus** - Metrics collection
- **Grafana** - Visualization dashboards
- **Docker Compose** - Local stack

---

## 🚀 Quick Start

### Start Observability Stack

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f otel-collector
```

### Access Points

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **OTLP HTTP**: http://localhost:4318
- **OTLP gRPC**: http://localhost:4317

---

## 📡 OpenTelemetry Tracing

### Enable Tracing

```bash
# In environment
ENABLE_TELEMETRY=true

# Start application
python server/main.py
```

### Instrumentation

All [[Sacred Trinity]] services instrumented:

**FastAPI**: Authentication, payments, WebSocket  
**Flask**: SVG generation, dashboards  
**Gradio**: Ethical audits, model evaluation

---

## 📊 Prometheus Metrics

### Key Metrics

- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `payment_processing_total` - Payment operations
- `system_health_status` - Health check results

### Query Examples

```promql
# Request rate
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{status=~"5.."}[5m])
```

---

## 📈 Grafana Dashboards

### Pre-built Dashboards

1. **System Overview** - Health, uptime, errors
2. **API Performance** - Latency, throughput, errors
3. **Payment Monitoring** - Payment success/failure rates
4. **Database Metrics** - Query performance, connections

### Import Dashboard

1. Open Grafana (http://localhost:3000)
2. Go to Dashboards → Import
3. Upload `grafana-dashboards/*.json`

---

## 🚨 Alerting

### Configure Alerts

**Prometheus** (`prometheus.yml`):
```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']

rule_files:
  - 'alerts.yml'
```

**Alert Rules** (`alerts.yml`):
```yaml
groups:
  - name: system_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        annotations:
          summary: "High error rate detected"
```

### Notification Channels

- **Slack**: Webhook integration
- **Email**: SMTP configuration
- **PagerDuty**: For critical alerts

---

## See Also

- [[Sacred Trinity]] - Service architecture
- [[Deployment Guide]] - Deployment procedures
- [[Runbook Index]] - Operational commands
- [[For Guardians]] - Guardian monitoring

---

[[Home]] | [[Sacred Trinity]] | [[Runbook Index]]
