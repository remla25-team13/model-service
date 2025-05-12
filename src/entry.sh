#!/bin/sh

if [ "$MODE" = "PROD" ]; then
    echo "Running in production mode 🚀."
    waitress-serve --host=0.0.0.0 --port=$PORT src.app:app
else
    echo "Running in dev mode 📝."
    python src/app.py
fi
