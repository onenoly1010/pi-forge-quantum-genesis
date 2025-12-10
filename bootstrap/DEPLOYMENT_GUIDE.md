# 🚀 Deployment Guide

Complete guide for deploying Quantum Pi Forge to production.

## Prerequisites

Before deploying, ensure you have:

- ✅ Completed bootstrap process (`./bootstrap/bootstrap.sh`)
- ✅ Configured `.env` with production credentials
- ✅ Run and passed all tests
- ✅ Chosen a deployment platform

## Deployment Options

### Option 1: Railway (Recommended)

Railway provides automatic deployments from GitHub with zero-config.

#### Step 1: Install Railway CLI

```bash
npm i -g @railway/cli
```

#### Step 2: Login to Railway

```bash
railway login
```

#### Step 3: Create New Project

```bash
# Option A: Link existing project
railway link

# Option B: Create new project
railway init
```

#### Step 4: Set Environment Variables

```bash
# Set required variables
railway variables set SUPABASE_URL="https://your-project.supabase.co"
railway variables set SUPABASE_KEY="your-anon-key"
railway variables set JWT_SECRET="$(openssl rand -hex 32)"

# Set optional variables
railway variables set ENVIRONMENT="production"
railway variables set LOG_LEVEL="INFO"
```

#### Step 5: Deploy

```bash
# Deploy current directory
railway up

# Or link to GitHub for automatic deployments
railway link
# Push to GitHub, Railway auto-deploys
```

#### Step 6: Verify Deployment

```bash
# Get deployment URL
railway domain

# Check logs
railway logs

# Test health endpoint
curl https://your-app.up.railway.app/health
```

### Option 2: Docker Deployment

Deploy using Docker containers for maximum portability.

#### Step 1: Build Image

```bash
# Build production image
docker build -t quantum-pi-forge:latest .

# Or use multi-stage build for development
docker build --target development -t quantum-pi-forge:dev .
```

#### Step 2: Run Container

```bash
# Run with .env file
docker run -d \
  --name quantum-pi-forge \
  -p 8000:8000 \
  --env-file .env \
  quantum-pi-forge:latest

# Or specify environment variables
docker run -d \
  --name quantum-pi-forge \
  -p 8000:8000 \
  -e SUPABASE_URL="https://your-project.supabase.co" \
  -e SUPABASE_KEY="your-anon-key" \
  -e JWT_SECRET="your-secret" \
  quantum-pi-forge:latest
```

#### Step 3: Verify Container

```bash
# Check container status
docker ps

# View logs
docker logs quantum-pi-forge -f

# Test health endpoint
curl http://localhost:8000/health
```

#### Step 4: Docker Compose (All Services)

```bash
# Copy template
cp bootstrap/templates/docker-compose.yml.template docker-compose.yml

# Edit configuration
nano docker-compose.yml

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Option 3: Manual Deployment

Deploy directly on a server without containers.

#### Step 1: Prepare Server

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3-pip nginx

# Configure firewall
sudo ufw allow 8000
sudo ufw allow 80
sudo ufw allow 443
```

#### Step 2: Clone and Bootstrap

```bash
# Clone repository
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis

# Run bootstrap
./bootstrap/bootstrap.sh --environment production
```

#### Step 3: Configure Environment

```bash
# Edit .env with production values
nano .env

# Secure the file
chmod 600 .env
```

#### Step 4: Install as System Service

Create systemd service file:

```bash
sudo nano /etc/systemd/system/quantum-pi-forge.service
```

Add content:

```ini
[Unit]
Description=Quantum Pi Forge FastAPI Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/pi-forge-quantum-genesis
Environment="PATH=/path/to/pi-forge-quantum-genesis/.venv/bin"
ExecStart=/path/to/pi-forge-quantum-genesis/.venv/bin/uvicorn server.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable quantum-pi-forge
sudo systemctl start quantum-pi-forge
sudo systemctl status quantum-pi-forge
```

#### Step 5: Configure Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/quantum-pi-forge
```

Add configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/quantum-pi-forge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 6: Setup SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

## Environment Configuration

### Production Environment Variables

```env
# Required
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-production-anon-key
JWT_SECRET=<generate-with-openssl-rand-hex-32>

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
NODE_ENV=production

# Service Ports (Railway sets PORT automatically)
PORT=8000
FASTAPI_PORT=8000
FLASK_PORT=5000
GRADIO_PORT=7860

# Security
CORS_ORIGINS=https://your-domain.com
SESSION_SECRET=<another-secure-random-string>
SESSION_TIMEOUT=3600

# Optional: Tracing
QUANTUM_TRACING_ENABLED=true
OTLP_ENDPOINT=http://otel-collector:4318
TRACE_SAMPLE_RATE=0.1

# Optional: Pi Network
PI_NETWORK_MODE=mainnet
PI_NETWORK_APP_ID=your-app-id
PI_NETWORK_API_KEY=your-api-key
```

### Generating Secure Secrets

```bash
# JWT Secret
openssl rand -hex 32

# Session Secret
openssl rand -base64 32

# API Keys
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Post-Deployment

### 1. Verify Health Endpoints

```bash
# FastAPI
curl https://your-domain.com/health

# Expected response
{
  "status": "healthy",
  "service": "FastAPI Quantum Conduit",
  "timestamp": "2024-12-10T22:00:00Z"
}
```

### 2. Test Authentication

```bash
# Register test user
curl -X POST https://your-domain.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Login
curl -X POST https://your-domain.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

### 3. Test WebSocket

```javascript
// Browser console
const ws = new WebSocket('wss://your-domain.com/ws/collective-insight?token=<jwt-token>');
ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => console.log('Message:', e.data);
```

### 4. Monitor Logs

```bash
# Railway
railway logs -f

# Docker
docker logs -f quantum-pi-forge

# Systemd
sudo journalctl -u quantum-pi-forge -f
```

### 5. Setup Monitoring

See [Autonomous Operations Guide](docs/AUTONOMOUS_OPERATIONS.md) for:
- GitHub Actions monitoring
- Scheduled health checks
- Automatic rollbacks
- Status tracking

## Production Best Practices

### Security

1. **Use HTTPS** - Always use SSL/TLS in production
2. **Secure secrets** - Never commit secrets to Git
3. **Rotate keys** - Change credentials regularly
4. **Rate limiting** - Implement rate limiting on APIs
5. **CORS configuration** - Restrict to known domains
6. **Input validation** - Validate all user inputs
7. **SQL injection** - Use parameterized queries
8. **XSS protection** - Sanitize outputs

### Performance

1. **Use workers** - Multiple uvicorn workers (`--workers 4`)
2. **Enable caching** - Cache frequent requests
3. **Database indexing** - Index frequently queried fields
4. **CDN** - Use CDN for static assets
5. **Compression** - Enable gzip compression
6. **Connection pooling** - Pool database connections

### Reliability

1. **Health checks** - Implement comprehensive health endpoints
2. **Graceful shutdown** - Handle SIGTERM properly
3. **Auto-restart** - Configure service auto-restart
4. **Backup database** - Regular database backups
5. **Monitoring** - Set up alerts for failures
6. **Load balancing** - Use multiple instances

### Scaling

1. **Horizontal scaling** - Add more instances
2. **Database optimization** - Optimize queries
3. **Async operations** - Use async/await properly
4. **Background tasks** - Use task queues for heavy work
5. **Caching layer** - Add Redis for caching
6. **CDN** - Distribute static content

## Troubleshooting

### Deployment Fails

```bash
# Check logs
railway logs  # Railway
docker logs quantum-pi-forge  # Docker
sudo journalctl -u quantum-pi-forge -n 100  # Systemd

# Verify environment variables
railway variables  # Railway
docker exec quantum-pi-forge env  # Docker
sudo systemctl show quantum-pi-forge | grep Environment  # Systemd

# Test locally first
./bootstrap/start-services.sh
```

### Health Check Fails

```bash
# Check if service is running
curl -v http://localhost:8000/health

# Check logs for errors
tail -f logs/*.log

# Verify database connection
python -c "from supabase import create_client; import os; client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')); print('OK')"
```

### High Memory Usage

```bash
# Check memory usage
docker stats  # Docker
htop  # Linux

# Reduce workers
uvicorn server.main:app --workers 2

# Optimize code
# - Use generators
# - Clear unused objects
# - Profile with memory_profiler
```

### Slow Response Times

```bash
# Profile application
python -m cProfile -o profile.stats server/main.py

# Analyze
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"

# Add caching
# - Redis for session data
# - CDN for static files
# - Database query caching
```

## Rollback Procedure

If deployment fails:

### Railway

```bash
# Railway auto-deploys from Git
# Rollback by reverting Git commit
git revert HEAD
git push
```

### Docker

```bash
# Stop current container
docker stop quantum-pi-forge

# Run previous version
docker run -d \
  --name quantum-pi-forge \
  -p 8000:8000 \
  --env-file .env \
  quantum-pi-forge:previous-tag
```

### Manual

```bash
# Stop service
sudo systemctl stop quantum-pi-forge

# Checkout previous version
git checkout <previous-commit>

# Restart service
sudo systemctl start quantum-pi-forge
```

## Continuous Deployment

### GitHub Actions (Automated)

The repository includes `.github/workflows/ai-agent-handoff-runbook.yml` which:

1. Runs tests on push
2. Builds deployment package
3. Deploys to production
4. Monitors health
5. Rolls back on failure

See [Autonomous Operations](docs/AUTONOMOUS_OPERATIONS.md) for details.

### Manual CD Setup

```bash
# Railway with GitHub integration
railway link
# Auto-deploys on push to main

# Docker with webhooks
# Set up webhook to trigger build on push
# See your platform documentation
```

## Support

Need help with deployment?

1. Check the [Bootstrap README](README.md)
2. Review deployment logs
3. Consult platform documentation:
   - [Railway Docs](https://docs.railway.app)
   - [Docker Docs](https://docs.docker.com)
4. Open a GitHub issue
5. Contact repository maintainer

---

**🎉 Your Quantum Resonance Lattice is now in production!**
