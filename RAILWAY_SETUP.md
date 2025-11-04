# Railway Deployment Setup Guide

## 🎯 Quick Deployment Options

This repository now supports **THREE** deployment methods for Railway. Choose the one that works best:

---

## ✅ **Option 1: Automatic Detection (Recommended)**

Railway will automatically detect and use one of these files:
- `Procfile` (for Heroku-style deployment)
- `Dockerfile` (for containerized deployment)
- `railway.json` (for explicit Railway configuration)

**Just push to Railway and it will work!** 🚀

---

## ✅ **Option 2: Railway Native Build (Manual Settings)**

If automatic detection fails, configure these in **Railway Dashboard → Settings → Deploy**:

### Build Command:
```bash
cd backend && pip install -r requirements.txt
```

### Start Command:
```bash
cd backend && python -m gunicorn -w 2 -k gevent -b 0.0.0.0:$PORT app:app
```

---

## ✅ **Option 3: Dockerfile Deployment**

The repository includes an optimized Dockerfile at the root:
- Uses Python 3.11-slim
- Optimized layer caching
- Includes .dockerignore for smaller images
- Properly handles $PORT environment variable

Railway will automatically detect and use this if enabled.

---

## 📋 **File Structure**

```
/
├── Procfile              # Heroku-style process definition
├── Dockerfile            # Container build instructions
├── railway.json          # Railway-specific configuration
├── nixpacks.toml         # Nixpacks configuration (alternative)
├── .dockerignore         # Docker build optimization
└── backend/              # Python application directory
    ├── app.py            # Flask application
    ├── requirements.txt  # Python dependencies
    └── ...
```

---

## 🔧 **Environment Variables**

Make sure these are set in Railway:

| Variable | Description | Required |
|----------|-------------|----------|
| `PORT` | Application port (auto-set by Railway) | ✅ |
| `SECRET_KEY` | Flask secret key | ✅ |
| `SUPABASE_URL` | Supabase project URL | Optional |
| `SUPABASE_KEY` | Supabase API key | Optional |
| `REDIS_URL` | Redis connection URL | Optional |

---

## 🎯 **Troubleshooting**

### If deployment fails:

1. **Check Railway Logs** for specific error messages
2. **Verify Build Command** is running from the correct directory
3. **Ensure $PORT** environment variable is being used
4. **Try switching builders** (Dockerfile → Nixpacks → Manual)

### Common Issues:

- **Python not found**: Make sure commands include `cd backend &&`
- **Gunicorn not found**: Ensure `pip install -r requirements.txt` runs successfully
- **Port binding errors**: Verify app binds to `0.0.0.0:$PORT`

---

## 🚀 **Deployment Status**

All deployment methods have been tested and configured:
- ✅ Procfile created and validated
- ✅ Dockerfile optimized with proper CMD syntax
- ✅ railway.json configured for automatic deployment
- ✅ nixpacks.toml updated with correct paths
- ✅ .dockerignore added for build optimization

**The forge is ready for deployment!** 🌀
