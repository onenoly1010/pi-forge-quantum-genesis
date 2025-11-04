FROM python:3.11-slim

WORKDIR /app/backend

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD python -m gunicorn -w 2 -k gevent -b 0.0.0.0:$PORT app:app
