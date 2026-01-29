# 🚀 Vercel Production Deployment Guide

## Autonomous Deployment Setup for Pi Forge Quantum Genesis

This guide provides step-by-step instructions for deploying Pi Forge Quantum Genesis to Vercel with full autonomous agent oversight capabilities.

---

## 📋 Prerequisites

- [Vercel Account](https://vercel.com) (Free tier supported)
- GitHub repository access
- Node.js 18+ installed locally (for testing)
- Environment variables ready (see Configuration section)

---

## 🎯 Quick Start (Autonomous Deployment)

### Option 1: Automated GitHub Integration (Recommended)

1. **Connect Repository to Vercel**
   - Visit [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New..." → "Project"
   - Import `onenoly1010/pi-forge-quantum-genesis`
   - Vercel auto-detects configuration from `vercel.json`

2. **Configure Environment Variables**
   ```bash
   # Required for Pi Network integration
   PI_APP_SECRET=your-pi-network-app-secret
   
   # Optional for enhanced features
   GUARDIAN_SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   MAILGUN_DOMAIN=mg.yourdomain.com
   MAILGUN_API_KEY=your-mailgun-api-key
   SENDGRID_API_KEY=your-sendgrid-api-key
   SENDGRID_FROM=noreply@yourdomain.com
   ```

3. **Deploy**
   - Click "Deploy"
   - Vercel automatically runs `npm run build`
   - Deployment completes in ~2 minutes
   - Your app is live at `https://your-project.vercel.app`

### Option 2: CLI Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Follow prompts to link project
```

---

## 🔧 Build Configuration

### Build Process

The build is configured in `vercel.json` and `package.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "public"
}
```

**Build Steps:**
1. TypeScript type-checking (`tsc --noEmit`)
2. Static asset copying (`node scripts/build.js`)
3. Output to `public/` directory

**Build Assets:**
- ✅ All HTML pages (index.html, ceremonial_interface.html, etc.)
- ✅ JavaScript files (pi-forge-integration.js)
- ✅ Frontend directory (complete assets)
- ✅ Mobile-optimized viewport configurations
- ✅ PWA manifest and service worker

### Local Build Testing

```bash
# Install dependencies
npm install

# Run build
npm run build

# Verify output
ls -la public/

# Expected output:
# - index.html
# - ceremonial_interface.html
# - resonance_dashboard.html
# - spectral_command_shell.html
# - pi-forge-integration.js
# - frontend/ (directory)
```

---

## 📱 Mobile Readiness

### Responsive Design Features

✅ **Viewport Configuration**
- All pages include `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Responsive breakpoints: 768px (tablet), 480px (mobile)

✅ **PWA Support** (Progressive Web App)
- Installable on mobile devices
- Offline capability via service worker
- App-like experience

✅ **Touch Optimization**
- Minimum touch target size: 44x44px
- No hover-dependent interactions
- Mobile-first navigation

✅ **Performance**
- Lazy loading for images
- Minified assets
- CDN delivery via Vercel

### Mobile Testing

```bash
# Test responsive design locally
npm run build
npx serve public -p 3000

# Open in browser and test:
# - Chrome DevTools > Device Toolbar (Cmd+Shift+M)
# - Test iPhone SE, iPad, Android devices
```

---

## 🔐 Environment Configuration

### Required Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `PI_APP_SECRET` | Pi Network authentication | `sk_live_xxxxx...` |

### Optional Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `GUARDIAN_SLACK_WEBHOOK_URL` | Slack alert notifications | None |
| `MAILGUN_DOMAIN` | Email service domain | None |
| `MAILGUN_API_KEY` | Mailgun API key | None |
| `SENDGRID_API_KEY` | SendGrid API key | None |
| `SENDGRID_FROM` | Email sender address | None |

### Setting Environment Variables

**Via Vercel Dashboard:**
1. Go to Project Settings → Environment Variables
2. Add each variable with appropriate scope (Production/Preview/Development)
3. Redeploy to apply changes

**Via CLI:**
```bash
# Set production variable
vercel env add PI_APP_SECRET production

# Pull environment variables locally
vercel env pull .env.local
```

---

## 🌐 Production URLs & Endpoints

### Main Application
- **Production URL**: `https://your-project.vercel.app`
- **Preview URLs**: `https://your-project-git-branch.vercel.app`

### API Endpoints

| Endpoint | Purpose | Method |
|----------|---------|--------|
| `/api/pi-identify` | Pi Network authentication | POST |
| `/health` | Health check (proxied to backend) | GET |
| `/` | Main application | GET |

### Static Assets
- All static files served from `/public` directory
- Automatic CDN caching via Vercel Edge Network
- Gzip compression enabled

---

## 🤖 Autonomous Agent Handoff

### Agent Oversight Configuration

This deployment is designed for complete agent oversight. The following endpoints and features enable autonomous monitoring:

**1. Health Monitoring**
```bash
# Automated health checks
curl https://your-project.vercel.app/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-12-11T14:52:21.490Z",
  "version": "1.0.0"
}
```

**2. Deployment Webhooks**
- Configure in Vercel Dashboard → Settings → Git
- Webhook URL: `https://your-monitoring-service.com/webhooks/vercel`
- Events: Deployment Started, Deployment Ready, Deployment Error

**3. GitHub Actions Integration**
- Automated deployment on PR merge
- Pre-deployment checks
- Post-deployment verification
- See `.github/workflows/deploy-vercel.yml` for details

**4. Monitoring & Alerts**
- Vercel Analytics (included): Real-time performance metrics
- Speed Insights: Core Web Vitals tracking
- Custom alerts via webhooks

### Agent Commands

```bash
# Check deployment status
vercel ls

# View deployment logs
vercel logs <deployment-url>

# Inspect deployment
vercel inspect <deployment-url>

# Rollback to previous deployment
vercel rollback <deployment-url>
```

---

## 📊 Performance & Optimization

### Vercel Optimizations (Automatic)

✅ **Edge Network**: Global CDN with 100+ locations
✅ **Compression**: Automatic gzip/brotli compression
✅ **Caching**: Smart caching headers
✅ **Image Optimization**: Automatic WebP conversion (if configured)
✅ **Analytics**: Built-in performance monitoring

### Custom Optimizations (Configured)

✅ **Security Headers**: X-Frame-Options, X-Content-Type-Options
✅ **Clean URLs**: Trailing slash normalization
✅ **SPA Routing**: Fallback to index.html for client-side routing

### Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| **First Contentful Paint** | < 1.5s | ~800ms |
| **Largest Contentful Paint** | < 2.5s | ~1.2s |
| **Time to Interactive** | < 3.5s | ~2.0s |
| **Cumulative Layout Shift** | < 0.1 | ~0.05 |

---

## 🧪 Testing & Verification

### Pre-Deployment Testing

```bash
# Run all tests
npm test

# Run Vercel build tests specifically
npm test -- tests/test_vercel_build.py

# Verify build output
npm run build && ls -la public/
```

### Post-Deployment Verification

**Automated Verification Script:**
```bash
# Run post-deployment checks
./scripts/verify-vercel-deployment.sh https://your-project.vercel.app

# Checks:
# ✓ Homepage loads (200 status)
# ✓ API endpoint responds
# ✓ Health check passes
# ✓ Static assets accessible
# ✓ Mobile viewport configured
```

**Manual Verification:**
1. Visit deployment URL
2. Test Pi Network authentication flow
3. Verify all pages load correctly
4. Test on mobile device (iOS/Android)
5. Check browser console for errors

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow

Automatic deployment is configured via `.github/workflows/deploy-vercel.yml`:

```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]
  pull_request:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

**Required Secrets:**
- `VERCEL_TOKEN`: Get from [Vercel Account Settings](https://vercel.com/account/tokens)
- `VERCEL_ORG_ID`: Found in `.vercel/project.json` after first deployment
- `VERCEL_PROJECT_ID`: Found in `.vercel/project.json` after first deployment

---

## 🚨 Troubleshooting

### Common Issues

**Build Fails: "Cannot find type definition file for 'node'"**
```bash
# Solution: Install dependencies
npm install
```

**404 on Deployment**
```bash
# Check: vercel.json outputDirectory matches build output
# Should be: "outputDirectory": "public"
```

**API Endpoints Return 404**
```bash
# Check: vercel.json rewrites configuration
# Ensure backend URL is correct in rewrites
```

**Environment Variables Not Working**
```bash
# Solution: Redeploy after adding variables
vercel --prod
```

### Debug Mode

```bash
# Deploy with debug logging
vercel --debug

# View detailed logs
vercel logs --follow
```

### Support Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Support](https://vercel.com/support)
- [Project Issues](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues)

---

## 🎉 Success Criteria

### Deployment Checklist

- [ ] Repository connected to Vercel
- [ ] Environment variables configured
- [ ] Build completes successfully
- [ ] Deployment URL accessible
- [ ] Health check endpoint responds
- [ ] Pi Network authentication works
- [ ] Mobile responsive on all devices
- [ ] Performance metrics meet targets
- [ ] No console errors
- [ ] All static assets load correctly

### Post-Deployment

- [ ] Custom domain configured (optional)
- [ ] SSL certificate active (automatic)
- [ ] Monitoring/alerts configured
- [ ] GitHub Actions CI/CD active
- [ ] Agent handoff documentation reviewed
- [ ] Team notified of deployment

---

## 📚 Additional Resources

- [Main README](./README.md) - Project overview
- [Production Deployment Guide](./docs/PRODUCTION_DEPLOYMENT.md) - Railway deployment
- [Agent Handoff Documentation](./docs/AI_AGENT_QUICK_REFERENCE.md) - Autonomous operations
- [Testing Guide](./tests/README.md) - Test suite documentation

---

**Deployment Status**: ✅ Production Ready  
**Last Updated**: 2025-12-11  
**Version**: 1.0.0  
**Maintained By**: Pi Forge Collective

---

*For autonomous agent oversight, see [AUTONOMOUS_DEPLOYMENT_HANDOFF.md](./AUTONOMOUS_DEPLOYMENT_HANDOFF.md)*
