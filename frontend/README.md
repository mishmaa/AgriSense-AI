# AgriSense AI Frontend

Premium React + Vite + TailwindCSS interface for the AgriSense AI smart agriculture platform.

## Architecture

- React Router drives public and authenticated application routes.
- TailwindCSS provides theme tokens, responsive layout, and glassmorphism surfaces.
- Framer Motion powers page entrances, panels, hover states, and modal transitions.
- Recharts renders telemetry and analytics charts.
- Axios is configured in `src/services/api.js` for backend integration.
- Theme state is handled in `src/context/ThemeContext.jsx`.

## Run Locally

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## Docker

From the project root:

```bash
docker compose up --build
```
