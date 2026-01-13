# LumiCore Data Cleaning API — Backend

This is the backend for the LumiCore Data Cleaning Challenge.
It acts as a proxy, validator, and data normalizer between the frontend and LumiCore’s unreliable external API.

---

## Tech Stack

- Django 5
- Django REST Framework
- Requests
- django-cors-headers
- Gunicorn
- WhiteNoise
- Python 3.11+

---

## What this backend does

The LumiCore API:
- fails randomly
- returns inconsistent field names
- sends duplicates
- uses mixed date formats

This backend:
- retries failed requests
- normalizes field names
- cleans date formats
- removes duplicates
- validates data
- protects the frontend from chaos

---

## Architecture

Next.js Frontend
        ↓
This Django API
        ↓
LumiCore Unreliable API

The frontend never talks directly to LumiCore.

---

## Environment Variables

Create a .env file in the backend root:

SECRET_KEY=your-secret-key
DEBUG=True
API_BASE_URL=https://fast-endpoint-production.up.railway.app
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-vercel-app.vercel.app

API_BASE_URL tells Django where the LumiCore API lives.

---

## Local Setup

1. Install dependencies

pip install -r requirements.txt

2. Run migrations

python manage.py migrate

3. Start the server

python manage.py runserver

The server will run at:

http://localhost:8000

---

## Production Deployment

This backend is designed to run on Railway or Render using:

gunicorn backend.wsgi

Static files are served using WhiteNoise.

---

## Key Idea

This backend is a data pipeline, not a database app.

It:
1. Fetches data from LumiCore
2. Retries on failure
3. Cleans and normalizes it
4. Sends only stable JSON to the frontend

---

## Purpose

Real-world systems depend on unstable third-party APIs.
This backend shows how engineers isolate failures and keep user-facing apps reliable.

---

