# 📦 Pi Forge Quantum Genesis - Installation Guide

Complete installation and setup instructions for Pi Forge Quantum Genesis.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- **Operating System**: Linux, macOS, or Windows 10+
- **Python**: 3.11 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB free space
- **Internet**: Required for dependency installation

### Optional Requirements

- **Redis**: For production-grade real-time features
- **Supabase Account**: For database persistence
- **Docker**: For containerized deployment

## Installation Methods

### Method 1: Local Python Installation (Recommended for Development)

#### Step 1: Clone the Repository

```bash
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis
```

#### Step 2: Set Up Python Environment

```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### Step 3: Install Server Dependencies

```bash
cd server
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Copy the example below or create your own
cat > .env << EOF
SECRET_KEY=pi-forge-kris-olofson-2024
PORT=5000
REDIS_URL=redis://localhost:6379
SUPABASE_URL=
SUPABASE_KEY=
EOF
```

#### Step 5: Start the Application

```bash
python server/app.py
```

The application will be available at `http://localhost:5000`

### Method 2: Docker Installation

#### Step 1: Install Docker

Follow instructions at https://docs.docker.com/get-docker/

#### Step 2: Build the Image

```bash
cd pi-forge-quantum-genesis
docker build -t pi-forge .
```

#### Step 3: Run the Container

```bash
docker run -p 8080:8080 \
  -e SECRET_KEY=your-secret-key \
  -e PORT=8080 \
  pi-forge
```

Access at `http://localhost:8080`

### Method 3: Production Deployment

#### Railway Deployment

1. Fork the repository to your GitHub account
2. Sign up at https://railway.app
3. Create a new project from your GitHub repository
4. Add environment variables in Railway dashboard
5. Deploy automatically

#### Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | No | `pi-forge-kris-olofson-2024` | JWT signing key |
| `PORT` | No | `5000` | Application port |
| `REDIS_URL` | No | `redis://localhost:6379` | Redis connection URL |
| `SUPABASE_URL` | No | - | Supabase project URL |
| `SUPABASE_KEY` | No | - | Supabase anon key |

### Database Setup (Optional)

If using Supabase:

1. Create account at https://supabase.com
2. Create a new project
3. Run these SQL commands in Supabase SQL Editor:

```sql
-- Create leaderboard table
CREATE TABLE leaderboard (
  user_id TEXT PRIMARY KEY,
  digits_mined INTEGER DEFAULT 0,
  last_active TIMESTAMP DEFAULT NOW()
);

-- Create stakes table
CREATE TABLE stakes (
  id SERIAL PRIMARY KEY,
  user_id TEXT NOT NULL,
  amount NUMERIC NOT NULL,
  start_time TIMESTAMP DEFAULT NOW(),
  apy NUMERIC DEFAULT 0.055
);
```

4. Copy URL and Key to `.env` file

### Redis Setup (Optional)

For production WebSocket features:

```bash
# Install Redis
# On Ubuntu/Debian:
sudo apt-get install redis-server

# On macOS:
brew install redis

# Start Redis
redis-server
```

## Verification

### Step 1: Run Verification Script

```bash
cd /path/to/pi-forge-quantum-genesis
python verify.py
```

This script will:
- ✅ Check Python version
- ✅ Verify dependencies installed
- ✅ Test server endpoints
- ✅ Validate configuration
- ✅ Check database connectivity (if configured)

### Step 2: Manual Testing

1. **Server Status**:
   ```bash
   curl http://localhost:5000/
   ```
   Should return JSON with status information

2. **Health Check**:
   ```bash
   curl http://localhost:5000/health
   ```
   Should return healthy status

3. **Compute Pi**:
   ```bash
   curl http://localhost:5000/compute/10
   ```
   Should return Pi computation result

4. **Frontend**: Open `http://localhost:5000` in browser

### Step 3: Test Authentication

```bash
# Login request
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pi-forge.com","password":"quantum2024"}'

# Use returned token for protected routes
curl http://localhost:5000/api/protected-route \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Troubleshooting

### Common Issues

#### Issue: "Module not found" error

**Solution**: Ensure you're in the virtual environment and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r server/requirements.txt
```

#### Issue: "Port already in use"

**Solution**: Change the port or kill the process:
```bash
# Change port
export PORT=5001
python server/app.py

# Or kill process on Linux/macOS
lsof -ti:5000 | xargs kill -9
```

#### Issue: WebSocket connection fails

**Solution**: 
1. Ensure Redis is running (if using REDIS_URL)
2. Or comment out Redis configuration to use default in-memory queue
3. Check CORS settings match your frontend origin

#### Issue: Database errors

**Solution**:
1. Verify Supabase credentials in `.env`
2. Check tables exist in Supabase dashboard
3. Application works without database (features limited)

### Getting Help

1. Check existing issues: https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
2. Review logs: Look for error messages in console output
3. Verify configuration: Double-check `.env` file settings

## Next Steps

After successful installation:

1. Review the [README.md](README.md) for feature overview
2. Explore API endpoints at `http://localhost:5000/`
3. Open frontend at `http://localhost:5000/` (if served)
4. Check the leaderboard and try mining some Pi digits
5. Configure production settings for deployment

---

**Installation complete! Welcome to Pi Forge Quantum Genesis** 🚀
