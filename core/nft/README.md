# NFT Functionality

This directory will contain NFT-related functionality extracted from donor repositories.

## Components to Extract
- NFT minting logic from `mr-nft-agent`
- Smart contracts from `oinio-contracts`
- NFT claiming interfaces from `pi-claimable-nft-demo`
- Marketplace functionality

## Integration Points
- Connects to `/core/identity` for ownership tracking
- Uses `/core/oracle` for metadata generation
- Links to `/integrations/pi` for payment processing