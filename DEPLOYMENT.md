# Deployment Notes

> **📌 Note**: This document is part of the deployment documentation suite.
> For the complete deployment guide, see the **[Deployment Dashboard](docs/DEPLOYMENT_DASHBOARD.md)**.

## Vercel Deployment

This repository is configured for deployment on Vercel with the following setup:

### Build Configuration

- **Build Command**: `npm run build`
- **Output Directory**: `public`
- **Node.js Version**: 18.x or higher (supports up to 24.x)

The build process:
1. Runs TypeScript type-checking (`tsc --noEmit`)
2. Copies static assets to the `public` directory
3. Includes all HTML files, JavaScript files, and the `frontend` directory

### Environment Variables

Set these in your Vercel project settings:
- `PI_APP_SECRET` - Required for Pi Network authentication
- `GUARDIAN_SLACK_WEBHOOK_URL` - Optional for Slack alerts
- `MAILGUN_DOMAIN` and `MAILGUN_API_KEY` - Optional for email alerts
- `SENDGRID_API_KEY` and `SENDGRID_FROM` - Optional for SendGrid emails

### Serverless Functions

API endpoints in the `api/` directory are automatically deployed as Vercel serverless functions:
- `/api/pi-identify` - Pi Network authentication endpoint

### Local Testing

To test the build locally:
```bash
npm install
npm run build
```

The `public` directory will contain all deployable assets.

---

## Railway Deployment

This repository includes a `railway.toml` to assist with Railway deployments. Quick notes:

- Start command used by Railway (in railway.toml):

```
cd server && uvicorn main:app --host 0.0.0.0 --port $PORT
```

- Ensure the following environment variables are set in Railway project settings:
  - `SUPABASE_URL` and `SUPABASE_KEY` if using Supabase integration
  - `SECRET_KEY` for application secrets
  - `DATABASE_URL` if you use a database
  - Any tracing/sentry/API keys (e.g., `SENTRY_DSN`)

- If your application relies on X-Forwarded-For headers for rate limiting, ensure Railway provides these headers or adjust proxy settings.

- For production, consider using Gunicorn with Uvicorn workers. Example start command:

```
cd server && exec gunicorn -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:$PORT -w 4
```

- Healthcheck endpoints available:
  - `/health` (lightweight)
  - `/` (detailed health_check)
