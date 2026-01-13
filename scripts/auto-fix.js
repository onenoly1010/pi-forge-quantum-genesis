#!/usr/bin/env node

/**
 * Automated Fix Script for Pi Forge Quantum Genesis
 * Validates and fixes common configuration issues
 */

const fs = require('fs');
const path = require('path');

const rootDir = path.join(__dirname, '..');
let issuesFound = 0;
let issuesFixed = 0;
let dryRun = process.argv.includes('--dry-run');

const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m'
};

function logIssue(message) {
  console.log(`${colors.red}❌ ISSUE: ${message}${colors.reset}`);
  issuesFound++;
}

function logFix(message) {
  console.log(`${colors.green}✅ FIXED: ${message}${colors.reset}`);
  issuesFixed++;
}

function logCheck(message) {
  console.log(`${colors.green}✓ OK: ${message}${colors.reset}`);
}

console.log(`${colors.cyan}🔧 Pi Forge Quantum Genesis - Automated Fix Script${colors.reset}`);
console.log('='.repeat(70));
console.log('');

if (dryRun) {
  console.log(`${colors.yellow}⚠️  DRY RUN MODE - No changes will be made${colors.reset}`);
  console.log('');
}

// Check 1: Vercel Configuration
console.log(`${colors.yellow}🔍 Checking Vercel Configuration...${colors.reset}`);
console.log('');

const vercelJsonPath = path.join(rootDir, 'vercel.json');
if (fs.existsSync(vercelJsonPath)) {
  const vercelJson = JSON.parse(fs.readFileSync(vercelJsonPath, 'utf8'));
  
  if (vercelJson.framework === null) {
    logCheck('Vercel framework is null (correct)');
  } else if (vercelJson.framework === 'nextjs') {
    logIssue('Vercel incorrectly configured as Next.js project');
    
    if (!dryRun) {
      vercelJson.framework = null;
      fs.writeFileSync(vercelJsonPath, JSON.stringify(vercelJson, null, 2) + '\n');
      logFix('Set vercel.json framework to null');
    }
  }
  
  if (vercelJson.buildCommand === 'npm run build') {
    logCheck('Build command configured correctly');
  } else {
    logIssue('Build command missing or incorrect');
    
    if (!dryRun) {
      vercelJson.buildCommand = 'npm run build';
      fs.writeFileSync(vercelJsonPath, JSON.stringify(vercelJson, null, 2) + '\n');
      logFix('Added buildCommand to vercel.json');
    }
  }
} else {
  logIssue('vercel.json not found');
}

// Check 2: package.json
console.log('');
console.log(`${colors.yellow}🔍 Checking package.json...${colors.reset}`);
console.log('');

const packageJsonPath = path.join(rootDir, 'package.json');
if (fs.existsSync(packageJsonPath)) {
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  
  const requiredScripts = {
    'build': 'npm run build:static',
    'build:static': 'node scripts/build.js',
    'typecheck': 'tsc --noEmit'
  };
  
  let scriptsOk = true;
  
  if (!packageJson.scripts) {
    logIssue('No scripts section in package.json');
    scriptsOk = false;
  } else {
    for (const [name, command] of Object.entries(requiredScripts)) {
      if (!packageJson.scripts[name]) {
        scriptsOk = false;
      } else if (packageJson.scripts[name] !== command) {
        scriptsOk = false;
      }
    }
  }
  
  if (scriptsOk) {
    logCheck('All required scripts present and correct');
  }
} else {
  logIssue('package.json not found');
}

// Check 3: Build Script
console.log('');
console.log(`${colors.yellow}🔍 Checking build script...${colors.reset}`);
console.log('');

const buildScriptPath = path.join(rootDir, 'scripts', 'build.js');
if (fs.existsSync(buildScriptPath)) {
  logCheck('Build script exists');
} else {
  logIssue('Build script not found');
}

// Check 4: TypeScript Configuration
console.log('');
console.log(`${colors.yellow}🔍 Checking TypeScript configuration...${colors.reset}`);
console.log('');

const tsconfigPath = path.join(rootDir, 'tsconfig.json');
if (fs.existsSync(tsconfigPath)) {
  logCheck('tsconfig.json exists');
  
  const tsconfig = JSON.parse(fs.readFileSync(tsconfigPath, 'utf8'));
  
  if (tsconfig.compilerOptions && tsconfig.compilerOptions.types) {
    if (tsconfig.compilerOptions.types.includes('next')) {
      logIssue('TypeScript configured with Next.js types');
      
      if (!dryRun) {
        tsconfig.compilerOptions.types = tsconfig.compilerOptions.types.filter(t => t !== 'next');
        fs.writeFileSync(tsconfigPath, JSON.stringify(tsconfig, null, 2) + '\n');
        logFix('Removed Next.js from TypeScript types');
      }
    } else {
      logCheck('TypeScript not configured for Next.js');
    }
  } else {
    logCheck('TypeScript types not explicitly configured');
  }
}

// Summary
console.log('');
console.log('='.repeat(70));
console.log(`${colors.cyan}📊 SUMMARY${colors.reset}`);
console.log('='.repeat(70));
console.log('');
console.log(`Issues Found:    ${issuesFound}`);

if (!dryRun) {
  console.log(`Issues Fixed:    ${issuesFixed}`);
  
  const remainingIssues = issuesFound - issuesFixed;
  if (remainingIssues > 0) {
    console.log(`Manual Fixes:    ${remainingIssues}`);
  }
}

console.log('');

if (issuesFound === 0) {
  console.log(`${colors.green}✅ All checks passed! Repository is healthy.${colors.reset}`);
  process.exit(0);
} else if (dryRun) {
  console.log(`${colors.yellow}⚠️  Run script without --dry-run to apply automatic fixes${colors.reset}`);
  process.exit(1);
} else {
  const remainingIssues = issuesFound - issuesFixed;
  if (remainingIssues === 0) {
    console.log(`${colors.green}✅ All issues fixed automatically!${colors.reset}`);
    process.exit(0);
  } else {
    console.log(`${colors.yellow}⚠️  Some issues remain. Check output above.${colors.reset}`);
    process.exit(1);
  }
}