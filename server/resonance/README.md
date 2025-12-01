# Resonance Tracking System

This module handles the quantum resonance tracking algorithm and metric storage for the Pi Forge ecosystem.

## Overview

The resonance tracking system monitors the state of transactions and system health across the four phases:

1. **Foundation** (Red) - Initial connection establishment
2. **Growth** (Green) - Processing and expansion
3. **Harmony** (Blue) - Verification and balance
4. **Transcendence** (Purple) - Completion and elevation

## Algorithm

The resonance state is computed using the following formula:

```python
resonance_value = (ethical_score * 0.7 + qualia_impact * 3) / 10
```

### State Thresholds
- **Transcendence**: resonance_value >= 80
- **Harmony**: resonance_value >= 60
- **Growth**: resonance_value >= 40
- **Foundation**: resonance_value < 40

## Metric Storage

Metrics are stored in three tiers:

### Hot Storage (In-Memory)
- Real-time caches for dashboard updates
- 24-hour rolling window
- Used for WebSocket broadcasts

### Warm Storage (Supabase)
- PostgreSQL tables with RLS
- 90-day retention
- Queryable for historical analysis

### Cold Storage (Aggregated)
- Monthly summaries
- Annual archival
- Minimal footprint

## Files in this Directory

Future implementations will include:
- `tracker.py` - Core tracking logic
- `metrics.py` - Metric collection and aggregation
- `storage.py` - Multi-tier storage handlers
- `alerts.py` - Threshold monitoring and notifications

## Related Documentation

- [Telemetry Overview](../../docs/TELEMETRY.md)
- [Guardian Alerts](../../guardian_alerts.py)
