#!/bin/bash

# Wiki Migration Script for pi-forge-quantum-genesis
# This script completes the migration of wiki directory contents to the GitHub Wiki

set -e

echo "🚀 Starting Wiki Migration..."
echo ""

# Check if we're in the right directory
if [ ! -d "wiki" ]; then
    echo "❌ Error: 'wiki' directory not found. Please run this script from the repository root."
    exit 1
fi

# Clone the wiki repository
echo "📥 Cloning GitHub Wiki repository..."
WIKI_DIR=$(mktemp -d)
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.wiki.git "$WIKI_DIR"

# Copy all wiki files
echo "📋 Copying wiki files..."
cp -v wiki/*.md "$WIKI_DIR/"

# Change to wiki directory
cd "$WIKI_DIR"

# Configure git
git config user.email "${GIT_USER_EMAIL:-github-actions[bot]@users.noreply.github.com}"
git config user.name "${GIT_USER_NAME:-github-actions[bot]}"

# Add all files
echo "➕ Adding files to git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit - wiki is already up to date!"
    cd ..
    rm -rf "$WIKI_DIR"
    exit 0
fi

# Commit changes
echo "💾 Committing changes..."
git commit -m "Migrated contents from the main repository's wiki directory"

# Push to GitHub
echo "⬆️  Pushing to GitHub Wiki..."
git push origin master

# Cleanup
cd ..
rm -rf "$WIKI_DIR"

echo ""
echo "✅ Wiki migration completed successfully!"
echo "🌐 View your wiki at: https://github.com/onenoly1010/pi-forge-quantum-genesis/wiki"
