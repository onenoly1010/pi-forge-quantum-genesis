# Safe Proposals (Unsigned)

Purpose: Draft unsigned transaction proposals for use with Gnosis Safe / Safe.app. DO NOT EXECUTE WITHOUT OWNER CONSENT.

Files:
- `renounce_proposal.json` — unsigned tx payload for renounceOwnership()
- `add_liquidity_template.js` — script to build unsigned addLiquidity tx
- `lock_lp_template.js` — template to prepare LP lock/burn tx
- `SECURITY_ROTATION_CHECKLIST.md` — steps to rotate keys and revoke access
- `gitignore_additions.txt` — suggested `.gitignore` lines to add

How to use:
1. Review the JSON and templates in a secure environment.
2. Use your Safe UI or the Safe CLI to propose the JSON (no signing automated here).
3. Require multisig confirmations before executing.

> **Warning:** All changes like renounceOwnership are irreversible. Confirm consensus among signers and ensure backups of necessary data before proceeding.
