# Security Status

**Last Updated:** 2026-05-31
**Repository:** pi-forge-quantum-genesis
**Status:** Archived genesis compendium

## Completed Remediation

The archived genesis repository has been triaged across all package zones.

Completed safe fixes:

- Press agent dependency audit fixed.
- Python python-dotenv advisory range corrected.
- Python gradio advisory range corrected.
- Soroban SDK upgraded from 21.0.0 to 22.0.11.
- Soroban contract checked successfully with cargo check.

## Remaining Advisory

GitHub Dependabot still reports one open advisory:

- Dependency: ws
- Manifest: root package-lock.json
- Dependency path: ethers -> ws
- Patched ws version: 8.20.1

Local npm audit only offers remediation through a forced breaking downgrade:

npm audit fix --force
Will install ethers@5.8.0, which is a breaking change

This repository currently uses the ethers v6 dependency line. A forced downgrade to ethers v5 is intentionally rejected because this repository is archived and the downgrade may break historical scripts or compatibility assumptions.

## Policy

Do not run npm audit fix --force.

The remaining advisory should be revisited only if a non-breaking ethers v6-compatible remediation becomes available or if the root runtime path is removed entirely.
