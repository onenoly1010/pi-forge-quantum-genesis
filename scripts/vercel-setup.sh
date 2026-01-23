#!/bin/bash

# Vercel Setup Script
# This script helps configure the Vercel CLI for autonomous deployment

set -e

echo "======================================"
echo "Pi Forge Quantum Genesis"
echo "Vercel CLI Setup Script"
echo "======================================"
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Vercel CLI not found. Installing..."
    npm install -g vercel
    echo "✅ Vercel CLI installed successfully"
else
    echo "✅ Vercel CLI already installed"
    vercel --version
fi

echo ""
echo "======================================"
echo "Authentication"
echo "======================================"
echo ""

# Login to Vercel
echo "Please authenticate with Vercel..."
vercel login

echo ""
echo "======================================"
echo "Project Setup"
echo "======================================"
echo ""

# Check if already linked to a project
if [ -d ".vercel" ]; then
    echo "⚠️  Project already linked to Vercel"
    echo "Current configuration:"
    cat .vercel/project.json 2>/dev/null || echo "No project.json found"
    echo ""
    read -p "Do you want to re-link? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing configuration"
    else
        echo "Re-linking project..."
        vercel link
    fi
else
    echo "Linking project to Vercel..."
    vercel link
fi

echo ""
echo "======================================"
echo "Environment Variables"
echo "======================================"
echo ""

echo "Setting up environment variables..."
echo ""
echo "The following environment variables are recommended:"
echo "  - PI_APP_SECRET (required for Pi Network integration)"
echo "  - GUARDIAN_SLACK_WEBHOOK_URL (optional for alerts)"
echo "  - SENDGRID_API_KEY (optional for email notifications)"
echo ""
read -p "Do you want to add environment variables now? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Adding environment variables..."
    echo "You can also add them later via:"
    echo "  - Vercel Dashboard: https://vercel.com/dashboard"
    echo "  - CLI: vercel env add <name> <environment>"
    echo ""
    
    read -p "Add PI_APP_SECRET for production? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        vercel env add PI_APP_SECRET production
    fi
    
    read -p "Add GUARDIAN_SLACK_WEBHOOK_URL for production? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        vercel env add GUARDIAN_SLACK_WEBHOOK_URL production
    fi
else
    echo "Skipping environment variable setup"
    echo "You can add them later via Vercel Dashboard or CLI"
fi

echo ""
echo "======================================"
echo "Deployment Test"
echo "======================================"
echo ""

read -p "Do you want to deploy to preview now? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Deploying to preview environment..."
    vercel
    echo ""
    echo "✅ Preview deployment completed"
else
    echo "Skipping deployment"
    echo "You can deploy later with: vercel (preview) or vercel --prod (production)"
fi

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Configure environment variables (if not done)"
echo "  2. Deploy to production: vercel --prod"
echo "  3. Set up GitHub integration for CI/CD"
echo "  4. Configure custom domain (optional)"
echo ""
echo "Useful commands:"
echo "  - Deploy preview: vercel"
echo "  - Deploy production: vercel --prod"
echo "  - View deployments: vercel ls"
echo "  - View logs: vercel logs <url>"
echo "  - Add environment: vercel env add <name> <environment>"
echo ""
echo "Documentation:"
echo "  - Local: ./VERCEL_DEPLOYMENT_GUIDE.md"
echo "  - Agent Handoff: ./AUTONOMOUS_DEPLOYMENT_HANDOFF.md"
echo "  - Vercel Docs: https://vercel.com/docs"
echo ""
echo "✅ Vercel setup completed successfully!"
