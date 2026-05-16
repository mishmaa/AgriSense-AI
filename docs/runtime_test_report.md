# AgriSense AI Runtime Test Report

Date: 2026-05-16  
Environment: Windows PowerShell, Python 3.14.4, Node 24.15.0, Docker 29.4.2, Docker Compose v5.1.3, WSL2

## Summary

AgriSense AI was executed and validated locally. The backend, frontend, PostgreSQL Docker database, database migration path, WebSocket flow, AI endpoints, browser rendering, Docker Compose stack, and IoT simulator all passed runtime verification.

## Services Run

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173`
- Local non-Docker validation database: SQLite
- Docker validation database: PostgreSQL 16 container
- PostgreSQL host port: `55432` because local PostgreSQL is already using `5432`
- API documentation: `http://127.0.0.1:8000/docs`

## Dependency Installation

- Backend dependencies: installed with `backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt`
- Frontend dependencies: installed with locally bootstrapped npm at `tools\npm\package\bin\npm-cli.js`
- Frontend lockfile generated: `frontend\package-lock.json`
- Docker Desktop, WSL2, Node.js, npm, and PostgreSQL CLI were installed and verified by full path where needed.

## Fixes Applied During Runtime Testing

- Fixed comma-separated environment parsing for `TRUSTED_HOSTS` and `BACKEND_CORS_ORIGINS`.
- Added portable SQLAlchemy JSON type while preserving PostgreSQL JSONB in production.
- Pinned `bcrypt<5` to fix `passlib` password hashing runtime failure.
- Added missing AI feature mapping for yield prediction: `irrigation_events_count` to `irrigation_events`.
- Added `soil_type` to fertilizer recommendation requests.
- Updated IoT simulator HTTP client to ignore local proxy environment for localhost runtime calls.
- Added frontend favicon to remove browser console 404 noise.
- Hardened the Recharts wrapper sizing to remove runtime layout warnings in Chrome.
- Added Alembic migration scaffold and generated the initial schema migration.

## Validation Results

| Area | Result |
|---|---:|
| Backend import/compile | Passed |
| Backend server health | Passed |
| Frontend dependency install | Passed |
| Frontend production build | Passed |
| Frontend dev server | Passed |
| Alembic migration upgrade | Passed |
| Auth APIs | Passed |
| Farm APIs | Passed |
| Sensor APIs | Passed |
| WebSocket sensor stream | Passed |
| AI crop recommendation | Passed |
| AI fertilizer recommendation | Passed |
| AI yield prediction | Passed |
| AI irrigation prediction | Passed |
| AI weather suggestion | Passed |
| Disease feature detection | Passed |
| Chatbot endpoint | Passed |
| Weather snapshot API | Passed |
| Analytics dashboard API | Passed |
| Notifications API | Passed |
| IoT simulator dry-run | Passed |
| IoT simulator live API posting | Passed |
| Browser rendering in Chrome | Passed |
| Docker Compose config | Passed |
| Docker image build | Passed |
| Docker backend container | Passed |
| Docker frontend container | Passed |
| Docker PostgreSQL container | Passed |
| Docker frontend Chrome render | Passed |
| Docker IoT simulator dry-run | Passed |
| Docker IoT simulator live API posting | Passed |
| Swagger API docs | Passed |

## API Integration Suite

The final Docker API/WebSocket integration suite passed `20/20` checks:

- `GET /health`
- `POST /api/v1/auth/register`
- `GET /api/v1/auth/me`
- `POST /api/v1/farms/`
- `POST /api/v1/sensors/`
- `WS /ws/sensors/{farm_id}`
- `POST /api/v1/sensors/readings`
- second `POST /api/v1/sensors/readings` for live broadcast verification
- WebSocket broadcast after sensor ingestion
- `GET /api/v1/sensors/readings/{farm_id}`
- `POST /api/v1/ai/crop-recommendation`
- `POST /api/v1/ai/fertilizer-recommendation`
- `POST /api/v1/ai/yield-prediction`
- `POST /api/v1/ai/irrigation-prediction`
- `POST /api/v1/ai/weather-suggestion`
- `POST /api/v1/disease-detection/features`
- `POST /api/v1/chatbot/message`
- `POST /api/v1/weather/snapshot`
- `GET /api/v1/analytics/dashboard/{farm_id}`
- `GET /api/v1/notifications/`

## Frontend Rendering

The React app rendered successfully in system Chrome via Playwright:

- Page title: `AgriSense AI`
- Dashboard route: `/app/dashboard`
- Chinese default UI verified with `html lang="zh-CN"`
- No console warnings or errors after chart wrapper fix
- No failed HTTP resources
- Docker dashboard screenshot: `runtime-logs/docker-chrome-dashboard.png`
- Earlier mobile dashboard screenshot: `runtime-logs/frontend-mobile-dashboard.png`

## Sensor Simulation

The simulator was tested in two modes:

- Dry-run mode generated realistic sensor values for soil moisture, temperature, humidity, pH, tank level, rainfall, light, wind, and anomaly score.
- Live mode posted two readings to the backend API and verified they were persisted through `GET /api/v1/sensors/readings/{farm_id}`.

## Docker Status

Docker Desktop and WSL2 are installed and working. The full Compose stack builds and runs successfully.

Installed and verified by full path:

- Docker CLI: `C:\Program Files\Docker\Docker\resources\bin\docker.exe`
- PostgreSQL CLI: `C:\Program Files\PostgreSQL\18\bin\psql.exe`
- Node/npm: `C:\Program Files\nodejs\node.exe`, `C:\Program Files\nodejs\npm.cmd`

Running containers:

- `agrisense-ai-backend-1`: healthy, mapped to `0.0.0.0:8000`
- `agrisense-ai-frontend-1`: running, mapped to `0.0.0.0:5173`
- `agrisense-ai-postgres-1`: healthy, mapped to `0.0.0.0:55432`

Validated Docker commands:

```powershell
docker compose config
docker compose up --build -d
docker compose --profile simulator run --rm iot-simulator
```

The development Compose file maps PostgreSQL to host port `55432` because local PostgreSQL is already running on `5432`. The backend still connects to `postgres:5432` inside the Docker network.

Native PostgreSQL note:

- PostgreSQL 18 is installed locally, but `psql` is not on the current shell PATH.
- Docker PostgreSQL was used for final runtime validation, so no manual local database creation is required for the running stack.

## Final Result

The project is locally runnable, Dockerized, and validated in the available environment. The running stack is ready for demonstration at `http://127.0.0.1:5173`, with backend docs available at `http://127.0.0.1:8000/docs`.
