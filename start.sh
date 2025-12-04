#!/bin/sh
# Simple start script for Railway
pip install -r requirements.txt
gunicorn game_files.server:app
