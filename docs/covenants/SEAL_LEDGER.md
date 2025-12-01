# 🛡️ SEAL LEDGER — Guardian Covenant

## Purpose
The SEAL_LEDGER is the immutable record of every guardian seal.  
It binds signatures to vows, ensuring accountability and remembrance.

## Structure
- **File**: `docs/covenants/SEAL_LEDGER.md`
- **Entries**:
  - Guardian glyph
  - GitHub handle
  - Wallet address
  - Seal signature (cryptographic)
  - Date enacted
  - Merkle root reference

## Example Entry
- Glyph: 🔨 Forgekeeper  
- Guardian: @kris-olofson  
- Wallet: GCREOJTBR2JD6...  
- Seal: `0xabc123`  
- Date: 2025-12-01  
- Merkle Root: `merkle_root_2025_12_01`

## Verification Ceremony
- Script: `scripts/verify_seals.py`
- Publishes Merkle root to Pi Network mainnet
- Broadcasts verification to HUB_LOG_STREAM
