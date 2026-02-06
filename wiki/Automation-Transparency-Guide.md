# 🔍 Automation Transparency Guide

## Understanding Automation in Quantum Pi Forge

The Quantum Pi Forge uses automation to **assist** human collaboration, not replace it. This guide explains all automated systems, how they work, and how to bypass them when needed.

**Core Principle:** *Automation enhances human work. Humans always have the final say.*

---

## 🏛️ Canon Alignment: Automation Principles

Per the [Canon of Autonomy](../wiki/Canon-of-Autonomy.md):

### Automation MUST Be:
1. **Visible** — You know when automation is active
2. **Optional** — You can bypass it when needed
3. **Explainable** — Logic is documented and understandable
4. **Reversible** — Humans can override automated decisions

### Automation MUST NOT:
- Hide its operation from contributors
- Block human participation
- Make irreversible decisions alone
- Create barriers to contribution

---

## 🤖 Automated Systems Overview

### 1. **Canon Auto-Merge System** 🔄

**What it does:**
- Automatically merges Pull Requests for Canon artifact documentation
- Runs a 6-gate validation pipeline
- Only merges if all gates pass

**When it runs:**
- PRs that modify files in `canon/` directory
- PRs with Canon-related labels

**How to bypass:**
1. Add `no-automerge` label to your PR
2. Request manual merge in PR comments
3. Any steward can merge manually, overriding automation

**Transparency:**
- Gate status visible in PR checks
- Each gate comments on PR with results
- Audit trail logged in `canon/INDEX.md`
- All automation code in `.github/workflows/`

**Documentation:** [AUTOMERGE_SETUP.md](../.github/AUTOMERGE_SETUP.md)

---

### 2. **Press Agent (Communications Bot)** 📢

**What it does:**
- Posts announcements to Discord, Twitter, Telegram
- Broadcasts releases, deployments, milestones
- Sends scheduled ecosystem updates

**When it runs:**
- GitHub releases are published
- Deployments complete successfully
- Manual triggers via GitHub Actions
- Scheduled weekly/monthly updates

**How to bypass:**
1. Add `skip-press-agent` label to releases
2. Disable workflows temporarily in repository settings
3. Manual announcements always override automated ones

**Human approval required for:**
- Major announcements (v1.0, etc.)
- Policy changes
- Security updates
- Governance decisions

**Transparency:**
- All broadcasts logged in repository
- Preview messages before sending
- Dry-run mode available for testing
- Opt-out available per channel

**Documentation:** [wiki/Press-Agent.md](../wiki/Press-Agent.md)

---

### 3. **GitHub Actions Workflows** ⚙️

**What they do:**
- Run tests on PRs
- Deploy to production on merge
- Update health dashboards
- Clean up stale branches

**When they run:**
- On push to specific branches
- On PR creation/update
- On scheduled cron jobs
- On manual workflow dispatch

**How to bypass:**
1. Skip CI with `[skip ci]` in commit message
2. Disable specific workflows in `.github/workflows/`
3. Use draft PRs to prevent automatic runs
4. Cancel running workflows manually

**Transparency:**
- All workflow files in `.github/workflows/`
- Run history visible in Actions tab
- Logs available for every run
- Status checks on PRs

---

### 4. **Dependabot** 🔐

**What it does:**
- Automatically creates PRs for dependency updates
- Scans for security vulnerabilities
- Keeps dependencies up-to-date

**When it runs:**
- Weekly dependency check
- When security vulnerabilities detected
- Manual dependency update requests

**How to bypass:**
1. Close Dependabot PRs without merging
2. Configure exclusions in `.github/dependabot.yml`
3. Disable Dependabot in repository settings
4. Manual dependency updates always possible

**Transparency:**
- PRs clearly labeled as Dependabot
- Changelog links in PR description
- Security advisories linked
- Configuration visible in repository

---

### 5. **Deployment Automation** 🚀

**What it does:**
- Automatically deploys to Railway/Vercel on merge to `main`
- Runs health checks post-deployment
- Updates deployment dashboards
- Rolls back on health check failure

**When it runs:**
- Merges to `main` branch
- Manual deployment triggers
- Rollback on failure detection

**How to bypass:**
1. Use feature branches for testing
2. Manual deployments via CLI always available
3. Hold deployments with `[skip deploy]` in commit
4. Emergency rollback via repository settings

**Transparency:**
- Deployment status in GitHub Actions
- Health dashboard auto-updated
- Deployment logs accessible
- Manual override always available

---

## 📋 Complete Automation Inventory

| System | Type | Auto-Level | Human Override | Docs |
|--------|------|-----------|----------------|------|
| Canon Auto-Merge | PR Management | HIGH | Label: `no-automerge` | [AUTOMERGE_SETUP.md](../.github/AUTOMERGE_SETUP.md) |
| Press Agent | Communications | MEDIUM | Label: `skip-press-agent` | [Press-Agent.md](../wiki/Press-Agent.md) |
| GitHub Actions | CI/CD | MEDIUM | `[skip ci]` in commit | [workflows/](../.github/workflows/) |
| Dependabot | Dependencies | LOW | Close PRs | [dependabot.yml](../.github/dependabot.yml) |
| Deployment | Infrastructure | MEDIUM | `[skip deploy]` in commit | [DEPLOYMENT.md](../DEPLOYMENT.md) |
| Health Monitoring | Observability | LOW | Disable workflows | [workflows/deployment-health-dashboard.yml](../.github/workflows/deployment-health-dashboard.yml) |

---

## 🚦 When Automation Runs: Visual Indicators

### PR with Canon Auto-Merge Active

```
✅ Canon Classification (Gate 1): Passed
⏳ ClosureSentinel (Gate 2): Waiting...
⏸️  Approval Check (Gate 3): Pending
⏸️  Conflict Detection (Gate 4): Pending
⏸️  Audit Logging (Gate 5): Pending
⏸️  Auto-Merge (Gate 6): Pending
```

**Human Action Available:**
- Comment: "skip auto-merge" → Disables automation
- Add label: `no-automerge` → Permanent bypass
- Manual merge button always visible

---

### PR with CI/CD Active

```
✅ Tests: Passed
✅ Linting: Passed
⏳ Build: Running...
⏸️  Deploy: Waiting for approval
```

**Human Action Available:**
- Cancel workflow run
- Skip CI with `[skip ci]` commit
- Manual deploy after review

---

## 🛑 Emergency: Disable All Automation

If automation is causing problems, disable it immediately:

### Quick Disable (Temporary)

1. **For a specific PR:**
   ```bash
   # Add label to PR
   gh pr edit <PR_NUMBER> --add-label "no-automerge,skip-ci,skip-deploy"
   ```

2. **For all PRs:**
   ```bash
   # Disable workflows temporarily
   # Settings → Actions → Disable Actions
   ```

### Complete Disable (Permanent)

1. Navigate to repository **Settings → Actions**
2. Select **Disable Actions**
3. Or delete/rename workflow files in `.github/workflows/`

### Re-enable

1. Settings → Actions → Enable Actions
2. Review and test with a small PR
3. Gradually re-enable systems

---

## 📖 Human-First Contribution Path

**You never NEED automation to contribute.**

### Without Automation

1. **Create a branch** locally
2. **Make changes** to code/docs
3. **Test locally** (no CI required)
4. **Push to GitHub** with `[skip ci]` in commit
5. **Create PR** with `no-automerge` label
6. **Request manual review** from community
7. **Merge manually** when consensus reached

### Automation as Enhancement (Optional)

1. **Create PR** normally
2. **Let automation run** tests/validation
3. **Review automated feedback**
4. **Override if needed** (automation is advisory)
5. **Merge** when YOU decide (not when bot decides)

---

## 🔔 Notification Settings

Control how much automation you see:

### GitHub Notifications

```
Settings → Notifications → Actions

Options:
- Notify only on workflow failure
- Notify on all workflow runs
- Disable workflow notifications
```

### Mute Automated Comments

```
.github/workflows/

Comment out or remove:
- `github.event.pull_request.comments.create`
- Notification steps in workflows
```

---

## 🎯 Best Practices

### For Contributors

✅ **Use automation when it helps** (tests, formatting, validation)
✅ **Bypass when it doesn't** (creative work, experimentation)
✅ **Ask questions** if automation blocks you
✅ **Report issues** with automation transparency

❌ **Don't assume automation is mandatory**
❌ **Don't let bots discourage contribution**
❌ **Don't accept automated decisions without review**

### For Maintainers

✅ **Keep automation optional** (always provide manual path)
✅ **Document clearly** (this guide, plus inline docs)
✅ **Listen to feedback** (if automation creates barriers, fix it)
✅ **Prioritize humans** (automation assists, doesn't replace)

❌ **Don't hide automation** (transparency required)
❌ **Don't make automation mandatory** (bypass always available)
❌ **Don't let automation block humans** (override always possible)

---

## 📚 Related Documentation

- [Canon of Autonomy](../wiki/Canon-of-Autonomy.md) — Automation principles
- [Human Contribution Guide](../wiki/Human-Contribution-Guide.md) — Contributing without automation
- [AUTOMERGE_SETUP.md](../.github/AUTOMERGE_SETUP.md) — Auto-merge system details
- [Press Agent](../wiki/Press-Agent.md) — Communications bot documentation

---

## ❓ FAQ

### Q: Is automation required to contribute?

**A:** No. You can contribute entirely through manual processes. See [Human Contribution Guide](../wiki/Human-Contribution-Guide.md).

### Q: Can I permanently disable automation for my PRs?

**A:** Yes. Add `no-automerge` and `skip-ci` labels to your PRs. All automation will be bypassed.

### Q: Who controls automation?

**A:** Humans do. Automation suggests, humans decide. Any maintainer can override any automated decision.

### Q: What if automation blocks my contribution?

**A:** Report it immediately as a Canon violation. Automation must never block human participation. We'll fix it or disable it.

### Q: Can automation make decisions without humans?

**A:** No. Per the Canon of Autonomy, humans always have final say. Automation can suggest, warn, or assist—never command.

---

## 🏛️ Canon Compliance

This automation system complies with the [Canon of Autonomy](../wiki/Canon-of-Autonomy.md):

✅ **Sovereignty** — No bot controls the project; humans lead
✅ **Transparency** — All automation documented and visible
✅ **Inclusivity** — Manual paths available for all actions
✅ **Non-Hierarchy** — Bots assist, humans decide
✅ **Safety** — Automation can be disabled at any time
✅ **Continuity** — Human override preserves workflow continuity

**If any automation violates these principles, it must be fixed or removed.**

---

*Automation serves humans. Humans do not serve automation.*

**🤖 Automation Transparent. Humans Empowered. Canon Aligned.** 🏛️
