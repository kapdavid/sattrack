# Satellite Tracking Website - Implementation Plan

## Tech Stack Summary
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Frontend**: Vue 3 (Composition API), Tailwind CSS, Vite
- **Auth**: Supabase (cloud - auth only)
- **Database**: SQLite (on VPS)
- **Mapping**: Leaflet.js + satellite.js
- **Email**: Resend
- **Deployment**: Single VPS (Nginx reverse proxy, systemd services)

---

## Phase 1: Project Foundation & Infrastructure

### 1.1 Project Setup
- [ ] Initialize Git repository with proper `.gitignore`
- [ ] Create project structure:
  ```
  sattrack/
  ├── backend/
  │   ├── app/
  │   │   ├── api/          # API routes
  │   │   ├── core/         # Config, security, dependencies
  │   │   ├── models/       # SQLAlchemy models
  │   │   ├── schemas/      # Pydantic schemas
  │   │   ├── services/     # Business logic
  │   │   └── main.py
  │   ├── tests/
  │   ├── requirements.txt
  │   └── alembic/          # DB migrations
  ├── frontend/
  │   ├── src/
  │   │   ├── components/
  │   │   ├── views/
  │   │   ├── composables/  # Vue composables
  │   │   ├── services/     # API clients
  │   │   └── stores/       # Pinia state management
  │   ├── public/
  │   └── package.json
  └── README.md
  ```
- [ ] Set up Python virtual environment
- [ ] Initialize FastAPI app with CORS, basic health check endpoint
- [ ] Initialize Vue 3 app with Vite
- [ ] Configure Tailwind CSS

### 1.2 Database Setup
- [ ] Design database schema:
  - `users` (id, email, supabase_id, location_lat, location_lon, created_at)
  - `satellites` (id, norad_id, name, category, tle_line1, tle_line2, last_updated)
  - `favorites` (user_id, satellite_id, created_at)
  - `pass_predictions` (id, user_id, satellite_id, aos_time, los_time, max_elevation, duration, quality_score)
  - `notification_preferences` (user_id, satellite_id, min_elevation, email_enabled, push_enabled)
- [ ] Set up SQLAlchemy models
- [ ] Configure Alembic for migrations
- [ ] Create initial migration

### 1.3 Authentication Setup
- [ ] Create Supabase project (cloud)
- [ ] Configure Supabase auth (email/password)
- [ ] Implement FastAPI middleware for Supabase JWT verification
- [ ] Create auth endpoints (verify token, get user profile)
- [ ] Test auth flow end-to-end

---

## Phase 2: Core Backend Features

### 2.1 Satellite Data Management
- [ ] Create service to fetch TLE data from CelesTrak API
- [ ] Implement satellite categorization:
  - Weather satellites (NOAA 15, 18, 19, Meteor-M, etc.)
  - Amateur radio (SO-50, AO-91, AO-92, etc.)
  - Popular satellites (ISS, Hubble, etc.)
- [ ] Create API endpoint: `GET /api/satellites` (list with filters by category)
- [ ] Create API endpoint: `GET /api/satellites/{id}` (satellite details)
- [ ] Create API endpoint: `GET /api/satellites/search?q=query`
- [ ] Schedule periodic TLE updates (daily via cron/scheduled task)

### 2.2 Orbital Calculations
- [ ] Install and configure `skyfield` or `pyorbital` for orbital calculations
- [ ] Create service for satellite position calculation (lat/lon/alt at given time)
- [ ] Create service for pass prediction:
  - Calculate AOS (Acquisition of Signal), LOS (Loss of Signal), TCA (Time of Closest Approach)
  - Calculate max elevation, azimuth at AOS/LOS
  - Calculate pass duration
- [ ] Implement pass quality scoring algorithm:
  - Base score on max elevation (higher = better)
  - Consider pass duration
  - Consider time of day (optional: favor evening/morning visible passes)
- [ ] Create API endpoint: `POST /api/satellites/{id}/predict` (calculate passes for user location)

### 2.3 User Features
- [ ] Create API endpoint: `PUT /api/user/location` (update user's observer location)
- [ ] Create API endpoint: `POST /api/favorites/{satellite_id}` (add favorite)
- [ ] Create API endpoint: `DELETE /api/favorites/{satellite_id}` (remove favorite)
- [ ] Create API endpoint: `GET /api/favorites` (list user's favorites with upcoming passes)
- [ ] Implement background task to pre-calculate passes for all user favorites (runs daily)
- [ ] Store pass predictions in database with cache invalidation strategy

---

## Phase 3: Frontend Development

### 3.1 Core UI Components
- [ ] Set up Vue Router (routes: home, login, register, satellites, favorites, satellite detail, settings)
- [ ] Set up Pinia for state management (auth store, satellite store, user store)
- [ ] Create layout components:
  - `AppHeader.vue` (navigation, user menu)
  - `AppFooter.vue`
  - `MainLayout.vue`
- [ ] Design and implement responsive navigation (mobile hamburger menu)
- [ ] Set up Tailwind responsive breakpoints

### 3.2 Authentication UI
- [ ] Create `LoginView.vue` (Supabase auth integration)
- [ ] Create `RegisterView.vue` (email/password signup)
- [ ] Create `ForgotPasswordView.vue`
- [ ] Implement auth state management (Pinia store)
- [ ] Add route guards for protected pages
- [ ] Create user settings page (location configuration)

### 3.3 Satellite Browser
- [ ] Create `SatellitesView.vue`:
  - Search bar
  - Category filters (tabs or dropdown)
  - Satellite list/grid (cards)
  - Responsive layout
- [ ] Create `SatelliteCard.vue` component:
  - Satellite name, category badge
  - Quick favorite button
  - Real-time position indicator
- [ ] Implement search functionality (debounced API calls)
- [ ] Add loading states and error handling

### 3.4 Satellite Detail Page
- [ ] Create `SatelliteDetailView.vue`:
  - Satellite info (name, NORAD ID, category)
  - Current position (lat/lon, altitude)
  - Upcoming passes table (7 days)
  - Pass quality indicators (badges/stars)
  - Favorite/unfavorite button
  - Set notification preferences
- [ ] Create `PassTable.vue` component:
  - Sortable by date, elevation, duration
  - Quality score visualization
  - AOS/LOS times formatted nicely
  - Max elevation and azimuth
- [ ] Format dates/times in user's local timezone

### 3.5 Favorites Dashboard
- [ ] Create `FavoritesView.vue`:
  - Grid of favorite satellites
  - "Next Pass" summary for each
  - Quick access to satellite details
  - Option to configure notifications per satellite
- [ ] Create aggregated "All Upcoming Passes" view:
  - Combined timeline of all favorite satellite passes
  - Sorted by time
  - Filterable by satellite, min elevation, etc.

---

## Phase 4: Real-time Tracking & Mapping

### 4.1 Map Integration
- [ ] Install Leaflet.js and Vue3 wrapper
- [ ] Create `SatelliteMap.vue` component:
  - Base map (OpenStreetMap tiles)
  - User location marker (from profile)
  - Configurable zoom/center
- [ ] Implement satellite.js for orbital calculations in browser
- [ ] Create real-time satellite position plotting:
  - Fetch TLE from backend
  - Calculate current position every 1-2 seconds
  - Update marker on map
- [ ] Add satellite ground track (orbital path visualization)
- [ ] Add visibility circle (where satellite is above horizon)

### 4.2 Interactive Features
- [ ] Click on satellite marker to show info popup (name, altitude, velocity)
- [ ] Add satellite selection (highlight on map when selected from list)
- [ ] Show multiple satellites simultaneously (user's favorites)
- [ ] Add playback controls:
  - Fast-forward time to see future positions
  - Pause/play real-time tracking
  - Reset to current time
- [ ] Add pass visualization:
  - Show satellite path during a specific pass
  - Highlight AOS/LOS points
  - Show user's horizon

### 4.3 Mobile Optimization
- [ ] Make map responsive (different controls for mobile)
- [ ] Add GPS location option for mobile devices
- [ ] Optimize map performance (lazy loading, marker clustering if needed)
- [ ] Touch-friendly controls

---

## Phase 5: Notifications & Polish

### 5.1 Email Notifications
- [ ] Set up Resend account and API key
- [ ] Create email templates (HTML + plain text):
  - Upcoming pass notification (sent X hours before)
  - Daily digest of passes for favorite satellites
  - Welcome email
- [ ] Implement notification scheduling service:
  - Check for upcoming passes (runs every hour)
  - Queue emails for users with notification preferences
  - Send emails via Resend API
- [ ] Create API endpoints:
  - `GET /api/notifications/preferences`
  - `PUT /api/notifications/preferences/{satellite_id}`
- [ ] Add unsubscribe mechanism (unique tokens)

### 5.2 Browser Push Notifications (Optional Enhancement)
- [ ] Set up Web Push API
- [ ] Request notification permissions in browser
- [ ] Store push subscriptions in database
- [ ] Send browser notifications for imminent passes

### 5.3 UI Polish & UX
- [ ] Add skeleton loaders for async content
- [ ] Implement proper error states and user-friendly messages
- [ ] Add tooltips and help text where needed
- [ ] Create dark mode (optional but nice with Tailwind)
- [ ] Add animations and transitions (subtle, performant)
- [ ] Create "first-time user" onboarding flow:
  - Set location
  - Browse/select first favorite satellites
  - Configure notification preferences
- [ ] Add About/Help page explaining pass quality, terminology

### 5.4 Performance Optimization
- [ ] Implement API response caching (passes don't change frequently)
- [ ] Add request rate limiting (prevent abuse)
- [ ] Optimize bundle size (code splitting, lazy loading routes)
- [ ] Add service worker for offline capability (optional)
- [ ] Database indexing for common queries

---

## Phase 6: Deployment & DevOps

### 6.1 VPS Setup
- [ ] Provision VPS (Ubuntu 22.04 LTS recommended)
- [ ] Configure firewall (UFW: allow 80, 443, 22)
- [ ] Set up non-root user with sudo
- [ ] Install dependencies: Python 3.11+, Node.js, Nginx, SQLite, Git
- [ ] Configure Nginx as reverse proxy:
  - Frontend served as static files
  - `/api/*` proxied to FastAPI backend
- [ ] Set up SSL with Let's Encrypt (Certbot)

### 6.2 Backend Deployment
- [ ] Create systemd service for FastAPI app (Gunicorn + Uvicorn workers)
- [ ] Configure environment variables (`.env` file):
  - Supabase URL and anon key
  - Resend API key
  - Database path
  - Secret keys
- [ ] Run database migrations
- [ ] Set up log rotation
- [ ] Create scheduled tasks (cron):
  - Daily TLE update
  - Hourly notification check
  - Daily pass prediction generation

### 6.3 Frontend Deployment
- [ ] Build Vue app for production (`npm run build`)
- [ ] Deploy dist files to Nginx web root
- [ ] Configure client-side routing (Nginx rewrite rules)
- [ ] Set up asset caching headers

### 6.4 Monitoring & Maintenance
- [ ] Set up basic monitoring:
  - Uptime checks (UptimeRobot or similar)
  - Error logging (file-based initially, could add Sentry later)
- [ ] Create backup strategy:
  - Daily SQLite database backups
  - Store backups off-site (S3/Backblaze B2)
- [ ] Document deployment process
- [ ] Create update/rollback procedures

### 6.5 Testing & QA
- [ ] Manual testing on desktop, tablet, mobile
- [ ] Test all user flows end-to-end
- [ ] Verify email delivery
- [ ] Load test with anticipated traffic
- [ ] Fix any bugs discovered

---

## Phase 7: Launch & Iteration

### 7.1 Soft Launch
- [ ] Deploy to production
- [ ] Test with small group of users
- [ ] Gather initial feedback
- [ ] Monitor error logs and performance

### 7.2 Future Enhancements (Post-MVP)
- [ ] GPS location support for mobile
- [ ] Weather satellite image reception info/tips
- [ ] Satellite pass visibility predictions (day/night, sunlit satellite)
- [ ] Social features (share passes, public favorite lists)
- [ ] API for third-party integrations
- [ ] Mobile app (PWA conversion or native)
- [ ] Support for geostationary satellites
- [ ] Integration with radio tuning apps/hardware
- [ ] Historical pass data and statistics

---

## Estimated Timeline
- **Phase 1**: 1-2 weeks
- **Phase 2**: 2-3 weeks
- **Phase 3**: 2-3 weeks
- **Phase 4**: 1-2 weeks
- **Phase 5**: 1-2 weeks
- **Phase 6**: 1 week
- **Total**: ~8-13 weeks for MVP

This plan is comprehensive but flexible - you can adjust priorities and tackle phases in different orders based on what excites you most!
