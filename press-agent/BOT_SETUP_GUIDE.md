# 🔑 Press Agent Bot Setup Guide

This guide walks you through setting up all bot integrations for the Quantum Pi Forge Press Agent.

## 📋 Prerequisites

- Admin access to Discord server (for webhook creation)
- Twitter/X Developer Account (for API access)
- Telegram account (for bot creation)
- GitHub repository admin access (for secrets)

---

## 🟦 Discord Bot Setup

### Step 1: Create Webhook

1. Open your Discord server
2. Click on server name → **Server Settings**
3. Navigate to **Integrations** → **Webhooks**
4. Click **Create Webhook** or **New Webhook**
5. Configure the webhook:
   - **Name:** Quantum Pi Forge Press Agent
   - **Channel:** Select your announcements channel
   - **Avatar:** (Optional) Upload a logo
6. Click **Copy Webhook URL**

### Step 2: Add to Environment

Add to your `.env` file:
```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz
```

### Step 3: Test

```bash
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "🌌 Press Agent Test - Discord Integration Working!"
  }'
```

You should see the message appear in your Discord channel.

### Webhook Security

- Never share your webhook URL publicly
- Rotate webhooks if compromised
- Create separate webhooks for different environments (dev/prod)

---

## 🐦 Twitter/X Bot Setup

### Step 1: Create Developer Account

1. Visit [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Sign in with your Twitter account
3. Apply for **Elevated Access** (required for posting)
4. Wait for approval (usually 1-2 days)

### Step 2: Create App

1. In Developer Portal, click **+ Create Project**
2. Fill in project details:
   - **Project Name:** Quantum Pi Forge Press Agent
   - **Use Case:** Informing your audience
   - **Project Description:** Automated announcements for Quantum Pi Forge ecosystem
3. Click **Create**

### Step 3: Generate Credentials

#### Option A: Bearer Token (Recommended)

1. In your app settings, go to **Keys and tokens**
2. Under **Authentication Tokens**, click **Generate** for Bearer Token
3. Copy the token immediately (shown only once)

Add to `.env`:
```bash
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAA...
```

#### Option B: OAuth 1.0a (Full Access)

1. In **Keys and tokens**, generate:
   - API Key and Secret
   - Access Token and Secret
2. Copy all four values

Add to `.env`:
```bash
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
```

### Step 4: Configure App Permissions

1. Go to **Settings** → **User authentication settings**
2. Set **App permissions** to **Read and write**
3. Save changes

### Step 5: Test

```bash
# The Press Agent will log test tweets in development mode
# In production, tweets will actually post
npm start
```

Then test via API:
```bash
curl -X POST http://localhost:3001/api/communications/update \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Update",
    "description": "Testing Twitter integration",
    "benefits": ["Feature 1", "Feature 2"]
  }'
```

### Twitter API Limits

- **Free Tier:** 500 tweets/month
- **Basic Tier ($100/month):** 3,000 tweets/month
- **Rate Limits:** 300 requests/15 min
- Implement rate limiting in production

---

## 📱 Telegram Bot Setup

### Step 1: Create Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Start a chat and send `/newbot`
3. Follow prompts:
   - **Bot Name:** Quantum Pi Forge Press Agent
   - **Username:** quantumpiforge_press_bot (must end in 'bot')
4. Copy the **HTTP API token** provided

### Step 2: Get Chat ID

#### Option A: For Direct Messages

1. Send a message to your new bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for `"chat":{"id":123456789}`
4. Copy the chat ID

#### Option B: For Channels

1. Add your bot as an admin to the channel
2. Send a message in the channel
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for the channel chat ID (starts with `-100`)

### Step 3: Add to Environment

Add to `.env`:
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
TELEGRAM_CHAT_ID=123456789
```

For channels, use the channel ID:
```bash
TELEGRAM_CHAT_ID=-1001234567890
```

### Step 4: Test

```bash
curl -X POST http://localhost:3001/api/communications/milestone \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Milestone",
    "description": "Testing Telegram integration",
    "achievement": "Bot is working!"
  }'
```

You should receive a formatted message on Telegram.

### Telegram Bot Settings

Configure your bot with BotFather:

```
/setdescription - Set bot description
/setabouttext - Set about text
/setuserpic - Set profile photo
/setcommands - Set bot commands
```

Recommended commands:
```
status - Check Press Agent status
help - Get help and documentation
latest - View latest announcements
```

---

## 🔐 GitHub Secrets Configuration

### Step 1: Navigate to Repository Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

### Step 2: Add Required Secrets

Add each of these secrets:

1. **DISCORD_WEBHOOK_URL**
   - Value: Your Discord webhook URL
   - Used by: Press Agent workflow

2. **TWITTER_BEARER_TOKEN**
   - Value: Your Twitter bearer token
   - Used by: Press Agent workflow

3. **TELEGRAM_BOT_TOKEN**
   - Value: Your Telegram bot token
   - Used by: Press Agent workflow

4. **TELEGRAM_CHAT_ID**
   - Value: Your Telegram chat ID
   - Used by: Press Agent workflow

### Step 3: Verify Secrets

Run the Press Agent workflow manually to test:

1. Go to **Actions** → **Press Agent - Automated Communications**
2. Click **Run workflow**
3. Fill in test announcement details
4. Check if announcement appears on all platforms

---

## 🧪 Testing Your Setup

### Complete Integration Test

1. **Start Press Agent locally:**
   ```bash
   cd press-agent
   npm start
   ```

2. **Check status:**
   ```bash
   curl http://localhost:3001/api/communications/status | jq
   ```

   Expected output:
   ```json
   {
     "success": true,
     "status": {
       "discord": { "enabled": true, "configured": true },
       "twitter": { "enabled": true, "configured": true },
       "telegram": { "enabled": true, "configured": true }
     }
   }
   ```

3. **Send test broadcast:**
   ```bash
   curl -X POST http://localhost:3001/api/communications/broadcast \
     -H "Content-Type: application/json" \
     -d '{
       "type": "update",
       "data": {
         "title": "Press Agent Activated",
         "description": "All communication systems operational",
         "benefits": ["Discord ✅", "Twitter ✅", "Telegram ✅"]
       }
     }' | jq
   ```

4. **Verify on all platforms:**
   - Check Discord channel for embed
   - Check Twitter for tweet
   - Check Telegram for message

### GitHub Actions Test

1. Go to repository **Actions**
2. Select **Press Agent - Automated Communications**
3. Click **Run workflow**
4. Use these test values:
   - Type: `update`
   - Title: `Press Agent System Check`
   - Description: `Testing automated GitHub Actions integration`
   - Version: `test-v1.0.0`
5. Click **Run workflow**
6. Wait for completion
7. Check all platforms for announcement

---

## 🔧 Troubleshooting

### Discord Issues

**Problem:** Webhook returns 404
- **Solution:** Webhook URL may be invalid. Create new webhook.

**Problem:** Messages don't appear
- **Solution:** Check webhook channel permissions.

### Twitter Issues

**Problem:** 401 Unauthorized
- **Solution:** Regenerate tokens, ensure Elevated Access approved.

**Problem:** 403 Forbidden
- **Solution:** Check app permissions (Read and Write required).

**Problem:** Rate limit exceeded
- **Solution:** Implement rate limiting, upgrade API tier.

### Telegram Issues

**Problem:** Bot token invalid
- **Solution:** Check for spaces/newlines in token, regenerate if needed.

**Problem:** Chat not found
- **Solution:** Ensure you've sent a message to bot first.

**Problem:** Can't send to channel
- **Solution:** Bot must be admin of the channel.

### General Issues

**Problem:** Environment variables not loaded
- **Solution:** 
  ```bash
  # Check if .env exists
  ls -la press-agent/.env
  
  # Verify variables are set
  cd press-agent
  node -e "require('dotenv').config(); console.log(process.env)"
  ```

**Problem:** Dependencies not installed
- **Solution:**
  ```bash
  cd press-agent
  rm -rf node_modules package-lock.json
  npm install
  ```

---

## 📊 Verification Checklist

Use this checklist to ensure everything is configured correctly:

### Discord
- [ ] Webhook created in server
- [ ] Webhook URL added to `.env`
- [ ] Test message sent successfully
- [ ] Secret added to GitHub

### Twitter
- [ ] Developer account approved
- [ ] App created with correct permissions
- [ ] Bearer token or OAuth credentials generated
- [ ] Credentials added to `.env`
- [ ] Test tweet logged successfully
- [ ] Secret added to GitHub

### Telegram
- [ ] Bot created with BotFather
- [ ] Bot token obtained
- [ ] Chat ID obtained (via getUpdates)
- [ ] Bot added to channel (if using channel)
- [ ] Credentials added to `.env`
- [ ] Test message sent successfully
- [ ] Secrets added to GitHub

### Press Agent
- [ ] All dependencies installed
- [ ] Server starts without errors
- [ ] Status endpoint shows all enabled
- [ ] Test broadcast succeeds on all platforms
- [ ] GitHub Actions workflow runs successfully
- [ ] Automated announcements working

---

## 🚀 Going Live

Once all tests pass:

1. **Update production environment variables** on your hosting platform
2. **Enable auto-broadcast** in Press Agent configuration
3. **Create announcement schedule** for regular updates
4. **Document credentials** in secure password manager
5. **Set up monitoring** for failed broadcasts
6. **Brief team** on submission process
7. **Announce Press Agent activation** to community

---

## 🔄 Maintenance

### Regular Tasks

**Weekly:**
- Check broadcast success rate
- Review API usage/rate limits
- Monitor error logs

**Monthly:**
- Rotate credentials (security best practice)
- Review and update announcement templates
- Check for bot API updates

**Quarterly:**
- Audit access permissions
- Review communication strategy
- Update documentation

### Credential Rotation

When rotating credentials:

1. Generate new credentials
2. Update `.env` file
3. Update GitHub Secrets
4. Test thoroughly
5. Update production environment
6. Deactivate old credentials
7. Document rotation date

---

## 📚 Additional Resources

- [Discord Webhook Documentation](https://discord.com/developers/docs/resources/webhook)
- [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Press Agent Operations Guide](./OPERATIONS_GUIDE.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

*Need help? Create an issue with the `press-agent` label and our team will assist.*
