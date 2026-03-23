# 🗣️ Press Agent Operations Guide

## Overview

The **Press Agent** is Quantum Pi Forge's autonomous communications specialist, responsible for coordinating all public announcements, social media updates, and community notifications across multiple platforms.

## 🎯 Purpose

The Press Agent ensures:
- **Consistent messaging** across all communication channels
- **Automated announcements** for releases, deployments, and milestones
- **Transparent communication** with the community
- **Wiki synchronization** for documentation updates
- **Event-driven notifications** without manual intervention

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│          Press Agent Communication System           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐      ┌──────────────────┐        │
│  │   GitHub    │─────▶│  Communication   │        │
│  │   Events    │      │   Dispatcher     │        │
│  └─────────────┘      └──────────────────┘        │
│                              │                      │
│              ┌───────────────┼───────────────┐     │
│              ▼               ▼               ▼     │
│       ┌──────────┐    ┌──────────┐   ┌──────────┐│
│       │ Discord  │    │ Twitter  │   │ Telegram ││
│       │   Bot    │    │   Bot    │   │   Bot    ││
│       └──────────┘    └──────────┘   └──────────┘│
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Configure Environment Variables

Copy the example configuration:
```bash
cd press-agent
cp .env.example .env
```

Edit `.env` and add your bot credentials:
```bash
# Discord
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN

# Twitter/X
TWITTER_BEARER_TOKEN=your_bearer_token

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 2. Install Dependencies

```bash
cd press-agent
npm install
```

### 3. Start the Press Agent

```bash
npm start
```

The Press Agent API will be available at `http://localhost:3001`

## 📡 Communication Channels

### Discord Integration

**Setup:**
1. Go to your Discord server
2. Navigate to Server Settings → Integrations → Webhooks
3. Create a new webhook
4. Copy the webhook URL
5. Add to `.env` as `DISCORD_WEBHOOK_URL`

**Features:**
- Rich embeds with colors and formatting
- Structured announcement cards
- Automatic timestamps
- Custom bot name and avatar

### Twitter/X Integration

**Setup:**
1. Visit [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new app or use existing
3. Generate Bearer Token or OAuth tokens
4. Add credentials to `.env`

**Features:**
- Auto-formatted tweets (280 char limit)
- Thread support for longer announcements
- Hashtag automation
- Link shortening support

### Telegram Integration

**Setup:**
1. Talk to [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token
4. Send a message to your bot
5. Visit `https://api.telegram.org/bot<TOKEN>/getUpdates` to get chat ID
6. Add both to `.env`

**Features:**
- Markdown formatting
- Inline links
- Photo/media support
- Channel broadcast capabilities

## 🔌 API Endpoints

### Health Check
```bash
GET /health
```

### Communication Status
```bash
GET /api/communications/status

Response:
{
  "success": true,
  "status": {
    "discord": { "enabled": true, "configured": true },
    "twitter": { "enabled": true, "configured": true },
    "telegram": { "enabled": true, "configured": true }
  }
}
```

### Broadcast Announcement
```bash
POST /api/communications/broadcast

Body:
{
  "type": "launch|update|milestone|deployment",
  "data": {
    "title": "Announcement Title",
    "description": "Announcement description",
    "version": "v1.0.0",
    "date": "2024-01-01T00:00:00Z",
    "url": "https://...",
    "features": ["Feature 1", "Feature 2"]
  }
}
```

### Launch Announcement
```bash
POST /api/communications/launch

Body:
{
  "title": "Quantum Pi Forge v2.0 Launch",
  "description": "Major new release with enhanced features",
  "version": "v2.0.0",
  "date": "2024-01-01T00:00:00Z",
  "url": "https://github.com/onenoly1010/pi-forge-quantum-genesis/releases",
  "features": [
    "Enhanced quantum resonance patterns",
    "Improved WebSocket streaming",
    "New ethical audit framework"
  ]
}
```

### Feature Update
```bash
POST /api/communications/update

Body:
{
  "title": "Enhanced Evaluation System",
  "description": "New AI evaluation framework with advanced metrics",
  "benefits": [
    "Faster processing",
    "Better accuracy",
    "Enhanced reporting"
  ],
  "url": "https://docs.example.com/updates"
}
```

### Milestone Achievement
```bash
POST /api/communications/milestone

Body:
{
  "title": "10,000 Deployments Milestone",
  "description": "Successfully reached 10,000 production deployments",
  "achievement": "Community growth milestone achieved",
  "stats": {
    "Total Deployments": "10,000",
    "Active Users": "5,000",
    "Success Rate": "99.9%"
  }
}
```

### Deployment Notification
```bash
POST /api/communications/deployment

Body:
{
  "environment": "production",
  "version": "v1.2.3",
  "duration": "3m 45s",
  "url": "https://pi-forge-quantum-genesis.up.railway.app"
}
```

## ⚙️ GitHub Actions Integration

The Press Agent automatically triggers on:

1. **GitHub Releases** - When a new release is published
2. **Successful Deployments** - After deploy workflows complete
3. **Manual Triggers** - Via workflow_dispatch

### Manual Announcement Workflow

1. Go to **Actions** → **Press Agent - Automated Communications**
2. Click **Run workflow**
3. Select announcement type (launch/update/milestone/deployment)
4. Fill in title, description, and optional version
5. Click **Run workflow**

The announcement will be broadcast to all configured channels.

## 📝 Contributor Announcement Submission

Contributors can submit draft announcements for review:

### Method 1: GitHub Issue

1. Create a new issue with template "Press Release Request"
2. Fill in the announcement details
3. Label with `press-agent` and `announcement`
4. Press Agent will review and broadcast approved announcements

### Method 2: Direct API

```bash
curl -X POST http://localhost:3001/api/communications/broadcast \
  -H "Content-Type: application/json" \
  -d '{
    "type": "update",
    "data": {
      "title": "Your Announcement",
      "description": "Description here",
      "url": "https://..."
    }
  }'
```

## 📊 Communication Dashboard

The Press Agent provides a public dashboard for transparency:

**URL:** `http://localhost:3001/dashboard` (when implemented)

**Features:**
- Real-time announcement log
- Platform status indicators
- Delivery success metrics
- Recent broadcasts history
- Scheduled announcements queue

## 🔍 Monitoring & Logs

### View Press Agent Logs

```bash
# Development
npm run dev

# Production logs
tail -f logs/press-agent.log
```

### Check Communication Status

```bash
curl http://localhost:3001/api/communications/status | jq
```

### Monitor Broadcast Results

All broadcasts return a results object:
```json
{
  "success": true,
  "results": {
    "discord": true,
    "twitter": true,
    "telegram": true,
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

## 🛡️ Security & Permissions

### Required Secrets (GitHub Actions)

Add these secrets to your repository:

1. `DISCORD_WEBHOOK_URL` - Discord webhook for announcements
2. `TWITTER_BEARER_TOKEN` - Twitter API bearer token
3. `TELEGRAM_BOT_TOKEN` - Telegram bot token
4. `TELEGRAM_CHAT_ID` - Telegram chat/channel ID

### Access Control

- Press Agent API should be behind authentication in production
- Use environment variables for all credentials
- Never commit credentials to git
- Rotate tokens regularly
- Monitor for unauthorized access

## 🔄 Continuous Operation

The Press Agent operates autonomously:

1. **GitHub Events** trigger automatic workflows
2. **Workflows** call Press Agent API endpoints
3. **Press Agent** broadcasts to all platforms
4. **Results** are logged for transparency
5. **Community** is updated in real-time

No manual intervention required for routine announcements.

## 📋 Communication Plan

### Short-Term (OINIO Launch)

- [ ] Launch announcement across all platforms
- [ ] Daily progress updates
- [ ] Critical milestone notifications
- [ ] Community engagement posts

### Medium-Term (Weekly Updates)

- [ ] Weekly feature highlights
- [ ] Community showcase
- [ ] Development progress
- [ ] Governance decisions

### Long-Term (Continuous Improvement)

- [ ] Automated weekly digests
- [ ] Monthly community reports
- [ ] Quarterly milestone reviews
- [ ] Annual ecosystem updates

## 🤝 Contributing

To improve the Press Agent:

1. Fork the repository
2. Make changes in `press-agent/` directory
3. Test with `npm test`
4. Submit PR with description
5. Press Agent will announce merged improvements

## 📞 Support

**Issues:** [GitHub Issues](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues)  
**Discussions:** [GitHub Discussions](https://github.com/onenoly1010/pi-forge-quantum-genesis/discussions)  
**Discord:** Link in repository README

---

*The Press Agent embodies the Canon of Autonomy - operating transparently, independently, and for the benefit of the entire Quantum Pi Forge community.*
