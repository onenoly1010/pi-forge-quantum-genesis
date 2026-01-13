# 🏛️ CANONICAL ARCHITECTURE - Source of Truth

**Last Updated:** January 13, 2026  
**Status:** 🟢 LOCKED — SOVEREIGN SPINE ESTABLISHED  

---

## 🎯 THE SOVEREIGN SPINE

This document defines the **authoritative repositories** for the Quantum Pi Forge ecosystem.  
**These four repos are the ONLY sources of production reality.**  
All other repos are supportive, experimental, or archived.

---

## ⚡ PRODUCTION CANONICAL REPOSITORIES

These repos define production reality and system behavior:

| Layer | Canonical Repo | Authority | Status |
|-------|----------------|-----------|--------|
| **Frontend / User Reality** | `quantum-pi-forge-fixed` | UI, staking, wallets | 🟢 ACTIVE |
| **Backend / Ledger & Agents** | `quantum-resonance-clean` | Truth, state, automation | 🟢 ACTIVE |
| **Smart Contracts / NFTs** | `pi-mr-nft-contracts` | On-chain law | 🟢 ACTIVE |
| **Minting Logic** | `pi-mr-nft-agent` | Contract executor | 🟢 ACTIVE |

**Non-Canonical Repositories:**
- `pi-forge-quantum-genesis` → 🟠 ARCHIVED (legacy coordination hub)
- All others → Supportive, experimental, or archived

---

## 🔄 SYSTEM FLOW (THE CANONICAL PATH)

```text
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            quantum-pi-forge-fixed (Next.js/TS)              │
│                  Frontend Interface                         │
│  • User authentication                                      │
│  • Wallet connections                                       │
│  • Staking interface                                        │
│  • Model royalty displays                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                 REST API / Signed Calls
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         quantum-resonance-clean (FastAPI/Python)            │
│                Backend Truth Layer                          │
│  • Agent orchestration                                      │
│  • Ledger state management                                  │
│  • Blockchain interaction coordination                      │
│  • Coherence monitoring                                     │
│                                                             │
│  ⚠️ CRITICAL RULE: AI agents NEVER touch frontend          │
│     They operate ONLY inside quantum-resonance-clean        │
└────────────────────────┬────────────────────────────────────┘
                         │
                Web3 Calls (Ethers/Web3.py)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    BLOCKCHAIN LAYER                         │
│                     (Polygon)                               │
│  • pi-mr-nft-contracts (Smart Contracts)                    │
│  • pi-mr-nft-agent (Minting Execution)                      │
│  • OINIO Token (ERC-20)                                     │
│  • Model Royalty NFTs (ERC-721)                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 ARCHITECTURAL RULES (NON-NEGOTIABLE)

### Rule 1: Single Source of Truth
Each layer has ONE canonical repository. No duplicates. No forks defining behavior.

### Rule 2: Agent Containment
AI agents operate ONLY in `quantum-resonance-clean`. They NEVER modify frontend code.

### Rule 3: Clear Boundaries
- Frontend calls backend via REST API
- Backend calls blockchain via Web3
- Blockchain emits events back to backend
- No layer-skipping allowed

### Rule 4: No Nested Repos
Canonical repos must NOT contain nested copies of other canonical repos.

### Rule 5: Archive, Don't Delete
Old repos are archived for historical reference, not deleted.

---

## 🗄️ ARCHIVED REPOSITORIES

These repositories are no longer authoritative and should be archived:

| Repo | Reason | Archive Date |
|------|--------|--------------|
| `pi-forge-quantum-genesis` | Legacy coordination hub, superseded | Jan 13, 2026 |
| `pi-forge-quantum-genesis-OPEN` | Duplicate/fork | Jan 13, 2026 |
| `PiForgeSovereign-GoldStandard` | Early experimental version | Jan 13, 2026 |
| `Oinio-server-*` | Superseded by quantum-resonance-clean | Jan 13, 2026 |
| `Piforge` | Original prototype | Jan 13, 2026 |
| `mainnetstatus` | Standalone utility | Jan 13, 2026 |
| `countdown` | Solstice event complete | Jan 13, 2026 |

---

## 📋 IMPLEMENTATION STATUS

### Phase A: Canonical Spine Declaration
- [x] Define 4 canonical repositories
- [x] Document system flow
- [x] Establish architectural rules
- [ ] Add README banners to canonical repos
- [ ] Add README banner to this repo (archive notice)

### Phase B: Surgical Cleanup
- [ ] Archive 7 legacy repos on GitHub
- [ ] Remove nested conflicts in canonical repos
- [ ] Move deprecated docs to archive folder

### Phase C: Lock the Spine (Quality Gates)
- [ ] Define CI/CD pipelines for canonical repos
- [ ] Establish branch protection rules
- [ ] Set up automated testing gates

---

## 🔐 MAINTENANCE

This document should be updated when:
- A canonical repository is replaced or renamed
- New architectural rules are established
- Repository archival status changes

**Update Frequency:** As needed, minimum quarterly review  
**Owner:** GitHub Agent / System Steward  
**Authority:** Requires consensus of core contributors

---

## 📚 RELATED DOCUMENTS

- [PHASE_A_README_BANNERS.md](PHASE_A_README_BANNERS.md) — Copy/paste banners for all repos
- [PHASE_B_CLEANUP_CHECKLIST.md](PHASE_B_CLEANUP_CHECKLIST.md) — Archival and cleanup steps
- [GENESIS.md](GENESIS.md) — Historical foundation document
- [README.md](README.md) — This repository's overview

---

**Cognitive Load Reduction Target:** 40%  
**Clarity Increase Target:** 90%  
**Status:** 🟢 PHASE A COMPLETE — SPINE LOCKED

