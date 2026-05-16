# AgriSense AI

AgriSense AI is a production-style smart agriculture platform for IoT monitoring, AI recommendations, irrigation automation, disease detection, weather intelligence, marketplace workflows, drone/satellite concepts, and multilingual farmer operations.

## Features

- FastAPI backend with PostgreSQL, SQLAlchemy, JWT auth, RBAC, and WebSockets.
- React + Vite + TailwindCSS frontend with premium glassmorphism UI.
- AI/ML models for crop, fertilizer, irrigation, yield, disease, and weather suggestions.
- Realtime IoT simulator for soil moisture, temperature, humidity, pH, tank level, rain, light, and wind.
- WebSocket live dashboard updates and alert broadcasting.
- SMS/email alert provider stubs.
- English, Chinese, and Urdu language support with Chinese as default.
- Docker and Docker Compose for development and production.

## Folder Structure

```txt
AgriSense-AI/
├── backend/
├── frontend/
├── ml/
├── iot-simulator/
├── docs/
├── scripts/
├── docker-compose.yml
├── docker-compose.prod.yml
└── .env.production.example
```

## Quick Start

Development:

```bash
docker compose up --build
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\uvicorn app.main:app --reload
```

## Environment Variables

Local examples:

- `backend/.env.example`
- `frontend/.env.example`

Production:

```bash
copy .env.production.example .env.production
```

Replace all secrets and domain values before deployment.

## Docker Deployment

Production:

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

Optional simulator profile:

```bash
docker compose --profile simulator up --build
```

## Backend API

- API docs in development: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- API prefix: `/api/v1`
- WebSockets:
  - `/ws/sensors/{farm_id}`
  - `/ws/alerts/{user_id}`

## Frontend Routes

- `/`
- `/login`
- `/app/dashboard`
- `/app/sensors`
- `/app/irrigation`
- `/app/weather`
- `/app/ai-crop`
- `/app/fertilizer`
- `/app/disease`
- `/app/satellite`
- `/app/marketplace`
- `/app/calendar`
- `/app/drone`
- `/app/notifications`
- `/app/profile`
- `/app/admin`
- `/app/settings`

## AI/ML System

Run training:

```bash
cd ml
..\backend\.venv\Scripts\python.exe training_scripts\train_all.py
```

Outputs:

- `ml/datasets`
- `ml/models`
- `ml/reports`

## IoT Simulator

Dry run:

```bash
cd iot-simulator
..\backend\.venv\Scripts\python.exe simulator.py --dry-run
```

Historical data:

```bash
python historical_generator.py --hours 168 --interval-minutes 15
```

## Security Notes

- Use strong JWT secrets.
- Restrict CORS and trusted hosts.
- Use HTTPS in production.
- Keep `.env.production` out of git.
- Add rate limiting before public exposure.
- Scan uploaded images before public disease-detection deployment.

## Performance Notes

- Nginx serves cached static assets.
- Backend uses GZip for larger JSON responses.
- WebSockets are used for live telemetry.
- ML models are lazily loaded and cached.
- Motion respects reduced-motion preferences.

## Future Improvements

- Alembic migration workflow.
- Redis cache and task queue.
- Real MQTT broker ingestion.
- SHAP explanations for tabular models.
- CNN/transfer-learning disease model.
- Production observability with metrics and tracing.
