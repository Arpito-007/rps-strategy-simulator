#!/bin/sh
set -e

# Install Python dependencies
python -m pip install -r requirements.txt

# Go into the folder that contains server.py
cd game_files

# Start your Flask app with Gunicorn
gunicorn server:app --bind 0.0.0.0:${PORT}
