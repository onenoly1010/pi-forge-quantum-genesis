#!/usr/bin/env node

/**
 * Build script for Vercel deployment
 * Creates the public directory and copies static assets
 */

const fs = require('fs');
const path = require('path');

// Resolve project root from the current working directory for build environment alignment
const rootDir = process.cwd();
const publicDir = path.join(rootDir, 'public');

// Debug logging for path resolution (gated behind DEBUG env flag)
// Normalize env vars: only "1", "true", or "yes" (case-insensitive) enable debug mode
const isDebugEnabled = () => {
  const debug = process.env.DEBUG || process.env.VERCEL_DEBUG || '';
  return ['1', 'true', 'yes'].includes(debug.toLowerCase());
};

if (isDebugEnabled()) {
  console.log('Build script path resolution:');
  console.log(`  Script directory: ${__dirname}`);
  console.log(`  Working directory (rootDir): ${rootDir}`);
  console.log(`  Public directory: ${publicDir}\n`);
}

// Files to copy from root to public directory
const staticFiles = [
  'index.html',
  'ceremonial_interface.html',
  'resonance_dashboard.html',
  'spectral_command_shell.html',
  'pi-forge-integration.js'
];

// Directories to copy from root to public directory
const staticDirs = [
  'frontend'
];

/**
 * Recursively copy a directory
 */
function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

/**
 * Copy a single file
 */
function copyFile(src, dest) {
  const srcPath = path.join(rootDir, src);
  const destPath = path.join(publicDir, path.basename(src));

  if (fs.existsSync(srcPath)) {
    fs.copyFileSync(srcPath, destPath);
    console.log(`✓ Copied ${src}`);
  } else {
    console.warn(`⚠ File not found: ${src}`);
  }
}

/**
 * Main build function
 */
function build() {
  console.log('Building static assets for Vercel deployment...\n');

  // Clean and create public directory
  if (fs.existsSync(publicDir)) {
    fs.rmSync(publicDir, { recursive: true });
  }
  fs.mkdirSync(publicDir, { recursive: true });
  console.log('✓ Created public directory\n');

  // Copy static files
  console.log('Copying static files:');
  for (const file of staticFiles) {
    copyFile(file, publicDir);
  }
  console.log('');

  // Copy static directories
  console.log('Copying static directories:');
  for (const dir of staticDirs) {
    const srcPath = path.join(rootDir, dir);
    const destPath = path.join(publicDir, dir);
    
    if (fs.existsSync(srcPath)) {
      copyDir(srcPath, destPath);
      console.log(`✓ Copied ${dir}/`);
    } else {
      console.warn(`⚠ Directory not found: ${dir}`);
    }
  }

  console.log('\n✅ Build completed successfully!');
  console.log(`📁 Output directory: ${publicDir}`);
  
  // Verification step: Confirm public directory exists and list contents (gated behind DEBUG env flag)
  if (isDebugEnabled()) {
    console.log('\nVerification:');
    if (fs.existsSync(publicDir)) {
      console.log('✓ Public directory exists');
      const files = fs.readdirSync(publicDir);
      console.log(`✓ Contains ${files.length} items:`);
      files.forEach(file => {
        const filePath = path.join(publicDir, file);
        const stats = fs.statSync(filePath);
        const type = stats.isDirectory() ? 'dir' : 'file';
        console.log(`  - ${file} (${type})`);
      });
    } else {
      throw new Error('Public directory was not created!');
    }
    console.log('');
  } else {
    // Quick verification without detailed listing
    if (!fs.existsSync(publicDir)) {
      throw new Error('Public directory was not created!');
    }
  }
}

// Run the build
try {
  build();
  process.exit(0);
} catch (error) {
  console.error('\n❌ Build failed:', error.message);
  console.error('\nStack trace:');
  console.error(error.stack);
  process.exit(1);
}
