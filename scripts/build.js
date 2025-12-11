#!/usr/bin/env node

/**
 * Build script for Vercel deployment
 * Creates the public directory and copies static assets
 */

const fs = require('fs');
const path = require('path');

const rootDir = path.join(__dirname, '..');
const publicDir = path.join(rootDir, 'public');

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
    fs.rmSync(publicDir, { recursive: true, force: true });
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
  console.log(`📁 Output directory: ${publicDir}\n`);
}

// Run the build
try {
  build();
  process.exit(0);
} catch (error) {
  console.error('\n❌ Build failed:', error.message);
  process.exit(1);
}
