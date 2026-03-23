# Repository Maintenance Best Practices Guide

**Purpose**: Establish sustainable practices for keeping the repository clean and efficient  
**Scope**: Branch management, release management, workflow optimization  
**Version**: 1.0.0

---

## Table of Contents

1. [Introduction](#introduction)
2. [Branch Management](#branch-management)
3. [Release Management](#release-management)
4. [Pull Request Lifecycle](#pull-request-lifecycle)
5. [Workflow Maintenance](#workflow-maintenance)
6. [Documentation Practices](#documentation-practices)
7. [Team Collaboration](#team-collaboration)
8. [Metrics and KPIs](#metrics-and-kpis)

---

## Introduction

This guide provides best practices for maintaining a clean, efficient, and collaborative repository. Following these practices will help prevent the accumulation of stale branches, ensure smooth releases, and maintain workflow health.

### Core Principles

1. **Clean as You Go**: Don't let technical debt accumulate
2. **Automate with Oversight**: Use automation but maintain human oversight
3. **Document Everything**: Make decisions and processes visible
4. **Communicate Proactively**: Keep team informed of changes
5. **Iterate and Improve**: Regularly review and optimize practices

---

## Branch Management

### Branch Naming Conventions

Use clear, consistent branch naming patterns:

```
<type>/<short-description>
```

**Types**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/modifications
- `chore/` - Maintenance tasks
- `hotfix/` - Critical production fixes

**Examples**:
```
feature/add-quantum-payment-api
fix/resolve-auth-token-expiry
docs/update-deployment-guide
refactor/optimize-database-queries
test/add-integration-tests
chore/update-dependencies
hotfix/fix-critical-security-issue
```

### Branch Lifecycle

#### Phase 1: Creation (Day 0)

```bash
# Always branch from main
git checkout main
git pull origin main

# Create descriptive branch
git checkout -b feature/your-feature-name

# Push immediately to establish remote tracking
git push -u origin feature/your-feature-name

# Create PR early (draft if needed)
gh pr create --draft --title "WIP: Your feature" --body "Working on..."
```

**Benefits**:
- Visible to team immediately
- Prevents naming conflicts
- Enables early collaboration

#### Phase 2: Active Development (Days 1-14)

**Best Practices**:

1. **Commit Frequently**
   ```bash
   # Small, focused commits
   git add specific-files
   git commit -m "Add payment validation logic"
   git push
   ```

2. **Keep PR Updated**
   ```bash
   # Update PR description as you progress
   gh pr edit --body "$(cat <<EOF
   ## Progress
   - [x] API endpoint implementation
   - [x] Unit tests
   - [ ] Integration tests
   - [ ] Documentation
   EOF
   )"
   ```

3. **Stay Sync with Main**
   ```bash
   # Regularly rebase or merge main
   git checkout main
   git pull origin main
   git checkout feature/your-feature
   git rebase main  # or: git merge main
   git push --force-with-lease  # if rebased
   ```

4. **Request Reviews Early**
   ```bash
   # Mark PR as ready and request reviews
   gh pr ready
   gh pr edit --add-reviewer @teammate1,@teammate2
   ```

**Target**: Complete and merge within 14 days

#### Phase 3: Review and Merge (Days 14-21)

**Before Merging**:

- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Conflicts resolved
- [ ] CI/CD checks passing
- [ ] No stale label applied

**Merge Strategy**:

```bash
# Option 1: Squash and merge (preferred for clean history)
gh pr merge --squash --delete-branch

# Option 2: Merge commit (preserve detailed history)
gh pr merge --merge --delete-branch

# Option 3: Rebase and merge (linear history)
gh pr merge --rebase --delete-branch
```

**Always delete the branch after merging** (use `--delete-branch` flag)

#### Phase 4: Post-Merge Cleanup (Immediate)

```bash
# Automatic cleanup via GitHub
# Branch is deleted on merge if using --delete-branch

# Manual cleanup if needed
git push origin --delete feature/your-feature
git branch -d feature/your-feature
```

### Long-Lived Branches

Some branches may need to exist longer than 90 days. Handle these appropriately:

#### Scenario 1: Large Features

```bash
# Use feature branch with sub-branches
git checkout -b feature/major-redesign
git push -u origin feature/major-redesign

# Create sub-branches
git checkout -b feature/major-redesign/api-changes
git checkout -b feature/major-redesign/ui-updates

# Merge sub-branches to feature branch
# Then merge feature branch to main when complete
```

**Keep Active**:
- Update PR description monthly with status
- Add comments explaining timeline
- Make periodic commits (at least monthly)
- Request periodic reviews

#### Scenario 2: Release Branches

```bash
# Create release branch
git checkout -b release/v2.0.0
git push -u origin release/v2.0.0

# Apply hotfixes as needed
# Merge back to main when release is complete
```

**Protection**: Add to protected branch list to prevent auto-deletion

#### Scenario 3: Experimental Branches

```bash
# Clearly label as experimental
git checkout -b experimental/quantum-ai-integration
git push -u origin experimental/quantum-ai-integration

# Create issue to track experiment
gh issue create --title "Experiment: Quantum AI Integration" \
  --body "Branch: experimental/quantum-ai-integration
  Goal: Evaluate feasibility of AI integration
  Timeline: 3 months
  Status: Active"
```

### Branch Protection Rules

#### Recommended Protection for Main Branch

```yaml
Branch: main
Settings:
  - Require pull request before merging: ✅
  - Require approvals: 1
  - Dismiss stale pull request approvals: ✅
  - Require review from Code Owners: ✅ (if CODEOWNERS exists)
  - Require status checks to pass: ✅
    - test-and-build
    - ledger-api-ci
    - canon-validation
  - Require branches to be up to date: ✅
  - Require conversation resolution: ✅
  - Require signed commits: ⚠️ (optional, depends on team)
  - Include administrators: ⚠️ (recommended)
  - Allow force pushes: ❌
  - Allow deletions: ❌
```

#### No Protection for Feature Branches

```yaml
Branches: copilot/*, feature/*, fix/*, etc.
Settings:
  - No protection rules
  - Allow automatic cleanup
  - Enable deletion after merge
```

**Rationale**: Feature branches should be temporary and easily manageable

---

## Release Management

### Semantic Versioning

Follow semantic versioning (SemVer):

```
MAJOR.MINOR.PATCH

Example: 2.3.1
- MAJOR: Breaking changes (1.x → 2.x)
- MINOR: New features, backward compatible (2.3 → 2.4)
- PATCH: Bug fixes, backward compatible (2.3.1 → 2.3.2)
```

### Release Process

#### Option 1: Manual Releases (Recommended Initially)

```bash
# 1. Ensure main is stable
git checkout main
git pull origin main

# 2. Run tests
npm test  # or appropriate test command
pytest tests/

# 3. Update version numbers
# Update package.json, __version__, etc.

# 4. Create release commit
git add .
git commit -m "chore: bump version to v2.3.1"
git push origin main

# 5. Create tag
git tag -a v2.3.1 -m "Release v2.3.1

## Changes
- Fixed authentication token expiry issue
- Updated deployment documentation
- Improved error handling in payment API

## Breaking Changes
None

## Contributors
@user1, @user2
"

# 6. Push tag
git push origin v2.3.1

# 7. Create GitHub release
gh release create v2.3.1 \
  --title "Release v2.3.1" \
  --notes-file RELEASE_NOTES.md \
  --latest
```

#### Option 2: Automated Releases

The repository has a `release-on-merge.yml` workflow. Configure it to:

```yaml
# .github/workflows/release-on-merge.yml
name: Release on Merge
on:
  push:
    branches: [main]
    paths-ignore:
      - 'docs/**'
      - '**.md'
      - '.github/**'

jobs:
  release:
    if: contains(github.event.head_commit.message, '[release]')
    # ... release steps
```

**Usage**:
```bash
# Trigger release with commit message
git commit -m "[release] Fix critical authentication bug

Fixes #123

This is a patch release to fix authentication issues."
```

### Release Cadence

#### Recommended Schedule

**Patch Releases**: As needed for bug fixes
- Trigger: Critical bugs, security fixes
- Frequency: Ad-hoc
- Timeline: Same day or next business day

**Minor Releases**: Monthly or bi-weekly
- Trigger: New features, enhancements
- Frequency: Every 2-4 weeks
- Timeline: Planned release days (e.g., first Monday of month)

**Major Releases**: Quarterly or less frequent
- Trigger: Breaking changes, major features
- Frequency: Every 3-6 months
- Timeline: Planned with advance notice (30 days)

#### Release Checklist

Before creating a release:

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Breaking changes documented
- [ ] Migration guide prepared (if needed)
- [ ] Deployment verified in staging
- [ ] Team notified of upcoming release
- [ ] Release notes drafted

### Release Notes Template

```markdown
# Release v2.3.1

**Release Date**: 2026-02-08  
**Type**: Patch Release  

## 🎉 What's New

- Feature: Added quantum payment integration API
- Enhancement: Improved error messages in authentication flow

## 🐛 Bug Fixes

- Fixed token expiry issue causing logouts (#123)
- Resolved deployment configuration errors (#124)

## 🔧 Maintenance

- Updated dependencies to latest versions
- Improved test coverage to 85%

## ⚠️ Breaking Changes

None

## 📚 Documentation

- Updated deployment guide with new Railway configuration
- Added API reference for payment endpoints

## 🙏 Contributors

@user1, @user2, @user3

## 📦 Installation

\`\`\`bash
pip install pi-forge-quantum-genesis==2.3.1
\`\`\`

## 🔗 Links

- [Full Changelog](https://github.com/onenoly1010/pi-forge-quantum-genesis/compare/v2.3.0...v2.3.1)
- [Documentation](https://docs.example.com)
- [Issues](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues)
```

---

## Pull Request Lifecycle

### PR Creation Best Practices

#### 1. Early and Draft

```bash
# Create draft PR immediately
gh pr create --draft \
  --title "WIP: Add quantum payment feature" \
  --body "## Goal
Implement quantum payment processing API

## Progress
- [ ] API endpoint design
- [ ] Implementation
- [ ] Tests
- [ ] Documentation

## Questions
- Which payment provider should we use?
- Should this be behind a feature flag?"
```

#### 2. Use PR Templates

Create `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description
<!-- Describe what this PR does -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
<!-- How was this tested? -->

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests passing
- [ ] No console errors
- [ ] Reviewed own code

## Related Issues
Fixes #
Relates to #

## Screenshots (if applicable)

## Deployment Notes
<!-- Special deployment considerations -->
```

### PR Review Process

#### For Authors

1. **Self-Review First**
   - Review your own code before requesting reviews
   - Check for console logs, commented code, TODOs
   - Run linters and formatters
   - Ensure tests pass locally

2. **Request Appropriate Reviewers**
   ```bash
   # Request reviews from relevant team members
   gh pr edit --add-reviewer @backend-team --add-reviewer @security-team
   ```

3. **Respond Promptly**
   - Address feedback within 24-48 hours
   - Mark conversations as resolved when addressed
   - Thank reviewers for their time

4. **Keep PR Updated**
   - Update based on feedback
   - Keep rebasing with main
   - Update description if scope changes

#### For Reviewers

1. **Review Promptly**
   - Target: Review within 24 hours of request
   - Use "Request changes" sparingly
   - Approve when ready, even if minor nits remain

2. **Be Constructive**
   ```
   ❌ "This code is bad"
   ✅ "Consider extracting this into a helper function for better readability"
   
   ❌ "You don't understand X"
   ✅ "Here's a resource on X that might help: [link]"
   ```

3. **Distinguish Severity**
   - **🚨 Blocking**: Security issues, bugs, broken tests
   - **⚠️ Important**: Performance issues, incorrect logic
   - **💡 Suggestion**: Style improvements, alternative approaches
   - **❓ Question**: Seeking clarification

### Stale PR Prevention

The repository has automated stale PR management. To keep your PR active:

#### Days 1-7: Active Development
- Make regular commits
- Update PR description with progress
- Respond to comments

#### Days 7-14: Review Stage
- Request reviews
- Address feedback
- Keep CI green

#### Days 14-21: Final Push
- Resolve all conversations
- Get final approvals
- Prepare for merge

#### Days 21-30: Critical Period
- **Day 21**: If no activity, add comment explaining status
- **Day 28**: Final push to merge or close
- **Day 30**: Auto-close if still inactive

**To Avoid Auto-Close**:
```bash
# Any of these actions reset the inactivity timer:
- Push a commit
- Add a comment
- Request a review
- Update PR description
```

---

## Workflow Maintenance

### Regular Workflow Health Checks

#### Weekly Review

```bash
# Check recent workflow runs
gh run list --limit 50 --json status,conclusion,name \
  | jq -r '.[] | "\(.name)|\(.status)|\(.conclusion)"' \
  | sort | uniq -c

# Identify failing workflows
gh run list --limit 20 --json status,conclusion,name \
  | jq -r '.[] | select(.conclusion == "failure") | .name' \
  | sort | uniq -c
```

#### Monthly Audit

1. **Review Workflow Files**
   ```bash
   # Check for outdated actions
   grep -r "uses:" .github/workflows/ | grep -v "@v" | sort -u
   
   # Check for deprecated syntax
   yamllint .github/workflows/
   ```

2. **Update Actions Versions**
   ```yaml
   # Keep actions up to date
   - uses: actions/checkout@v4  # Update from v3
   - uses: actions/setup-python@v5  # Update from v4
   ```

3. **Remove Unused Workflows**
   ```bash
   # Move disabled workflows to archive
   mkdir -p .github/workflows/archive
   mv .github/workflows/*.disabled .github/workflows/archive/
   ```

### Workflow Optimization

#### Reduce Redundancy

```yaml
# Before: Multiple jobs doing similar things
jobs:
  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pytest
      - run: pytest
      
  lint-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install flake8
      - run: flake8

# After: Combined job with matrix
jobs:
  python-checks:
    strategy:
      matrix:
        task: [test, lint]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run ${{ matrix.task }}
        run: |
          if [ "${{ matrix.task }}" = "test" ]; then
            pip install pytest && pytest
          elif [ "${{ matrix.task }}" = "lint" ]; then
            pip install flake8 && flake8
          fi
```

#### Cache Dependencies

```yaml
# Add caching to speed up workflows
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Cache npm dependencies
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

---

## Documentation Practices

### Keep Documentation Current

#### Documentation Types

1. **README.md**: Project overview, quick start
2. **docs/**: Detailed guides, API references
3. **wiki/**: Conceptual documentation, architecture
4. **CONTRIBUTING.md**: Contribution guidelines
5. **CHANGELOG.md**: Version history

#### Update Triggers

Update documentation when:
- Adding new features → Update API docs
- Changing architecture → Update architecture diagrams
- Modifying workflows → Update CONTRIBUTING.md
- Releasing version → Update CHANGELOG.md
- Changing deployment → Update deployment guides

#### Documentation PR Requirements

```markdown
## Documentation Checklist

When your PR includes code changes, also update:

- [ ] API documentation (if API changes)
- [ ] README.md (if user-facing changes)
- [ ] Architecture docs (if structure changes)
- [ ] Deployment guides (if deployment changes)
- [ ] CHANGELOG.md (for all changes)
```

### Documentation Review

#### Monthly Review

- Check for broken links
- Update outdated information
- Remove deprecated content
- Add missing documentation

```bash
# Check for broken links
find docs wiki -name "*.md" -exec grep -H "http" {} \; \
  | cut -d: -f2 | sort -u > links.txt

# Test links (requires linkchecker or similar tool)
cat links.txt | while read url; do
  curl -s -o /dev/null -w "%{http_code} $url\n" "$url"
done | grep "^[45]"
```

---

## Team Collaboration

### Communication Channels

#### GitHub Issues
- Feature requests
- Bug reports
- Documentation improvements
- Architecture discussions

#### Pull Requests
- Code reviews
- Implementation discussions
- Quick questions

#### Team Meetings
- Major decisions
- Architecture changes
- Release planning
- Retrospectives

### Decision Making

#### Async-First Approach

1. **Propose in Issue**
   ```markdown
   ## Proposal: Add GraphQL API
   
   **Context**: REST API is becoming complex
   
   **Proposal**: Implement GraphQL alongside REST
   
   **Benefits**:
   - Flexible queries
   - Reduced over-fetching
   - Better developer experience
   
   **Drawbacks**:
   - Added complexity
   - Learning curve
   - Maintenance overhead
   
   **Questions for Discussion**:
   1. Should we replace REST or run both?
   2. What's the migration timeline?
   3. Who will maintain it?
   ```

2. **Gather Feedback**
   - Allow 48-72 hours for team input
   - Address questions and concerns
   - Revise proposal based on feedback

3. **Document Decision**
   - Create ADR (Architecture Decision Record)
   - Update relevant documentation
   - Communicate to team

#### Architecture Decision Records (ADR)

Template: `docs/adr/NNNN-title.md`

```markdown
# ADR-0001: Use PostgreSQL for Primary Database

**Date**: 2026-02-08  
**Status**: Accepted  
**Deciders**: @user1, @user2, @user3  

## Context

We need to choose a database for production deployment.

## Decision

We will use PostgreSQL 14+ as our primary database.

## Rationale

- Strong ACID compliance
- Excellent JSON support
- Rich ecosystem
- Team familiarity
- Good performance

## Consequences

### Positive
- Reliable transactions
- Flexible data models
- Strong community support

### Negative
- Requires managed service or maintenance
- Slightly higher resource usage than SQLite
- Learning curve for complex queries

## Alternatives Considered

1. MongoDB: Rejected due to consistency concerns
2. MySQL: Rejected due to JSON support limitations
3. SQLite: Rejected due to concurrency limitations
```

---

## Metrics and KPIs

### Track Repository Health

#### Branch Metrics

```bash
# Daily tracking
echo "$(date +%Y-%m-%d),$(git branch -r | grep -v HEAD | wc -l)" \
  >> metrics/daily-branch-count.csv

# Weekly report
tail -7 metrics/daily-branch-count.csv | awk -F',' '{sum+=$2; count++} END {print "Avg branches:", sum/count}'
```

**Targets**:
- Total branches: < 20
- Average branch age: < 30 days
- Branches >90 days: 0

#### PR Metrics

```bash
# PR age distribution
gh pr list --state open --json number,createdAt \
  | jq -r '.[] | (now - (.createdAt | fromdateiso8601)) / 86400 | floor' \
  | sort -n | uniq -c

# Time to merge (closed PRs)
gh pr list --state closed --limit 50 --json number,createdAt,closedAt \
  | jq -r '.[] | ((.closedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 86400 | floor' \
  | awk '{sum+=$1; count++} END {print "Avg days to merge:", sum/count}'
```

**Targets**:
- Average PR age: < 7 days
- Time to first review: < 24 hours
- Time to merge: < 14 days

#### Workflow Metrics

```bash
# Workflow success rate
gh run list --limit 100 --json status,conclusion \
  | jq -r 'group_by(.conclusion) | map({conclusion: .[0].conclusion, count: length})'

# Average workflow duration
gh run list --limit 50 --json workflowName,createdAt,updatedAt \
  | jq -r '.[] | "\(.workflowName),\(((.updatedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 60)"' \
  | awk -F',' '{sum[$1]+=$2; count[$1]++} END {for(w in sum) print w":", sum[w]/count[w], "minutes"}'
```

**Targets**:
- Success rate: > 95%
- Average duration: Varies by workflow
- Failed runs: < 5% of total

### Dashboard

The repository already has an automated health dashboard updated by `deployment-health-dashboard.yml`. Ensure it includes:

- Branch count and age distribution
- PR count and age distribution
- Workflow success rates
- Recent deployment status
- Test coverage trends

---

## Appendix

### Recommended Tools

- **GitHub CLI**: `gh` for automation
- **Git Aliases**: Shortcuts for common commands
- **Pre-commit Hooks**: Automated checks before commit
- **Conventional Commits**: Standardized commit messages

### Git Aliases

Add to `~/.gitconfig`:

```ini
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --graph --oneline --all
    cleanup = !git branch --merged | grep -v '*' | xargs -n 1 git branch -d
    prune-all = fetch --all --prune
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
EOF

# Install hooks
pre-commit install
```

---

**Document Version**: 1.0.0  
**Last Updated**: 2026-02-08  
**Next Review**: 2026-05-08  
**Maintained By**: Repository Maintainers

**Remember**: These are guidelines, not rigid rules. Adapt them to your team's needs and always prioritize collaboration over process.
