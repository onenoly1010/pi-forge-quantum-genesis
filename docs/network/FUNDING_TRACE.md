# Funding Trace

## Scope and Method
This record captures funding-related claims and signals found in local repository materials only.  
It distinguishes between:
- claimed status in documentation,
- evidence currently available in-repo,
- evidence missing for institutional verification.

No external assumptions are included.

## Verification Scale
- **Confirmed:** Direct evidence artifact present locally (transaction artifact, signed record, or verifiable receipt in repository).
- **Claimed:** Statement exists in documentation, but no direct evidentiary artifact was found in this phase.
- **Unknown:** Mention exists but status cannot be classified from available local artifacts.

---

## Entry 1 — Pi Network Catalyst/Treasury Narrative

- **Source/Platform:** `docs/CATALYST_POOL_ECONOMICS.md`
- **Claimed Status:** A treasury model and funding flow are described (including percentage allocations and sustainability framing).
- **Evidence Available:** Narrative and formula-level documentation exist in markdown.
- **Missing Evidence:** No direct treasury transaction ledger, on-chain proof bundle, signed wallet attestations, or disbursement receipts identified in this phase.
- **Next Verification Action:** Correlate claimed treasury addresses and percentages with exported chain data and attach immutable evidence files under `docs/audit/` or `public/metrics/`.
- **Disbursement Confirmed:** **No (not confirmed from local evidence in this phase).**

## Entry 2 — Wallet Funding Prerequisites for Deployments

- **Source/Platform:** Contract deployment guides (including `contracts/DEPLOYMENT_GUIDE.md`, `contracts/DEPLOYMENT_EXAMPLES.md`, `contracts/DEPLOYMENT_CHECKLIST.md`, `contracts/0g-uniswap-v2/README.md`, `docs/0G_DEX_QUICKSTART.md`)
- **Claimed Status:** Documents state deployer wallets must be funded and reference faucet/top-up requirements.
- **Evidence Available:** Operational prerequisites and command guidance are documented.
- **Missing Evidence:** No locally stored wallet balance snapshots, transaction IDs, or signed proof of actual wallet funding events tied to a release.
- **Next Verification Action:** Produce release-bound wallet funding evidence pack with address, network, block height, tx hash, and timestamp.
- **Disbursement Confirmed:** **No (funding requirement documented; disbursement not evidenced).**

## Entry 3 — Faucet References

- **Source/Platform:** `SKILL.md`, `contracts/QUICK_REFERENCE.md`, `docs/DEMO_DASHBOARD.md`, `docs/0G_DEX_QUICKSTART.md`
- **Claimed Status:** Testnet faucet usage is referenced for obtaining deploy/test funds.
- **Evidence Available:** Faucet URLs and instructions are present.
- **Missing Evidence:** No faucet claim receipts, transaction hashes, or account funding confirmations stored locally.
- **Next Verification Action:** For each faucet-based setup, archive claim timestamp, recipient address, tx hash, and explorer link in a deterministic evidence file.
- **Disbursement Confirmed:** **No (reference only).**

## Entry 4 — Funding/Approval Signals in Guardian Workflow

- **Source/Platform:** `GUARDIAN_APPROVAL_SUMMARY.md`, `GUARDIAN_APPROVAL_QUICKSTART.md`, `docs/GUARDIAN_DECISION_WORKFLOW.md`
- **Claimed Status:** Approval workflow and a specific deployment approval record are documented.
- **Evidence Available:** Approval workflow documentation and example approval identifiers appear in markdown.
- **Missing Evidence:** No immutable, signed financial disbursement receipts connected to approvals were identified in this phase.
- **Next Verification Action:** Separate operational approvals from financial disbursement evidence; bind any funding decision to transaction-level proof artifacts.
- **Disbursement Confirmed:** **No (approval evidence is not disbursement evidence).**

## Entry 5 — Grant/Funding Readiness Indicators

- **Source/Platform:** `ROADMAP.md` (Funding Readiness Goals), additional governance and deployment docs referencing funding conditions.
- **Claimed Status:** Project indicates readiness objectives for funding and treasury verification.
- **Evidence Available:** Explicit readiness goals and verification intent are documented.
- **Missing Evidence:** No complete grant dossier bundle (submission copy, reviewer acknowledgment, award letter, milestone acceptance, payment confirmation artifacts) identified locally in this phase.
- **Next Verification Action:** Build a grant evidence register with immutable artifact IDs and statuses (submitted, reviewed, approved, paid, reconciled).
- **Disbursement Confirmed:** **No (readiness intent only).**

---

## Consolidated Verification State

| Category | Current State |
|---|---|
| Funding claims present in docs | Yes |
| Direct disbursement proof artifacts located | No |
| Wallet submission evidence bundle located | No |
| Grant award confirmation artifact located | No |
| Milestone payment confirmation artifact located | No |

## Immediate Controls for Phase 2
1. Create an evidence manifest under `docs/audit/` with deterministic file naming and hash tracking.
2. Separate policy/intent documents from evidentiary documents.
3. Require transaction-level proof for any statement implying funding receipt or disbursement.
4. Publish machine-readable funding verification status to `public/metrics/` once evidence exists.