# Vercel Decommission Note

Vercel project was linked as:

- Team/project: onenoly1010s-projects/pi-forge-quantum-genesis-zpvu
- Public URL: https://pi-forge-quantum-genesis-zpvu.vercel.app/
- Reason for decommission: account suspended / payment required; moving away from Vercel for cost control.

The app used:
- Static frontend files
- Vercel Node API routes under api/*.ts
- vercel.json routing

Before redeploying elsewhere, replace Vercel functions with either:
- Railway/Render backend routes
- GitHub Pages static-only frontend
- Cloudflare Pages + Workers
- Local-first deployment
