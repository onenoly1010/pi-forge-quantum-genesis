# Telemetry Overview

> *Understanding the resonance metrics that drive system health*

## Philosophy

Telemetry in Pi Forge follows the principle of **Ethical Observability**:
- Collect only what improves the system
- Anonymize by default
- Full transparency with users
- Opt-in for detailed metrics

---

## Core Metrics

### Resonance Health
| Metric | Description | Collection Frequency |
|--------|-------------|---------------------|
| `resonance_state` | Current phase (foundation/growth/harmony/transcendence) | Real-time |
| `coherence_score` | System stability measure (0-100) | Every 30 seconds |
| `entropy_level` | Disorder metric, lower is better | Every minute |

### Transaction Metrics
| Metric | Description | Collection Frequency |
|--------|-------------|---------------------|
| `tx_count` | Total transactions processed | Per transaction |
| `tx_latency_ms` | Processing time in milliseconds | Per transaction |
| `tx_success_rate` | Percentage of successful transactions | Aggregated hourly |

### Ethical Audit Metrics
| Metric | Description | Collection Frequency |
|--------|-------------|---------------------|
| `audit_risk_score` | Risk assessment (0.0-1.0) | Per audit |
| `branch_simulations` | Number of "what-if" scenarios tested | Per audit |
| `narrative_quality` | Teaching effectiveness score | Per audit |

---

## Data Storage

### Short-term (Hot Storage)
- In-memory caches for real-time dashboards
- 24-hour rolling window

### Medium-term (Warm Storage)
- Supabase PostgreSQL tables
- 90-day retention

### Long-term (Cold Storage)
- Aggregated summaries only
- Annual archival

---

## Privacy Safeguards

### Data Minimization
- No personally identifiable information in metrics
- User IDs are hashed before storage
- IP addresses never logged

### Access Control
- Metrics accessible only to guardians
- Audit trail for all access
- Regular access reviews

### User Rights
- Export personal data on request
- Delete historical data
- Opt-out of all non-essential collection

---

## Dashboard Access

### Internal Dashboard
```
http://localhost:5000/resonance-dashboard
```
Displays real-time resonance state, archetype distributions, and system health.

### Metrics Endpoints
- `GET /health` - Basic health check
- `GET /metrics` - Prometheus-compatible metrics (when enabled)

---

## Alerting

Alerts are configured through `guardian_alerts.py`:
- **Warning**: Coherence score drops below 70
- **Critical**: Coherence score drops below 50
- **Emergency**: System enters unstable resonance state

See [GUARDIANS.md](./GUARDIANS.md) for escalation procedures.

---

*Telemetry specification version: 1.0.0*
*Last updated: {current_date}*
