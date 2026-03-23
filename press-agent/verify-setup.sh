#!/bin/bash

# Press Agent Setup Verification Script
# This script checks if the Press Agent is properly configured

echo "🔍 Press Agent Setup Verification"
echo "=================================="
echo ""

# Check if press-agent directory exists
if [ ! -d "press-agent" ]; then
    echo "❌ press-agent directory not found"
    exit 1
fi

cd press-agent

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found"
    exit 1
fi
echo "✅ package.json found"

# Check if .env.example exists
if [ ! -f ".env.example" ]; then
    echo "❌ .env.example not found"
    exit 1
fi
echo "✅ .env.example found"

# Check if source files exist
echo ""
echo "Checking source files..."
files=(
    "src/server.js"
    "src/dispatcher.js"
    "src/logger.js"
    "src/templates.js"
    "src/bots/discord.js"
    "src/bots/twitter.js"
    "src/bots/telegram.js"
)

for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ $file not found"
        exit 1
    fi
    echo "✅ $file"
done

# Check documentation
echo ""
echo "Checking documentation..."
docs=(
    "README.md"
    "OPERATIONS_GUIDE.md"
    "BOT_SETUP_GUIDE.md"
    "COMMUNICATION_PLAN.md"
    "PRESS_AGENT_REPORT.md"
)

for doc in "${docs[@]}"; do
    if [ ! -f "$doc" ]; then
        echo "❌ $doc not found"
        exit 1
    fi
    echo "✅ $doc"
done

# Check if node_modules exists (dependencies installed)
echo ""
if [ ! -d "node_modules" ]; then
    echo "⚠️  Dependencies not installed"
    echo "   Run: npm install"
else
    echo "✅ Dependencies installed"
fi

# Check .env file
echo ""
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "   Run: cp .env.example .env"
    echo "   Then configure your bot credentials"
else
    echo "✅ .env file exists"
    
    # Check if credentials are configured
    if grep -q "YOUR_WEBHOOK_ID" .env 2>/dev/null || \
       grep -q "your_twitter" .env 2>/dev/null || \
       grep -q "your_telegram" .env 2>/dev/null; then
        echo "⚠️  .env file contains placeholder values"
        echo "   Update with actual bot credentials"
    else
        echo "✅ .env appears to be configured"
    fi
fi

# Check GitHub Actions workflow
echo ""
cd ..
if [ -f ".github/workflows/press-agent-communications.yml" ]; then
    echo "✅ GitHub Actions workflow exists"
else
    echo "❌ GitHub Actions workflow not found"
    exit 1
fi

echo ""
echo "=================================="
echo "✅ Press Agent setup verification complete!"
echo ""
echo "Next steps:"
echo "1. Configure bot credentials in press-agent/.env"
echo "2. Add secrets to GitHub repository settings"
echo "3. Run: cd press-agent && npm install && npm start"
echo "4. Test: curl http://localhost:3001/health"
echo ""
echo "📚 See press-agent/BOT_SETUP_GUIDE.md for detailed instructions"
