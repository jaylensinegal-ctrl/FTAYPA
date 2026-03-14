# Flight Time Athletics Worldwide Rollout

This app works locally today. To make it available to your business and families on a real website, deploy the frontend and backend separately and connect them with environment variables.

## Best Fit Setup

- Frontend website: Vercel
- Backend API: Render
- Database: managed PostgreSQL
- Media storage: cloud object storage later, instead of local disk
- Payments: Stripe for online memberships, Square for in-person payments where supported

This split is the cleanest fit for the current codebase:
- the frontend is a Vite React app
- the backend is a FastAPI app
- the app already supports a public API URL through `VITE_FTA_API_URL`

## Public Architecture

1. Deploy the frontend from `/Users/jay/Documents/New project`
2. Deploy the backend from `/Users/jay/Documents/New project/backend`
3. Put PostgreSQL behind the backend
4. Point the frontend env var at the backend URL
5. Attach your custom domain

## Frontend Deployment

Deploy the root Vite app and set:

```env
VITE_FTA_API_URL=https://api.yourdomain.com
```

Notes:
- `vercel.json` is already included so client-side routes like `/dashboard` and `/hangar` resolve correctly on a public site
- update the frontend custom domain after the first deployment, for example:
  - `www.flighttimeathletics.com`
  - `app.flighttimeathletics.com`

## Backend Deployment

Deploy the FastAPI app from the `backend` directory with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set these environment variables:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@your-db-host:5432/flighttime_athletics
APP_BASE_URL=https://app.yourdomain.com
CORS_ORIGINS=https://app.yourdomain.com,https://www.yourdomain.com
STRIPE_SECRET_KEY=sk_live_your_real_live_key
SQUARE_PAYMENT_LINK_URL=https://square.link/u/your-link
SEED_DEMO_USERS=false
```

Notes:
- `APP_BASE_URL` controls Stripe checkout success and cancel redirects, plus account invite links
- `CORS_ORIGINS` now supports your public frontend domains without changing code
- `SEED_DEMO_USERS` should stay `false` for production so public environments do not create the local demo logins

## Domain Setup

Recommended setup:
- frontend: `app.flighttimeathletics.com`
- backend API: `api.flighttimeathletics.com`

This keeps the app and API cleanly separated while still feeling like one product.

## Before You Go Live

- switch from SQLite to PostgreSQL
- move uploads from local disk to cloud storage
- add real Stripe live keys
- add your Square payment link or Square integration
- attach custom domains
- keep HTTPS enabled
- review all payment methods for the countries you want to support
- create real coach, parent, athlete, and admin accounts instead of relying on demo users

## What Is Ready Now

- frontend can point at a public API with `VITE_FTA_API_URL`
- backend can accept public frontend origins with `CORS_ORIGINS`
- invite links and Stripe redirects can use your real domain with `APP_BASE_URL`
- public frontend route refreshes are handled with `vercel.json`

## What Still Needs Hosting Accounts

- actual Vercel project
- actual Render service
- PostgreSQL database
- domain/DNS connection
- Stripe live account configuration

## Current Local Pages

- Membership signup: `http://127.0.0.1:5173/membership`
- Hangar: `http://127.0.0.1:5173/hangar`
- Events: `http://127.0.0.1:5173/events`
- API docs: `http://127.0.0.1:8000/docs`
