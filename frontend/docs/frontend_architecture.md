# AgriSense AI Frontend Architecture

AgriSense AI uses a React + Vite frontend designed as a premium agri-tech command center. The interface blends a deep agritech visual language with glass surfaces, motion, dense operational dashboards, and mobile-first workflows.

## 1. Frontend Folder Structure

```txt
frontend/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── layout/
│   │   └── ui/
│   ├── context/
│   ├── data/
│   ├── hooks/
│   ├── pages/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── docs/
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── vite.config.js
```

## 2. Component Architecture

### Layout Components

- `AppShell`: Protected application frame with sidebar, topbar, page container, and mobile drawer behavior.
- `Sidebar`: Primary navigation across all product modules.
- `Topbar`: Search, theme toggle, notifications, and profile controls.
- `PageHeader`: Consistent page title, subtitle, and page-level actions.

### UI Components

- `GlassPanel`: Shared glassmorphism panel primitive.
- `StatCard`: Animated KPI card with icon, value, trend, and supporting signal.
- `SensorWidget`: Live IoT metric widget with thresholds and status state.
- `RealtimeChart`: Recharts-powered chart wrapper for live analytics.
- `ProgressRing`: Circular progress indicator for tank level, health score, and confidence.
- `AIInsightCard`: Recommendation/diagnostic summary card.
- `DataTable`: Responsive operational table.
- `SearchFilterBar`: Search input and compact filter controls.
- `LoadingSkeleton`: Premium loading state.
- `Modal`: Reusable motion modal.
- `FloatingActionButton`: Contextual action launcher.

## 3. Theme System

The theme uses Tailwind class-based dark mode. `ThemeProvider` stores preference in localStorage and applies `dark` to the document root.

Design tokens:

- Backgrounds: near-black graphite, soft white, layered translucent panels.
- Primary: emerald and agritech green.
- Secondary: cyan, blue, amber, and rose for analytics state.
- Surfaces: glass panels with subtle borders, blur, and restrained shadows.
- Typography: Inter-like system stack, compact dashboard scale, no negative letter spacing.

## 4. Routing System

Routes use React Router:

```txt
/                  Landing page
/login             Login/Register
/app/dashboard     Smart dashboard
/app/sensors       Sensor analytics
/app/irrigation    Irrigation control
/app/weather       Weather intelligence
/app/ai-crop       AI crop recommendation
/app/disease       Disease detection
/app/marketplace   Marketplace
/app/calendar      Crop calendar
/app/drone         Drone monitoring
/app/notifications Notifications
/app/profile       Farmer profile
/app/admin         Admin dashboard
/app/settings      Settings
```

## 5. State Management Plan

Initial production-ready approach:

- React Context for theme and UI state.
- Local component state for page-specific filters/forms.
- Axios service layer for backend calls.
- React Query can be added later for cache, retry, background refresh, and optimistic updates.
- WebSocket hooks can subscribe to `/ws/sensors/{farm_id}` and `/ws/alerts/{user_id}` once backend auth is connected.

State domains:

- Auth session: user, access token, role.
- Farm context: selected farm and zone.
- Realtime telemetry: live sensor snapshots.
- Notifications: unread count and alert stream.
- UI preferences: theme, sidebar state, language.

## 6. Responsive Strategy

- Mobile-first CSS with single-column views by default.
- Sidebar becomes a slide-in drawer below large screens.
- Dashboard cards use responsive grids with fixed minimum dimensions to prevent layout jumps.
- Tables degrade into scrollable surfaces with sticky headers.
- Charts retain stable height and touch-friendly tooltips.
- Buttons and filters wrap into compact toolbars on small screens.
- Landing hero always leaves the next section visible and uses a real agriculture background image.

## 7. UI/UX Direction

The product should feel like a commercial control center:

- First screen shows an actual farm intelligence experience, not a generic marketing block.
- Dashboard is dense but calm, optimized for scanning live metrics.
- Motion is used for state changes, route entrances, modals, and card hover feedback.
- AI features expose confidence, reasoning, and recommended actions.
- Concept pages such as drone monitoring look credible, with operational mission data and map-like visualization.
