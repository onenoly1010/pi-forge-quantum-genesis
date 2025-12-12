# 🚀 Quick Deployment Reference Card

**Pi Forge Quantum Genesis - Vercel Deployment**

---

## One-Line Deploy

```bash
# Automated setup and deploy
./scripts/vercel-setup.sh && vercel --prod
```

---

## Essential Commands

| Task | Command |
|------|---------|
| **Install Vercel CLI** | `npm install -g vercel` |
| **Login** | `vercel login` |
| **Link Project** | `vercel link` |
| **Deploy Preview** | `vercel` |
| **Deploy Production** | `vercel --prod` |
| **View Deployments** | `vercel ls` |
| **View Logs** | `vercel logs <url>` |
| **Rollback** | `vercel rollback <url>` |
| **Add Env Var** | `vercel env add <name> production` |

---

## Pre-Deployment Checklist

- [ ] Node.js 18+ installed
- [ ] Environment variables ready
- [ ] Build tested locally (`npm run build`)
- [ ] Tests passing (`npm test`)
- [ ] Git repository up to date

---

## Required Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `PI_APP_SECRET` | Pi Network authentication | ✅ Yes |
| `GUARDIAN_SLACK_WEBHOOK_URL` | Slack alerts | ❌ No |
| `SENDGRID_API_KEY` | Email notifications | ❌ No |

**Set via:**
- Vercel Dashboard: Settings → Environment Variables
- CLI: `vercel env add <name> production`

---

## Build Process

```bash
npm install        # Install dependencies
npm run typecheck  # TypeScript check
npm run build      # Build static assets
```

**Output:** `public/` directory (deployed to Vercel)

---

## Post-Deployment Verification

```bash
# Automated verification
./scripts/verify-vercel-deployment.sh https://your-project.vercel.app

# Manual checks
curl https://your-project.vercel.app
curl https://your-project.vercel.app/health
```

---

## GitHub Actions (CI/CD)

**Required Secrets:**
- `VERCEL_TOKEN` - From [Vercel Account Tokens](https://vercel.com/account/tokens)
- `VERCEL_ORG_ID` - Found in `.vercel/project.json`
- `VERCEL_PROJECT_ID` - Found in `.vercel/project.json`

**Setup:**
1. Deploy once manually to generate `.vercel/project.json`
2. Copy `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID`
3. Add secrets to GitHub: Settings → Secrets → Actions
4. Push to main branch to trigger auto-deploy

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Run `npm install && npm run build` locally |
| 404 on deploy | Check `vercel.json` output directory |
| Env vars not working | Redeploy after adding variables |
| TypeScript errors | Run `npm run typecheck` to debug |

---

## Quick Links

- **Documentation**: [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md)
- **Agent Handoff**: [AUTONOMOUS_DEPLOYMENT_HANDOFF.md](./AUTONOMOUS_DEPLOYMENT_HANDOFF.md)
- **Vercel Docs**: https://vercel.com/docs
- **GitHub Actions**: `.github/workflows/deploy-vercel.yml`

---

## Support

- **Issues**: https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
- **Vercel Support**: https://vercel.com/support
- **Documentation**: See `docs/` directory

---

**Last Updated**: 2025-12-11  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
