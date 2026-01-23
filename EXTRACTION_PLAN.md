# Component Extraction Plan

This document outlines the specific extraction steps for migrating components from donor repositories into the canonical `pi-forge-quantum-genesis` platform.

## 🔮 **1. OINIO Oracle Engine Extraction**

**Source**: `quantum-pi-forge` (OINIO Soul System)  
**Target**: `core/oracle/`

### **Components to Extract**
- `oracle_engine.py` - Core deterministic reading algorithms
- `pattern_recognition.py` - Soul pattern analysis
- `personality_traits.py` - Cryptographic trait generation
- `divination_logic.py` - Oracle computation engine

### **Extraction Steps**
1. Copy core oracle files to `legacy/quantum-pi-forge/oracle/`
2. Refactor imports to work with FastAPI framework
3. Adapt CLI interfaces to REST API endpoints
4. Integrate with existing guardian monitoring system
5. Move cleaned code to `core/oracle/`

### **Integration Points**
- Connect to `/core/identity` for user context
- Power `/core/inft` personality trait generation
- Provide divination layer for platform features

---

## ⚡ **2. Pi Network Integration Extraction**

**Source**: `quantum-pi-forge-fixed`  
**Target**: `integrations/pi/`

### **Components to Extract**
- Pi SDK integration from `app/` directory
- Payment processing components
- Wallet connection logic
- Authentication flows

### **Extraction Steps**
1. Copy Pi Network components to `legacy/quantum-pi-forge-fixed/pi/`
2. Extract payment verification logic
3. Adapt Next.js components to work with FastAPI backend
4. Merge with existing Pi Network API integration in `server/main.py`
5. Move unified integration to `integrations/pi/`

### **Integration Points**
- Connect to `/core/identity` for wallet linking
- Power payment flows for NFT minting
- Provide authentication foundation

---

## 🧬 **3. OINIO Identity System Extraction**

**Source**: `quantum-pi-forge`  
**Target**: `core/identity/`

### **Components to Extract**
- Soul registry system
- Encrypted profile storage
- Memorial node management
- OG/OINIO identity mapping

### **Extraction Steps**
1. Copy identity components to `legacy/quantum-pi-forge/identity/`
2. Refactor encrypted storage to work with Supabase
3. Adapt CLI interfaces to REST API endpoints
4. Integrate with Pi Network wallet linking
5. Move cleaned code to `core/identity/`

### **Integration Points**
- Connect to `/integrations/pi` for wallet authentication
- Power `/core/oracle` for personalized readings
- Provide foundation for `/core/inft` creation

---

## 🧩 **4. NFT + iNFT Logic Extraction**

**Source**: `mr-nft-agent`, `oinio-contracts`, `pi-claimable-nft-demo`  
**Target**: `core/nft/`, `core/inft/`

### **Components to Extract**
- NFT minting logic from `mr-nft-agent`
- Smart contracts from `oinio-contracts`
- Claiming interfaces from `pi-claimable-nft-demo`
- Marketplace functionality

### **Extraction Steps**
1. Copy NFT components to `legacy/mr-nft-agent/`, `legacy/oinio-contracts/`, `legacy/pi-claimable-nft-demo/`
2. Extract smart contract ABIs and deployment scripts
3. Refactor minting logic to work with FastAPI
4. Integrate oracle-powered trait generation for iNFTs
5. Move unified NFT system to `core/nft/` and `core/inft/`

### **Integration Points**
- Use `/core/oracle` for iNFT trait generation
- Connect to `/core/identity` for ownership tracking
- Link to `/integrations/pi` for minting payments

---

## 📋 **Extraction Workflow**

### **Phase 1: Staging (Current)**
- ✅ Create directory structure
- ⏳ Extract components to `legacy/` directories
- ⏳ Analyze dependencies and integration points

### **Phase 2: Refactoring**
- ⏳ Adapt code for unified architecture
- ⏳ Update imports and dependencies
- ⏳ Create REST API interfaces where needed

### **Phase 3: Integration**
- ⏳ Merge components into core directories
- ⏳ Test integration points
- ⏳ Update documentation

### **Phase 4: Cleanup**
- ⏳ Remove legacy staging directories
- ⏳ Update CONSOLIDATION.md with completion status
- ⏳ Archive donor repositories

---

## 🛠️ **Technical Considerations**

### **Dependency Management**
- Consolidate `package.json` and `requirements.txt` files
- Resolve version conflicts between repositories
- Update import paths for unified structure

### **API Design**
- Standardize REST API patterns across all components
- Implement consistent error handling
- Add comprehensive API documentation

### **Security**
- Audit all extracted components for security issues
- Implement consistent authentication patterns
- Add guardian monitoring to all new endpoints

### **Testing**
- Create integration tests for all merged components
- Test cross-component interactions
- Validate end-to-end user flows

---

## 🎯 **Success Criteria**

- **Unified Platform**: Single repository with all three pillars
- **Zero Breaking Changes**: Existing production deployments continue working
- **Complete Integration**: Seamless flow between Pi payments, OINIO identity, and NFT creation
- **Production Ready**: Comprehensive testing and monitoring in place