# Legacy Code Staging

This directory temporarily holds code extracted from donor repositories during the consolidation process.

## Purpose
- Staging area for component extraction and refactoring
- Temporary storage during migration from donor repositories
- Code that needs integration work before moving to core directories

## Workflow
1. Extract code from donor repositories to `/legacy/[repo-name]/`
2. Refactor and adapt code for integration
3. Move cleaned code to appropriate `/core/` or `/integrations/` directories
4. Remove legacy staging once integration is complete

## Current Staging
- `quantum-pi-forge/` - OINIO Soul System components
- `quantum-pi-forge-fixed/` - Pi Network integration components
- `mr-nft-agent/` - NFT functionality
- `oinio-contracts/` - Smart contracts
- `pi-claimable-nft-demo/` - NFT claiming interfaces