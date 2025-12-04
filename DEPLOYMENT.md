# Deployment Notes (Railway)

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
