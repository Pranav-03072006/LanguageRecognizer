#!/usr/bin/env bash
# Vercel Build Script for Django Application
set -e

echo "==> Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "==> Collecting static assets with WhiteNoise..."
python3 manage.py collectstatic --noinput --clear

echo "==> Vercel build complete!"
