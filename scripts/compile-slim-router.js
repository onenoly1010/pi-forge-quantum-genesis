#!/usr/bin/env node

const solc = require('solc');
const fs = require('fs');
const path = require('path');

// Read all contract files
function readContract(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

// Build input for solc
const contracts = {
  'UniswapV2Router02Slim.sol': readContract(path.join(__dirname, '../contracts/dex-slim/UniswapV2Router02Slim.sol')),
  'MockERC20.sol': readContract(path.join(__dirname, '../contracts/dex-slim/MockERC20.sol')),
  'interfaces/IERC20.sol': readContract(path.join(__dirname, '../contracts/dex-slim/interfaces/IERC20.sol')),
  'interfaces/IUniswapV2Factory.sol': readContract(path.join(__dirname, '../contracts/dex-slim/interfaces/IUniswapV2Factory.sol')),
  'interfaces/IUniswapV2Pair.sol': readContract(path.join(__dirname, '../contracts/dex-slim/interfaces/IUniswapV2Pair.sol')),
};

const input = {
  language: 'Solidity',
  sources: {},
  settings: {
    optimizer: {
      enabled: true,
      runs: 1,
    },
    viaIR: true,
    outputSelection: {
      '*': {
        '*': ['evm.bytecode.object', 'evm.deployedBytecode.object', 'metadata']
      }
    }
  }
};

// Add all contracts to input
for (const [filename, content] of Object.entries(contracts)) {
  input.sources[filename] = { content };
}

console.log('🔧 Compiling UniswapV2Router02Slim with optimization...');
console.log('⚙️  Settings: optimizer runs=1, viaIR=true\n');

const output = JSON.parse(solc.compile(JSON.stringify(input)));

// Check for errors
if (output.errors) {
  const errors = output.errors.filter(e => e.severity === 'error');
  if (errors.length > 0) {
    console.error('❌ Compilation errors:');
    errors.forEach(err => console.error(err.formattedMessage));
    process.exit(1);
  }
  
  const warnings = output.errors.filter(e => e.severity === 'warning');
  if (warnings.length > 0) {
    console.warn('⚠️  Warnings:');
    warnings.forEach(warn => console.warn(warn.formattedMessage));
  }
}

// Get bytecode for slim router
const contract = output.contracts['UniswapV2Router02Slim.sol']['UniswapV2Router02Slim'];
if (!contract) {
  console.error('❌ Could not find compiled contract');
  process.exit(1);
}

const bytecode = contract.evm.deployedBytecode.object;
const bytecodeSize = bytecode.length / 2; // Hex string, so divide by 2 for bytes

console.log('✅ Compilation successful!');
console.log(`📏 Bytecode size: ${bytecodeSize} bytes`);
console.log(`📊 24KB limit: 24,576 bytes`);
console.log(`📈 Percentage used: ${((bytecodeSize / 24576) * 100).toFixed(2)}%`);

if (bytecodeSize > 24576) {
  console.error(`\n❌ ERROR: Bytecode exceeds 24KB limit by ${bytecodeSize - 24576} bytes`);
  process.exit(1);
} else {
  const remaining = 24576 - bytecodeSize;
  console.log(`✅ Under 24KB limit! ${remaining} bytes remaining\n`);
}

// Save artifacts
const artifactsDir = path.join(__dirname, '../artifacts/contracts/dex-slim');
fs.mkdirSync(artifactsDir, { recursive: true });

const artifact = {
  contractName: 'UniswapV2Router02Slim',
  abi: JSON.parse(contract.metadata).output.abi,
  bytecode: '0x' + contract.evm.bytecode.object,
  deployedBytecode: '0x' + bytecode,
  linkReferences: {},
  deployedLinkReferences: {}
};

fs.writeFileSync(
  path.join(artifactsDir, 'UniswapV2Router02Slim.json'),
  JSON.stringify(artifact, null, 2)
);

console.log('📁 Artifact saved to: artifacts/contracts/dex-slim/UniswapV2Router02Slim.json');
console.log('🎉 Build complete!');
