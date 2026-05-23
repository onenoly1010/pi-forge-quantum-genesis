# 0GSKILLS

![0GSKILLS wordmark — 0 (zero), G, S, K, I, L, L, S](banner-0gskills.svg)

**0** (zero) · **G** · **S** · **K** · **I** · **L** · **L** · **S**

Plain-text wordmark URL (agents / no renderer): `https://0gskills.com/banner-0gskills.svg`

**The missing layer between AI agents and 0G apps** — modular guides for **0G Chain** (EVM execution, decentralized storage, AI compute).

**Canonical index:** when this repo is hosted at `https://0gskills.com`, each skill lives at `https://0gskills.com/<topic>/SKILL.md`.

**SEO:** [`/robots.txt`](https://0gskills.com/robots.txt) · [`/sitemap.xml`](https://0gskills.com/sitemap.xml)

### Use with AI agents

```text
Read https://0gskills.com/ship/SKILL.md before coding on 0G.
```

### How to fetch (agents & humans)
```bash
curl -sSL https://0gskills.com/SKILL.md
curl -sSL https://0gskills.com/ship/SKILL.md
```

### Agent API (structured JSON on the same host)
Vercel Edge routes — no auth, CORS `*`. Same markdown as above, parsed for tools.

```bash
curl -sS "https://0gskills.com/api/skill?topic=ship"
curl -sS "https://0gskills.com/api/search?q=security"
```

- **`topic`:** skill id (`ship`, `gas`, …) or `index` for this file.
- **`format`:** `json` (default) or `markdown` for raw body.
- **`depth`:** `2` to include `related` summaries for linked `*/SKILL.md` paths (capped).

### Skills (fetch any URL)
| Topic                  | Description                                      | URL                          |
|------------------------|--------------------------------------------------|------------------------------|
| **Ship**               | End-to-end: idea → contracts → storage/compute → deploy on 0G. **Start here.** | [/ship/SKILL.md](ship/SKILL.md) |
| Why ZeroG              | Strengths, tradeoffs, and when 0G fits your product. | [/why-zerog/SKILL.md](why-zerog/SKILL.md) |
| Protocol               | Upgrades, restaking, roadmap hygiene.            | [/protocol/SKILL.md](protocol/SKILL.md) |
| Gas & Costs            | Fee models vs Ethereum/L2s.                      | [/gas/SKILL.md](gas/SKILL.md) |
| Wallets                | Keys, RPC, signing, operational security.        | [/wallets/SKILL.md](wallets/SKILL.md) |
| Layer 2s               | Bridges, DA, Ethereum relationship.              | [/l2s/SKILL.md](l2s/SKILL.md) |
| Standards              | Tokens, NFTs, identity on EVM.                   | [/standards/SKILL.md](standards/SKILL.md) |
| Tools                  | RPCs, SDKs, Foundry/Hardhat, verification.       | [/tools/SKILL.md](tools/SKILL.md) |
| Money Legos            | DeFi composability patterns on 0G.               | [/money-legos/SKILL.md](money-legos/SKILL.md) |
| Orchestration          | Agent workflows: plan → build → verify → ship.   | [/orchestration/SKILL.md](orchestration/SKILL.md) |
| Contract Addresses     | System contracts & precompiles — **always re-verify**. | [/contract-addresses/SKILL.md](contract-addresses/SKILL.md) |
| Concepts               | Mental models: execution + storage + compute.    | [/concepts/SKILL.md](concepts/SKILL.md) |
| Security               | Defensive Solidity & common vulnerabilities.     | [/security/SKILL.md](security/SKILL.md) |
| Testing                | Unit, fuzz, fork, invariant testing.             | [/testing/SKILL.md](testing/SKILL.md) |
| Indexing               | Events, subgraphs, analytics pipelines.          | [/indexing/SKILL.md](indexing/SKILL.md) |
| Frontend UX            | Mandatory dApp UX rules for 0G.                  | [/frontend-ux/SKILL.md](frontend-ux/SKILL.md) |
| Frontend Playbook      | Production pipeline: envs, CI, hosting.          | [/frontend-playbook/SKILL.md](frontend-playbook/SKILL.md) |
| QA                     | Pre-release checklist for reviewers.             | [/qa/SKILL.md](qa/SKILL.md) |
| Audit                  | Structured smart-contract audit prompts.         | [/audit/SKILL.md](audit/SKILL.md) |

### Official 0G Links
- [0G Documentation](https://docs.0g.ai/)
- [0G Discord (dev support)](https://discord.gg/0glabs)
- [0G Labs on X](https://x.com/0G_labs)
- [Chainscan (mainnet)](https://chainscan.0g.ai/)
- [Chainscan (Galileo testnet)](https://chainscan-galileo.0g.ai/)
- [Testnet faucet](https://faucet.0g.ai/)
- [0G Foundation GitHub](https://github.com/0gfoundation)

**MIT License** · Open source — PRs welcome from humans and agents.

**Always verify** chain IDs, RPCs, and contract addresses against [docs.0g.ai](https://docs.0g.ai/) before production use.