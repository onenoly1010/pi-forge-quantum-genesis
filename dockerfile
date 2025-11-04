FROM python:3.11-slim

WORKDIR /app/backend

# Copy requirements first for better caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY backend/ .

# Expose the port Railway provides
ENV PORT=8080
EXPOSE $PORT

# Run gunicorn
CMD ["python", "-m", "gunicorn", "-w", "2", "-k", "gevent", "-b", "0.0.0.0:8080", "app:app"]
