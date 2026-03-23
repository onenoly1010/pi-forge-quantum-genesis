# iNFT Creation and Management

This directory contains intelligent NFT (iNFT) functionality with oracle-driven personality traits and decentralized storage integration.

## Components

- **0G Storage Integration** - Sovereign memory persistence for AI/agent iNFTs
  - See [0G_STORAGE_INTEGRATION.md](./0G_STORAGE_INTEGRATION.md) for complete documentation
  - TypeScript implementation: [zero-g-storage.ts](./zero-g-storage.ts)
  - Python implementation: See `/server/integrations/zero_g_storage.py`
- iNFT minting with dynamic traits
- Oracle-powered metadata generation
- Personality trait algorithms
- Soul-bound NFT logic

## Integration Points

- Uses `/core/oracle` for trait generation
- Connects to `/core/identity` for soul binding
- Links to `/core/nft` for base NFT functionality
- Integrates with `/integrations/pi` for minting payments
- **NEW**: 0G Storage for encrypted AI/agent memory persistence