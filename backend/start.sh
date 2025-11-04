#!/bin/bash
# Install dependencies and start the application
pip install -r requirements.txt
python -m gunicorn -w 2 -k gevent -b 0.0.0.0:$PORT app:app
