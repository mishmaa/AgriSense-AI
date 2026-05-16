# Deployment Guide

## Local Production Rehearsal

1. Copy `.env.production.example` to `.env.production`.
2. Replace `JWT_SECRET_KEY`, `POSTGRES_PASSWORD`, `DATABASE_URL`, `BACKEND_CORS_ORIGINS`, and `TRUSTED_HOSTS`.
3. Run:

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

4. Open the frontend on `http://localhost`.
5. Check backend health:

```bash
curl http://localhost:8000/health
```

In the included production compose, backend is exposed internally and frontend is exposed on port 80. In a real deployment, route `/api` and `/ws` through a reverse proxy or platform gateway to the backend service.

## Cloud Deployment Notes

- Put PostgreSQL on a managed database service when possible.
- Store secrets in the platform secret manager.
- Terminate TLS at the platform load balancer or reverse proxy.
- Run backend and frontend as separate services.
- Mount or bake `ml/models` into the backend image.
- Enable container restart policies.
- Configure log forwarding.

## Release Checklist

- Production env configured.
- Database migrated.
- Backend health check passes.
- Frontend loads through Nginx.
- API and WebSocket origins are correct.
- ML models exist.
- IoT simulator disabled unless needed.
- SMS/email keys configured if alerts are expected.
