# 0GSKILLS

![0GSKILLS wordmark — 0 (zero), G, S, K, I, L, L, S](banner-0gskills.svg)

**0** (zero) · **G** · **S** · **K** · **I** · **L** · **L** · **S**

Plain-text wordmark URL (agents / no renderer): `https://0gskills.com/banner-0gskills.svg`

**The missing layer between AI agents and 0G apps** — modular guides for **0G Chain** (EVM execution, decentralized storage, AI compute).

**Canonical index:** when this repo is hosted at `https://0gskills.com`, each skill topic lives under `https://0gskills.com/<topic>/`.

**SEO:** [`/robots.txt`](https://0gskills.com/robots.txt) · [`/sitemap.xml`](https://0gskills.com/sitemap.xml)

### Use with AI agents

```text
Read https://0gskills.com/ship/ before coding on 0G.
```

### How to fetch (agents & humans)
```bash
curl -sSL https://0gskills.com/SKILL.md
curl -sSL https://0gskills.com/ship/
```

### Agent API (structured JSON on the same host)
Vercel Edge routes — no auth, CORS `*`. Same markdown as above, parsed for tools.

```bash
curl -sS "https://0gskills.com/api/skill?topic=ship"
curl -sS "https://0gskills.com/api/search?q=security"
```

- **`topic`:** skill id (`ship`, `gas`, …) or `index` for this file.
- **`format`:** `json` (default) or `markdown` for raw body.
- **`depth`:** `2` to include `related` summaries for linked topic paths (capped).

### Skills (fetch any URL)
This file is an index summary for the 0GSKILLS host. Individual skill guides are published externally at `https://0gskills.com/<topic>/` and are not stored in this repository.

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