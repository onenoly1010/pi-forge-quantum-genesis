# Repository Cleanup Action Plan

**Repository**: onenoly1010/pi-forge-quantum-genesis  
**Date Created**: 2026-02-08  
**Status**: Ready for Execution  
**Priority**: Medium

---

## Executive Summary

This action plan provides a step-by-step process to safely clean up the pi-forge-quantum-genesis repository, which currently has 129 branches (128 feature branches + main). The repository has existing automation that can be leveraged, and no critical dependencies will be affected by the cleanup.

### Quick Stats

| Metric | Current State | Target State | Timeline |
|--------|---------------|--------------|----------|
| Total Branches | 129 | <20 | 30 days |
| Protected Branches | 129 (all) | 1-5 | Week 1 |
| Releases | 0 | v1.0.0+ | Week 2 |
| Stale PRs | TBD | 0 | Ongoing |
| Automation Status | Active ✅ | Optimized ✅ | Week 3 |

---

## Phase 1: Preparation (Week 1)

### Day 1-2: Documentation Review

**Objective**: Ensure all stakeholders understand the cleanup process

**Tasks**:
- [x] Create comprehensive documentation
  - [x] BRANCH_CLEANUP_ANALYSIS.md
  - [x] REPOSITORY_CLEANUP_SAFEGUARDS.md
  - [x] REPOSITORY_MAINTENANCE_BEST_PRACTICES.md
- [ ] Review documentation with team
- [ ] Get approval from repository maintainers
- [ ] Set up communication channel for cleanup activities

**Deliverables**:
- ✅ Documentation in `docs/` directory
- [ ] Team approval recorded
- [ ] Communication plan established

### Day 3: Baseline Metrics

**Objective**: Establish current state for comparison

**Tasks**:
```bash
# 1. Export branch list
git for-each-ref --sort=-committerdate refs/remotes/origin \
  --format='%(refname:short)|%(committerdate:iso8601)|%(authorname)|%(subject)' \
  > baseline/branches-$(date +%Y%m%d).txt

# 2. Export PR list
gh pr list --state all --json number,title,state,createdAt,closedAt,headRefName \
  > baseline/prs-$(date +%Y%m%d).json

# 3. Export workflow status
gh run list --limit 100 --json name,status,conclusion \
  > baseline/workflows-$(date +%Y%m%d).json

# 4. Document current protection rules
gh api repos/onenoly1010/pi-forge-quantum-genesis/branches \
  --jq '.[] | select(.protected == true) | .name' \
  > baseline/protected-branches-$(date +%Y%m%d).txt
```

**Deliverables**:
- [ ] Baseline metrics exported to `baseline/` directory
- [ ] Metrics dashboard updated
- [ ] Team notified of baseline

### Day 4-5: Branch Protection Review

**Objective**: Adjust branch protection rules to allow cleanup

**Current State**:
- All 129 branches are protected ⚠️
- This prevents automated cleanup

**Required Changes**:

1. **Keep Protection** (Critical Branches):
   ```
   - main
   ```

2. **Remove Protection** (Feature Branches):
   ```
   - copilot/*
   - codespace/*
   - feature/*
   - fix/*
   - Any other temporary branches
   ```

**Tasks**:
- [ ] Document current protection rules
- [ ] Create proposal for new protection strategy
- [ ] Get admin approval
- [ ] Update branch protection rules via GitHub settings
- [ ] Verify changes

**Commands** (requires admin access):
```bash
# List protected branches
gh api repos/onenoly1010/pi-forge-quantum-genesis/branches \
  --jq '.[] | select(.protected == true) | .name'

# Note: Branch protection removal requires web UI or admin API access
# Navigate to: Settings > Branches > Branch protection rules
```

**Deliverables**:
- [ ] Protection rules documented
- [ ] Approval obtained
- [ ] Changes implemented
- [ ] Verification completed

### Day 6-7: Dry Run Testing

**Objective**: Test automated cleanup without making changes

**Tasks**:
```bash
# 1. Trigger branch cleanup workflow in dry-run mode
gh workflow run branch-cleanup.yml -f dry_run=true

# 2. Wait for completion (5-10 minutes)
sleep 600

# 3. Review results
gh run list --workflow=branch-cleanup.yml --limit 1

# 4. Download and review log
gh run view --log > dry-run-results-$(date +%Y%m%d).log

# 5. Analyze results
grep "Would delete:" dry-run-results-*.log | wc -l
grep "Skipping:" dry-run-results-*.log | wc -l
```

**Expected Results**:
- List of branches that would be deleted (likely 50-100)
- List of branches that would be skipped (with reasons)
- No actual deletions

**Verification**:
- [ ] Dry run completed successfully
- [ ] Results reviewed and approved
- [ ] No unexpected branches in deletion list
- [ ] Team notified of findings

**Deliverables**:
- [ ] Dry run results documented
- [ ] Branch list validated
- [ ] Approval to proceed

---

## Phase 2: Initial Cleanup (Week 2)

### Day 8: Execute First Cleanup

**Objective**: Delete branches >90 days old with merged PRs

**Pre-Flight Checklist**:
- [ ] Branch protection rules updated
- [ ] Dry run results approved
- [ ] Team notified of cleanup schedule
- [ ] Backup created
- [ ] All critical workflows passing

**Execution**:
```bash
# 1. Create backup before execution
git for-each-ref --format='%(refname:short)|%(objectname)' refs/remotes/origin \
  > backups/pre-cleanup-backup-$(date +%Y%m%d).txt

# 2. Execute cleanup
gh workflow run branch-cleanup.yml -f dry_run=false

# 3. Monitor execution
watch -n 30 'gh run list --workflow=branch-cleanup.yml --limit 1'

# 4. Wait for completion (10-20 minutes depending on branch count)

# 5. Review results
gh run view --log > cleanup-results-$(date +%Y%m%d).log
```

**Monitoring**:
- Watch workflow progress in real-time
- Check for any errors or warnings
- Verify expected branch counts

**Post-Execution Verification**:
```bash
# 1. Count remaining branches
git fetch --all --prune
git branch -r | grep -v HEAD | wc -l

# 2. Verify critical branches still exist
git branch -r | grep "main"

# 3. Check workflow status
gh run list --limit 10 --json name,conclusion

# 4. Test deployments
gh workflow run deploy-vercel.yml
gh workflow run test-and-build.yml
```

**Rollback Procedure** (if needed):
```bash
# If critical branch deleted accidentally:
# 1. Use GitHub UI to restore (Settings > Branches > Deleted)
# 2. Or use git reflog to find commit and recreate
git reflog --all | grep "branch-name"
git checkout -b branch-name <commit-sha>
git push origin branch-name
```

**Deliverables**:
- [ ] Cleanup executed successfully
- [ ] Results documented
- [ ] Verification completed
- [ ] Team notified of results

### Day 9-10: Release Management Setup

**Objective**: Create initial release and establish versioning

**Current State**:
- No releases exist
- No tags exist
- No formal versioning

**Tasks**:

1. **Determine Initial Version**
   ```
   Recommendation: v1.0.0
   Rationale: 
   - Repository is mature with production deployments
   - Active development and contributors
   - Stable feature set
   ```

2. **Create Release**
   ```bash
   # 1. Ensure main is clean and stable
   git checkout main
   git pull origin main
   
   # 2. Verify all tests pass
   # (Run test suite)
   
   # 3. Create tag
   git tag -a v1.0.0 -m "Initial stable release

   This release marks the baseline for the Pi Forge Quantum Genesis platform.
   
   ## Features
   - FastAPI backend (port 8000)
   - Flask visualization service (port 5000)
   - Gradio ethics interface (port 7860)
   - Supabase authentication integration
   - Pi Network payment integration
   - Quantum fractal generation
   - Sacred Trinity architecture
   - Comprehensive documentation
   
   ## Deployments
   - Railway: https://pi-forge-quantum-genesis.railway.app
   - Render: https://pi-forge-quantum-genesis-1.onrender.com
   - Vercel: Frontend deployment
   
   ## Documentation
   - See README.md for quick start
   - See docs/ for detailed guides
   - See wiki/ for architecture information"
   
   # 4. Push tag
   git push origin v1.0.0
   
   # 5. Create GitHub release
   gh release create v1.0.0 \
     --title "Pi Forge Quantum Genesis v1.0.0" \
     --notes-file RELEASE_NOTES.md \
     --latest
   ```

3. **Update Documentation**
   - Add version to README.md
   - Create CHANGELOG.md
   - Document release process

**Deliverables**:
- [ ] v1.0.0 release created
- [ ] Release notes published
- [ ] CHANGELOG.md created
- [ ] Documentation updated
- [ ] Team notified

### Day 11-14: Stale PR Cleanup

**Objective**: Address inactive pull requests

**Tasks**:

1. **Audit Open PRs**
   ```bash
   # List all open PRs with age
   gh pr list --state open --json number,title,createdAt,updatedAt \
     --jq '.[] | "\(.number)|\(.title)|\(.createdAt)|\(.updatedAt)"' \
     > open-prs-audit.txt
   ```

2. **Review Stale PR Workflow**
   - The `stale-pr-management.yml` workflow handles this automatically
   - Verify it's running daily at 2:00 AM UTC
   - Check recent runs for effectiveness

3. **Manual Review** (if needed)
   - Check PRs >30 days old
   - Contact authors for status
   - Close truly abandoned PRs with explanation

**Deliverables**:
- [ ] PR audit completed
- [ ] Stale PR workflow verified
- [ ] Manual interventions (if any) completed
- [ ] Documentation updated

---

## Phase 3: Optimization (Week 3)

### Day 15-17: Workflow Optimization

**Objective**: Ensure automation is efficient and effective

**Tasks**:

1. **Review Workflow Configuration**
   ```bash
   # Check branch-cleanup.yml settings
   - Schedule: Daily at 2:00 AM UTC ✅
   - Protected branches: main, master, develop, staging, production ✅
   - Age threshold: 90 days ✅
   - Dry run default: true ✅
   ```

2. **Add Enhancements**
   
   **Enhancement 1: Notification System**
   ```yaml
   # Add to branch-cleanup.yml
   - name: Create summary issue
     if: ${{ github.event.inputs.dry_run == 'false' }}
     uses: actions/github-script@v7
     with:
       script: |
         const fs = require('fs');
         const deleted = fs.readFileSync('/tmp/deleted_count.txt', 'utf8');
         const skipped = fs.readFileSync('/tmp/skipped_count.txt', 'utf8');
         
         await github.rest.issues.create({
           owner: context.repo.owner,
           repo: context.repo.repo,
           title: `🧹 Branch Cleanup Report - ${new Date().toISOString().split('T')[0]}`,
           body: `## Automated Branch Cleanup Summary
           
           **Branches Deleted**: ${deleted}
           **Branches Skipped**: ${skipped}
           
           See [workflow run](${context.payload.repository.html_url}/actions/runs/${context.runId}) for details.`,
           labels: ['maintenance', 'automated']
         });
   ```

   **Enhancement 2: Metrics Tracking**
   ```yaml
   # Add to branch-cleanup.yml
   - name: Update metrics
     run: |
       mkdir -p metrics
       echo "$(date +%Y-%m-%d),$DELETED_COUNT,$SKIPPED_COUNT" \
         >> metrics/cleanup-history.csv
   ```

3. **Test Enhanced Workflow**
   - Deploy changes to test branch
   - Run with dry-run=true
   - Verify enhancements work
   - Merge to main

**Deliverables**:
- [ ] Workflow enhancements implemented
- [ ] Testing completed
- [ ] Changes deployed
- [ ] Documentation updated

### Day 18-21: Documentation Finalization

**Objective**: Ensure all documentation is complete and accessible

**Tasks**:

1. **Update Repository Documentation**
   - [ ] README.md - Add cleanup info
   - [ ] CONTRIBUTING.md - Add branch guidelines
   - [ ] docs/index.md - Link to cleanup docs
   - [ ] wiki/ - Update as needed

2. **Create Quick Reference**
   ```bash
   # Create docs/CLEANUP_QUICK_REFERENCE.md
   ```
   - Common cleanup commands
   - Workflow triggers
   - Emergency procedures
   - Contact information

3. **Update Metrics Dashboard**
   - Add branch count metrics
   - Add cleanup frequency
   - Add success rates

**Deliverables**:
- [ ] All documentation updated
- [ ] Quick reference created
- [ ] Dashboard updated
- [ ] Links verified

---

## Phase 4: Monitoring (Ongoing)

### Daily Tasks

**Automated** (via workflows):
- Branch cleanup runs at 2:00 AM UTC
- Stale PR management runs at 2:00 AM UTC
- Deployment health dashboard updates every 6 hours

**Manual** (5 minutes):
```bash
# Quick health check
echo "Branch count: $(git branch -r | grep -v HEAD | wc -l)"
echo "Open PRs: $(gh pr list --state open --json number --jq 'length')"
echo "Recent workflow failures: $(gh run list --limit 20 --json conclusion | jq '[.[] | select(.conclusion == "failure")] | length')"
```

### Weekly Tasks (15 minutes)

1. **Review Cleanup Reports**
   ```bash
   # Check last 7 cleanup runs
   gh run list --workflow=branch-cleanup.yml --limit 7
   
   # Review any issues created by automation
   gh issue list --label maintenance --limit 10
   ```

2. **Branch Audit**
   ```bash
   # List branches by age
   git for-each-ref --sort=committerdate refs/remotes/origin \
     --format='%(committerdate:short)|%(refname:short)' \
     | head -20
   
   # Identify branches >60 days (approaching cleanup threshold)
   # Contact owners if needed
   ```

3. **PR Review**
   ```bash
   # Check for PRs approaching stale threshold
   gh pr list --state open --json number,title,updatedAt \
     --jq '.[] | select((.updatedAt | fromdateiso8601) < (now - 604800))'
   ```

### Monthly Tasks (1 hour)

1. **Metrics Analysis**
   ```bash
   # Analyze cleanup trends
   cat metrics/cleanup-history.csv | tail -30
   
   # Calculate averages
   awk -F',' '{deleted+=$2; skipped+=$3; count++} 
     END {print "Avg deleted:", deleted/count, "Avg skipped:", skipped/count}' \
     metrics/cleanup-history.csv
   ```

2. **Workflow Health Review**
   - Check success rates
   - Review any failures
   - Update configurations if needed

3. **Documentation Review**
   - Check for outdated information
   - Update metrics and examples
   - Add new learnings

4. **Team Feedback**
   - Gather feedback on cleanup process
   - Identify pain points
   - Propose improvements

### Quarterly Tasks (2-4 hours)

1. **Comprehensive Audit**
   - Review all branches
   - Check all protection rules
   - Verify all automations
   - Update documentation

2. **Process Improvement**
   - Analyze metrics trends
   - Identify optimization opportunities
   - Update workflows
   - Refine thresholds

3. **Team Retrospective**
   - Review cleanup effectiveness
   - Discuss challenges
   - Share successes
   - Plan improvements

---

## Success Criteria

### Immediate Success (Week 2)

- [ ] Branch count reduced from 129 to <30
- [ ] All branches >90 days deleted (except protected)
- [ ] First release (v1.0.0) created
- [ ] No broken workflows
- [ ] No broken deployments

### Short-term Success (Month 1)

- [ ] Branch count maintained at <20
- [ ] Average branch age <30 days
- [ ] Stale PRs <5
- [ ] Automated cleanup running smoothly
- [ ] Team comfortable with new processes

### Long-term Success (Month 3)

- [ ] Consistent branch count <20
- [ ] Regular releases (monthly or bi-weekly)
- [ ] No stale PRs
- [ ] Automation requires minimal intervention
- [ ] Team follows best practices naturally

---

## Risk Assessment

### Low Risk ✅

- Deleting merged branches >90 days old
- Creating initial releases
- Documentation updates
- Automation enhancements

**Mitigation**: Standard verification procedures

### Medium Risk ⚠️

- Removing branch protection from feature branches
- First execution of cleanup automation
- Workflow modifications

**Mitigation**: 
- Dry run testing
- Manual review before execution
- Staged rollout

### High Risk 🚨

- None identified - all changes are reversible

**Mitigation**: 
- Comprehensive documentation
- Team training
- Emergency procedures ready

---

## Rollback Plan

If anything goes wrong:

### Scenario 1: Wrong Branch Deleted

**Action**: Restore within 30 days via GitHub UI
```
1. Navigate to repository
2. Click "Branches" tab
3. Click "All branches" > "Deleted"
4. Click "Restore" next to the branch
```

### Scenario 2: Workflow Broken

**Action**: Disable workflow temporarily
```bash
# Rename workflow file to disable
mv .github/workflows/branch-cleanup.yml \
   .github/workflows/branch-cleanup.yml.disabled
   
# Fix issue, test, and re-enable
```

### Scenario 3: Too Many Branches Deleted

**Action**: Review and restore as needed
```bash
# Review backup file
cat backups/pre-cleanup-backup-*.txt

# Restore specific branches using commit SHAs
git checkout -b branch-name <commit-sha>
git push origin branch-name
```

---

## Communication Plan

### Before Cleanup (Days 1-7)

**Audience**: All contributors, maintainers  
**Channel**: GitHub issue, email, chat  
**Message**:
```
📢 Repository Cleanup Announcement

We're planning to clean up the repository to improve maintainability.

**Timeline**: Starting Day 8
**Impact**: Deletion of inactive branches (>90 days old)
**Your Action**: Review your open PRs and branches

**Details**: [Link to documentation]
**Questions**: Reply to this issue or contact @maintainers
```

### During Cleanup (Days 8-14)

**Audience**: Team members  
**Channel**: Real-time during execution  
**Message**: Progress updates via automation issues

### After Cleanup (Day 15+)

**Audience**: All stakeholders  
**Channel**: GitHub issue, email  
**Message**:
```
✅ Repository Cleanup Complete

**Results**:
- Branches deleted: X
- Branches remaining: Y
- First release: v1.0.0 created
- No disruptions to workflows

**Next Steps**: Follow new branch guidelines in CONTRIBUTING.md

**Questions**: Reply to this issue
```

---

## Appendix

### A. Quick Commands Reference

```bash
# Branch count
git branch -r | grep -v HEAD | wc -l

# Trigger cleanup (dry run)
gh workflow run branch-cleanup.yml -f dry_run=true

# Trigger cleanup (actual)
gh workflow run branch-cleanup.yml -f dry_run=false

# View last cleanup run
gh run list --workflow=branch-cleanup.yml --limit 1

# List branches by age
git for-each-ref --sort=committerdate refs/remotes/origin \
  --format='%(committerdate:short)|%(refname:short)'

# List open PRs
gh pr list --state open

# Create release
gh release create v1.0.0 --title "Release v1.0.0" --notes "Release notes"
```

### B. Contacts

**Repository Maintainers**: See CONTRIBUTORS.md  
**Emergency Contact**: [Define for your organization]  
**Support**: GitHub Issues

### C. Resources

- **Documentation**: docs/BRANCH_CLEANUP_ANALYSIS.md
- **Safeguards**: docs/REPOSITORY_CLEANUP_SAFEGUARDS.md
- **Best Practices**: docs/REPOSITORY_MAINTENANCE_BEST_PRACTICES.md
- **Workflows**: .github/workflows/

---

## Action Items Summary

**Week 1 - Preparation**:
- [ ] Review documentation with team
- [ ] Get approval
- [ ] Capture baseline metrics
- [ ] Update branch protection rules
- [ ] Run dry-run test
- [ ] Get final approval

**Week 2 - Initial Cleanup**:
- [ ] Execute first cleanup
- [ ] Verify results
- [ ] Create v1.0.0 release
- [ ] Address stale PRs
- [ ] Document results

**Week 3 - Optimization**:
- [ ] Enhance workflows
- [ ] Update documentation
- [ ] Train team
- [ ] Establish monitoring

**Ongoing - Maintenance**:
- [ ] Daily monitoring (automated)
- [ ] Weekly reviews
- [ ] Monthly analysis
- [ ] Quarterly audits

---

**Plan Version**: 1.0.0  
**Created**: 2026-02-08  
**Owner**: Repository Maintainers  
**Status**: Ready for Execution  
**Approval Required**: Yes

**Next Step**: Review this plan with team and get approval to proceed.
