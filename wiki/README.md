# Wiki Documentation - Maintenance Guide

This directory contains wiki-ready documentation for the Quantum Pi Forge ecosystem. The content is structured for manual transfer to the GitHub Wiki.

## 📋 Overview

The wiki provides comprehensive documentation organized into:
- **Foundation** - Core principles and Genesis declaration
- **Getting Started** - Quick starts and guides for different user types
- **Core Concepts** - Fundamental system concepts
- **Architecture** - Technical architecture and references
- **Operations** - Maintenance and operational procedures
- **Pi Network** - Pi Network integration documentation
- **Governance** - Governance structure and community guidelines

## 🚀 How to Transfer to GitHub Wiki

### Step 1: Enable GitHub Wiki

1. Go to your repository settings: https://github.com/onenoly1010/pi-forge-quantum-genesis/settings
2. Scroll to "Features" section
3. Check the "Wikis" checkbox to enable the wiki

### Step 2: Clone the Wiki Repository

```bash
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.wiki.git
cd pi-forge-quantum-genesis.wiki
```

### Step 3: Copy Wiki Files

```bash
# Copy all wiki markdown files from this directory
cp /path/to/pi-forge-quantum-genesis/wiki/*.md .

# Remove the README.md (or rename it)
rm README.md  # This file is for maintenance, not wiki content
```

### Step 4: Commit and Push

```bash
git add .
git commit -m "Add comprehensive wiki documentation"
git push origin master
```

### Step 5: Verify

Visit your wiki at: https://github.com/onenoly1010/pi-forge-quantum-genesis/wiki

## 📝 Wiki Page Naming Conventions

GitHub Wiki uses filename-based routing:
- `Home.md` becomes the homepage
- `Genesis-Declaration.md` becomes accessible at `/Genesis-Declaration`
- Spaces in filenames become hyphens in URLs
- Use Title Case with hyphens: `Quick-Start.md`, `API-Reference.md`

### Internal Links

Use wiki link syntax: `[[Page-Name]]`
- `[[Home]]` links to Home.md
- `[[Genesis Declaration]]` links to Genesis-Declaration.md
- `[[Quick Start]]` links to Quick-Start.md

GitHub automatically converts spaces to hyphens in wiki links.

## 🔄 Maintaining the Wiki

### Updating Content

1. Edit files in this `/wiki/` directory
2. Test locally if needed
3. Commit changes to main repository
4. Transfer updated files to wiki repository
5. Push to wiki repository

### Adding New Pages

1. Create new `.md` file in this directory
2. Use Title-Case-With-Hyphens.md naming
3. Add to `_Sidebar.md` navigation
4. Add cross-references in related pages
5. Include "Last Updated" date
6. Add "See Also" section

### Page Template

```markdown
# Page Title

**Last Updated**: December 2025

Brief introduction to the page content.

## Section 1

Content here...

## Section 2

More content...

## See Also

- [[Related Page 1]]
- [[Related Page 2]]
- [External Link](https://example.com)

---

[[Home]] | [[Other Relevant Page]]
```

## ✅ Quality Checklist

Before transferring content, ensure:
- [ ] All pages use `[[Wiki Link]]` syntax
- [ ] `_Sidebar.md` includes all pages
- [ ] `_Footer.md` is up to date
- [ ] Each page has "Last Updated" date
- [ ] Cross-references are accurate
- [ ] External URLs are correct (HTTPS)
- [ ] Code blocks have language hints
- [ ] Tables are properly formatted
- [ ] Lists are consistent (use `-` for bullets)
- [ ] Emoji usage is consistent with repository style

## 🎯 Wiki Structure

```
wiki/
├── README.md              # This maintenance guide
├── _Sidebar.md           # Navigation sidebar
├── _Footer.md            # Footer on all pages
├── Home.md               # Wiki homepage
│
├── Foundation/
│   ├── Genesis-Declaration.md
│   └── Canon-of-Closure.md
│
├── Getting Started/
│   ├── Quick-Start.md
│   ├── Installation.md
│   ├── For-Users.md
│   ├── For-Developers.md
│   └── For-Guardians.md
│
├── Core Concepts/
│   ├── Autonomous-Agents.md
│   └── Sacred-Trinity.md
│
├── Architecture/
│   ├── Ecosystem-Overview.md
│   ├── API-Reference.md
│   ├── Smart-Contracts.md
│   ├── Deployment-Guide.md
│   └── Verification-System.md
│
├── Operations/
│   ├── Runbook-Index.md
│   ├── CI-CD-Automation.md
│   ├── Monitoring-Observability.md
│   ├── Troubleshooting.md
│   └── Operational-Team.md
│
├── Pi Network/
│   ├── Pi-Network-Overview.md
│   ├── Payment-API.md
│   └── Mainnet-Guide.md
│
└── Governance/
    ├── Identity-Lock.md
    ├── Canon-Artifacts.md
    ├── Guardian-Playbook.md
    └── Contribution-Guide.md
```

## 🔗 Important Links

- **Main Repository**: https://github.com/onenoly1010/pi-forge-quantum-genesis
- **Wiki Repository**: https://github.com/onenoly1010/pi-forge-quantum-genesis.wiki.git
- **Live Wiki**: https://github.com/onenoly1010/pi-forge-quantum-genesis/wiki (after enabling)
- **Genesis Declaration**: See `GENESIS.md` in main repository

## 📚 Source Documentation

Wiki content is derived from:
- `GENESIS.md` - Foundational principles
- `README.md` - Repository overview
- `ECOSYSTEM_OVERVIEW.md` - Ecosystem structure
- `QUICK_START.md` - Quick start guide
- `RUNBOOK.md` - Operational procedures
- `DEPLOYMENT.md` - Deployment instructions
- `docs/*.md` - Various documentation files

## 🛡️ Governance

All wiki content must align with:
1. **GENESIS.md** principles (Sovereignty, Transparency, Inclusivity, Non-hierarchy, Safety)
2. **Canon of Closure** documentation standards
3. **OINIO Seal** commitments from Solstice 2025

Changes to foundational pages require steward approval.

## 🆘 Support

For questions about wiki maintenance:
1. Review this README
2. Check existing wiki pages for examples
3. Open an issue in the main repository
4. Tag @onenoly1010 for guidance

---

**Remember**: The wiki is a living document. Keep it clear, accurate, and aligned with the Genesis principles. 🏛️⚛️🔥
