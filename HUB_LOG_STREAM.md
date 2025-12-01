# 🔥 HUB LOG STREAM — Covenant Ledger

## Purpose
The HUB_LOG_STREAM is the eternal, append-only JSONL ledger.  
Every ritual commit becomes a public event, visible at:  
**https://quantumpiforge.com/stream**

## Specification
- **Format**: JSON Lines (`.jsonl`)
- **Fields**:
  - `timestamp` (ISO 8601)
  - `glyph` (guardian glyph)
  - `vow` (commit vow prefix: INGEST, AUDIT, BROADCAST, RESONANCE, etc.)
  - `message` (commit message body)
  - `wallet` (guardian wallet address, truncated)
  - `seal` (cryptographic signature)

## Example Entries
```json
{"timestamp":"2025-12-01T12:00:00Z","glyph":"🔨","vow":"INGEST","message":"root_hash verified","wallet":"GCREOJTBR2JD6...","seal":"0xabc123"}
{"timestamp":"2025-12-01T12:15:00Z","glyph":"🛡️","vow":"AUDIT","message":"ethical audit complete","wallet":"GCREOJTBR2JD6...","seal":"0xdef456"}
```

## GitHub Action Integration
- Workflow appends each commit event to `/resonance/stream.jsonl`
- Pushes updates to quantumpiforge.com transparency hub
