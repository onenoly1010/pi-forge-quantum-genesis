# 🆘 Troubleshooting - Common Issues & Solutions

**Last Updated**: December 2025

Solutions to common issues across the Quantum Pi Forge ecosystem.

---

## 🔧 Installation Issues

### "Module not found"
```bash
# Reinstall dependencies
pip install --force-reinstall -r server/requirements.txt
```

### "Port already in use"
```bash
# Find process
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Use different port
uvicorn server.main:app --port 8001
```

---

## 🗄️ Database Issues

### Connection Failed
```bash
# Check DATABASE_URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Verify Supabase credentials
curl $SUPABASE_URL/rest/v1/ \
  -H "apikey: $SUPABASE_KEY"
```

### Migration Errors
```bash
# Re-run migrations
psql $DATABASE_URL < supabase_migrations/001_payments_schema.sql

# Check table existence
psql $DATABASE_URL -c "\dt"
```

---

## 💰 Pi Network Issues

### "PI_NETWORK_API_KEY not set"
```bash
# Set in Railway
railway variables set PI_NETWORK_API_KEY=your-key

# Set locally
export PI_NETWORK_API_KEY=your-key
```

### "Invalid webhook signature"
- Verify `PI_NETWORK_WEBHOOK_SECRET` matches Pi Portal
- Ensure webhook URL is HTTPS
- Check webhook configuration in Pi Developer Portal

### Payment Not Processing
```bash
# Check Pi Network status
curl https://your-app/api/pi-network/status

# Review logs
railway logs | grep "payment"

# Verify webhook endpoint
curl -X POST https://your-app/api/pi-webhooks/payment \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

---

## 🚀 Deployment Issues

### Build Failures
- Check build logs in Railway/Vercel dashboard
- Verify `requirements.txt` is complete
- Ensure Python version compatibility (3.11+)

### Health Check Failing
```bash
# Test locally
curl http://localhost:8000/health

# Test production
curl https://your-app.railway.app/health

# Check logs
railway logs --follow
```

### Environment Variables Missing
```bash
# List variables
railway variables

# Set missing variable
railway variables set KEY=value
```

---

## ⚡ Performance Issues

### Slow Response Times
- Check database query performance
- Review logs for bottlenecks
- Monitor resource usage in platform dashboard
- Consider scaling resources

### High Memory Usage
- Check for memory leaks
- Review Docker container limits
- Optimize database queries
- Use connection pooling

---

## 🔒 Security Issues

### JWT Token Expired
```bash
# Refresh token
POST /api/auth/refresh
{
  "refresh_token": "your_refresh_token"
}
```

### CORS Errors
- Verify allowed origins in configuration
- Check request headers
- Ensure preflight requests handled

---

## 🧪 Testing Issues

### Tests Failing
```bash
# Run with verbose output
pytest -vv

# Run specific test
pytest tests/test_api.py::test_health -v

# Disable telemetry for tests
ENABLE_TELEMETRY=false pytest
```

### Coverage Too Low
```bash
# Generate coverage report
pytest --cov=server --cov-report=html

# Open report
open htmlcov/index.html
```

---

## 📱 Frontend Issues

### Assets Not Loading
- Check `public/` directory exists
- Verify build command ran
- Check network tab in browser devtools

### API Calls Failing
- Verify base URL configuration
- Check CORS headers
- Review network requests in devtools

---

## 🆘 Emergency Procedures

### System Down
1. Check health endpoint
2. Review logs
3. Restart service
4. Notify guardians if needed

### Data Loss Suspected
1. Stop all operations immediately
2. Contact lead guardian
3. Review backup status
4. Document incident

### Security Breach
1. Execute emergency stop
2. Contact lead guardian immediately
3. Isolate affected systems
4. Document timeline
5. Review audit logs

---

## 📞 Getting Help

### Resources

- [[Runbook Index]] - Operational procedures
- [[Deployment Guide]] - Deployment help
- [[API Reference]] - API documentation
- [[For Developers]] - Development guide

### Support Channels

- **GitHub Issues**: [Open issue](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues)
- **Documentation**: Browse this wiki
- **Contact**: @onenoly1010

---

## See Also

- [[Runbook Index]] - Operational commands
- [[Deployment Guide]] - Deployment procedures
- [[Monitoring Observability]] - Monitoring setup
- [[For Guardians]] - Guardian procedures

---

[[Home]] | [[Runbook Index]] | [[For Developers]]
