#!/bin/sh

if [ "$MODE" = "PROD" ]; then
    echo "Running in production mode 🚀."
    waitress-serve src.app:app
else
    echo "Running in dev mode 📝."
    python src/app.py
fi
