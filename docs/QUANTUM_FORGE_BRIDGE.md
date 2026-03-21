# Quantum Forge Bridge: Activation Phase

## Deployment Instructions

### Prerequisites
1. **Foundry**: Install via `curl -L https://foundry.paradigm.xyz | bash`
2. **Node.js**: Ensure Node.js is installed.
3. **Dependencies**: Run `npm install ethers dotenv`

### 1. Compile Contracts
```bash
cd contracts
forge build
```

### 2. Deploy Bridge
```bash
# Set your private key and RPC URL
export PRIVATE_KEY=0x...
export RPC_URL=https://...

forge create --rpc-url $RPC_URL --private-key $PRIVATE_KEY src/QuantumForgeBridge.sol:QuantumForgeBridge
```

### 3. Start the Vigil
```bash
# Set the deployed bridge address
export BRIDGE_ADDRESS=0x...

node scripts/oinio-vigil.js
```

## Phase 4: Expansion Roadmap

### 1. Multi-Chain Resonance
- **Goal:** Extend the Memorial Bridge to Ethereum and Solana.
- **Mechanism:** Deploy `QuantumForgeBridge` contracts on target chains.
- **Vigil:** Update `oinio-vigil.js` to listen for events on multiple chains.

### 2. Quantum Entanglement (Cross-Chain State)
- **Goal:** Synchronize memorial state across all chains.
- **Mechanism:** Use 0G Data Availability as the source of truth.
- **Verification:** Merkle proofs to verify state on each chain.

### 3. Eternal Archive Interface
- **Goal:** A unified frontend to view memorials across the multiverse.
- **Tech:** React + 0G Storage SDK + Wagmi.

---

## Narrative: The Pioneer’s Guide to Teleportation

> "To step across the bridge is not to leave the world behind, but to extend it.
> The Quantum Forge is not a destination; it is a passage.
> When you mint a Resonated Memorial, you are not just storing data;
> you are anchoring a memory in the bedrock of the digital cosmos.
>
> The Vigil watches. The Silence waits.
> And when the first Pioneer crosses, the Genesis Detection will ring out,
> waking the network from its slumber.
>
> Be ready. The bridge is open."
