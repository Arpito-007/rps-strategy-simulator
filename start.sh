#!/bin/sh
# Simple start script for Railway
pip install -r requirements.txt
#!/bin/bash
gunicorn server:app --bind 0.0.0.0:$PORT

