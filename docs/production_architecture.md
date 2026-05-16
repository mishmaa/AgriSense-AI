# AgriSense AI Production Architecture

## 1. Final Optimized Architecture

```txt
Client Browser
  -> Nginx static frontend
  -> FastAPI backend
  -> PostgreSQL
  -> ML model artifacts
  -> IoT simulator / MQTT bridge
  -> SMS and email providers
```

Runtime responsibilities:

- Frontend serves a Vite production build through Nginx with asset caching and SPA fallback.
- Backend exposes REST APIs, WebSockets, JWT authentication, RBAC, AI prediction endpoints, and IoT ingestion.
- PostgreSQL stores users, farms, sensors, readings, AI outputs, marketplace listings, crop calendar, and notifications.
- ML models are loaded from `ml/models` and have deterministic fallbacks if models are missing.
- IoT simulator can publish directly to FastAPI or through MQTT using the optional adapter.

## 2. Docker Setup

Development:

```bash
docker compose up --build
```

Production:

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

Main containers:

- `postgres`: PostgreSQL 16 with persistent volume.
- `backend`: FastAPI + ML models + WebSocket support.
- `frontend`: Nginx static frontend.
- `iot-simulator`: optional profile-driven telemetry producer.

## 3. Deployment Configuration

Recommended deployment flow:

1. Copy `.env.production.example` to `.env.production`.
2. Replace secrets, database password, JWT secret, CORS origins, and hostnames.
3. Build images with `docker compose -f docker-compose.prod.yml build`.
4. Start services with `docker compose -f docker-compose.prod.yml up -d`.
5. Check health with `GET /health`.
6. Confirm frontend loads and can reach `/api/v1`.
7. Configure HTTPS at reverse proxy or platform load balancer.

## 4. Environment Variables Template

Root `.env.production.example` defines shared production variables. Backend and frontend examples remain in their own folders for local development.

Critical variables:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `BACKEND_CORS_ORIGINS`
- `TRUSTED_HOSTS`
- `VITE_API_BASE_URL`
- `VITE_WS_BASE_URL`
- `SMTP_HOST`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `SMS_PROVIDER_API_KEY`

## 5. Production Checklist

- Use HTTPS.
- Use a long random `JWT_SECRET_KEY`.
- Disable default dev secrets.
- Restrict CORS origins.
- Restrict trusted hosts.
- Configure persistent PostgreSQL volume.
- Keep `.env.production` out of git.
- Run database migrations before release.
- Confirm `/health` returns `ok`.
- Confirm WebSocket sensor stream connects.
- Confirm AI endpoints return model-backed outputs.
- Confirm frontend assets are served with cache headers.

## 6. Security Checklist

- Passwords are hashed with passlib/bcrypt.
- JWT tokens are signed and expire.
- RBAC guards admin endpoints.
- SQLAlchemy parameterization avoids SQL injection.
- CORS is configured by environment.
- Trusted hosts are configured by environment.
- Sensitive values are never committed.
- SMS/email providers are optional and environment-backed.
- Uploaded disease images should be size/type scanned before public launch.
- Add API rate limiting before internet exposure.

## 7. Performance Checklist

- Nginx serves compressed static assets.
- Long-lived cache headers are applied to hashed assets.
- FastAPI uses GZip middleware for larger JSON responses.
- Dashboard WebSocket avoids polling for live telemetry.
- ML models are loaded lazily and cached in process.
- Frontend code is organized by routes and reusable widgets.
- Motion effects honor `prefers-reduced-motion`.
- Skeleton states are reusable and lightweight.
- Historical analytics endpoints support `limit` query bounds.

## 8. Final README Structure

```txt
README.md
├── Project overview
├── Features
├── Architecture
├── Tech stack
├── Folder structure
├── Quick start
├── Environment variables
├── Docker deployment
├── Backend API
├── Frontend routes
├── AI/ML system
├── IoT simulator
├── Security notes
├── Performance notes
└── Future improvements
```
