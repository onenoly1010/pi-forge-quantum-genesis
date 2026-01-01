# Press Agent - Quick Start for Repository Admin

## ⚡ Immediate Actions Required

The Press Agent has been fully implemented. To activate it, you need to:

### 1. Configure Bot Credentials (15 minutes)

#### Discord Setup
1. Go to your Discord server
2. Server Settings → Integrations → Webhooks
3. Create new webhook, name it "Quantum Pi Forge Press Agent"
4. Copy the webhook URL
5. Save for next step

#### Twitter Setup (Optional but Recommended)
1. Visit https://developer.twitter.com/en/portal/dashboard
2. Create new app or use existing
3. Apply for Elevated Access (required for posting)
4. Generate Bearer Token
5. Save for next step

#### Telegram Setup (Optional but Recommended)
1. Open Telegram, search for @BotFather
2. Send `/newbot` and follow prompts
3. Name: "Quantum Pi Forge Press Agent"
4. Username: something ending in "bot"
5. Copy the bot token
6. Send a test message to your bot
7. Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
8. Find and copy your chat ID
9. Save both for next step

**Detailed instructions:** See `press-agent/BOT_SETUP_GUIDE.md`

### 2. Add GitHub Secrets (5 minutes)

1. Go to: https://github.com/onenoly1010/pi-forge-quantum-genesis/settings/secrets/actions
2. Click "New repository secret"
3. Add these secrets:

```
Name: DISCORD_WEBHOOK_URL
Value: [Your Discord webhook URL from step 1]

Name: TWITTER_BEARER_TOKEN  (optional)
Value: [Your Twitter bearer token from step 1]

Name: TELEGRAM_BOT_TOKEN  (optional)
Value: [Your Telegram bot token from step 1]

Name: TELEGRAM_CHAT_ID  (optional)
Value: [Your Telegram chat ID from step 1]
```

### 3. Deploy Press Agent Service (10 minutes)

#### Option A: Railway
1. Create new Railway project
2. Add service from GitHub repo
3. Select `press-agent` directory
4. Add environment variables (same as secrets above)
5. Set `PRESS_AGENT_PORT=3001`
6. Deploy

#### Option B: Local Testing First
```bash
cd press-agent
cp .env.example .env
# Edit .env with your bot credentials
npm install
npm start
```

Then test:
```bash
curl http://localhost:3001/health
curl http://localhost:3001/api/communications/status
```

### 4. Test the Integration (5 minutes)

Once deployed, run a manual test:

1. Go to: Actions → Press Agent - Automated Communications
2. Click "Run workflow"
3. Fill in:
   - Type: `update`
   - Title: `Press Agent Test`
   - Description: `Testing the Press Agent system`
4. Run workflow
5. Check Discord/Twitter/Telegram for the announcement

---

## 📚 Complete Documentation

All documentation is in `press-agent/` directory:

- **OPERATIONS_GUIDE.md** - How to use the Press Agent
- **BOT_SETUP_GUIDE.md** - Detailed setup instructions (recommended read)
- **COMMUNICATION_PLAN.md** - What the Press Agent will do
- **PRESS_AGENT_REPORT.md** - Full technical report

---

## 🆘 Quick Troubleshooting

**Problem:** Secrets not working in GitHub Actions
- **Solution:** Make sure secret names match exactly (case-sensitive)

**Problem:** Discord messages not appearing
- **Solution:** Check webhook URL is correct, test with curl first

**Problem:** Twitter not posting
- **Solution:** Ensure Elevated Access is approved, check token

**Problem:** Telegram not working
- **Solution:** Make sure you sent a message to bot first, verify chat ID

---

## ✅ Success Criteria

You'll know it's working when:
- ✅ GitHub Actions workflow runs without errors
- ✅ Test announcement appears in configured channels
- ✅ Status endpoint shows all channels as enabled
- ✅ No errors in Press Agent logs

---

## 🎯 After Activation

Once working:
1. Announce Press Agent activation to community
2. Share submission guidelines
3. Monitor first few automated announcements
4. Adjust configuration as needed

---

**Need help?** Check the detailed guides in `press-agent/` directory or create an issue with the `press-agent` label.

**Ready to activate?** Start with step 1 above. Estimated total time: 30-45 minutes.
