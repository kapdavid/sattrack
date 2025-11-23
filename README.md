# SatTrack - Satellite Tracking Website

A modern, clean web application for tracking satellites with real-time updates, pass predictions, and user favorites.

## ✅ Current Status

**MVP Complete!** Phases 1-3 are fully functional. The application is ready for testing and use.

### Implemented Features

- ✅ **Browse Satellites** - View 12 curated satellites (weather, amateur radio, popular)
- ✅ **Search & Filter** - Search by name or filter by category
- ✅ **Satellite Details** - View NORAD ID, TLE data, and satellite information
- ✅ **Current Position** - Get real-time latitude, longitude, and altitude
- ✅ **Pass Predictions** - Calculate 7-day pass predictions for any location
- ✅ **Quality Scoring** - Pass quality rated 0-100 based on elevation and duration
- ✅ **User Authentication** - Sign up/login with Supabase
- ✅ **Favorites** - Save and manage favorite satellites
- ✅ **Observer Location** - Set location manually, use GPS, or quick-select cities
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile

### Planned Features (Not Yet Implemented)

- ⏳ Real-time satellite tracking map (Leaflet.js)
- ⏳ Email notifications for upcoming passes
- ⏳ Browser push notifications
- ⏳ VPS deployment setup

## Tech Stack

### Backend
- **Python 3.11+** with FastAPI
- **SQLite** for database
- **SQLAlchemy** for ORM
- **Alembic** for migrations
- **Skyfield** for orbital calculations
- **Supabase** for authentication
- **CelesTrak API** for TLE data

### Frontend
- **Vue 3** with Composition API
- **Vite** for build tooling
- **Tailwind CSS v4** for styling
- **Pinia** for state management
- **Vue Router** for routing
- **Supabase JS Client** for auth

## Project Structure

```
sattrack/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes (satellites, users, favorites)
│   │   ├── core/           # Config, auth, database
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic (orbital, satellite)
│   ├── alembic/            # Database migrations
│   ├── seed_satellites.py  # Script to seed satellite data
│   ├── requirements.txt    # Python dependencies
│   └── sattrack.db         # SQLite database
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Page views
│   │   ├── stores/         # Pinia stores
│   │   ├── services/       # API clients
│   │   └── router/         # Vue Router config
│   └── package.json        # Node dependencies
├── IMPLEMENTATION_PLAN.md  # Full development roadmap
├── SUPABASE_SETUP.md       # Supabase configuration guide
└── README.md               # This file
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm
- A Supabase account (free tier works)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd sattrack
```

### 2. Set Up Supabase

Follow the detailed guide in [SUPABASE_SETUP.md](./SUPABASE_SETUP.md) to:
1. Create a Supabase project
2. Get your API keys
3. Configure environment variables

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your Supabase credentials

# Run database migrations
alembic upgrade head

# Seed satellite data
python seed_satellites.py

# Start the development server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cat > .env << EOF
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_URL=http://localhost:8000/api
EOF

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Available API Endpoints

### Satellites
- `GET /api/satellites` - List all satellites (optional `?category=` filter)
- `GET /api/satellites/search?q=query` - Search satellites by name
- `GET /api/satellites/{id}` - Get satellite details
- `GET /api/satellites/{id}/position` - Get current satellite position
- `POST /api/satellites/{id}/predict` - Calculate pass predictions

### User (requires authentication)
- `GET /api/user/me` - Get user profile
- `PUT /api/user/location` - Update observer location

### Favorites (requires authentication)
- `GET /api/favorites` - List favorite satellites
- `POST /api/favorites` - Add satellite to favorites
- `DELETE /api/favorites/{satellite_id}` - Remove from favorites
- `GET /api/favorites/passes` - Get upcoming passes for all favorites

## Database Schema

- **users** - User accounts (linked to Supabase)
- **satellites** - Satellite catalog with TLE data
- **favorites** - User's favorite satellites
- **pass_predictions** - Cached pass predictions (not yet used)
- **notification_preferences** - Notification settings (not yet used)

## Current Satellites in Database

### Weather (5)
- NOAA 15, NOAA 18, NOAA 19
- METEOR-M 2, METEOR-M2 2

### Amateur Radio (4)
- SO-50 (SAUDISAT 1C)
- AO-91 (FOX-1B)
- LILACSAT 2
- MOVE-2 (MOVE-II)

### Popular (3)
- ISS (ZARYA)
- HST (HUBBLE)
- TIANZHOU 1

## Testing the Application

### 1. Sign Up
- Go to http://localhost:5173/register
- Create an account with email/password
- Check your email for confirmation (Supabase will send it)

### 2. Set Your Location
- Go to Settings
- Enter lat/lon manually, use GPS, or click a quick-select city
- Save location

### 3. Browse Satellites
- Click "Satellites" in navigation
- Search for satellites or filter by category
- Click "View Details" on any satellite

### 4. Calculate Passes
- On a satellite detail page
- Click "Calculate Passes (7 days)"
- View all passes in the next week with quality scores

### 5. Add Favorites
- Click the ⭐ icon on any satellite card or detail page
- View your favorites at `/favorites`

## Configuration Files

### Backend `.env`
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
RESEND_API_KEY=re_your_api_key_here  # Optional for now
```

### Frontend `.env`
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_URL=http://localhost:8000/api
```

## Development Notes

### Adding More Satellites

Edit `backend/app/services/satellite_service.py` and add entries to the `CURATED_SATELLITES` dictionary:

```python
CURATED_SATELLITES = {
    # Add your satellite
    12345: {"name": "YOUR SATELLITE", "category": "weather"},
}
```

Then run `python seed_satellites.py` to update the database.

### Updating TLE Data

TLE data is fetched from CelesTrak when seeding. To refresh:
```bash
cd backend
python seed_satellites.py
```

## Known Issues

1. **AO-92 TLE Fetch** - One amateur radio satellite (AO-92) currently fails to fetch TLE data from CelesTrak
2. **Email Notifications** - Resend integration is set up but notification scheduling is not yet implemented
3. **Pass Predictions Cache** - Pass predictions are calculated on-demand but not yet cached in the database

## Troubleshooting

### Backend won't start
- Check that `sattrack.db` exists in `/backend` directory
- Run `alembic upgrade head` to create tables
- Verify `.env` file has all required values

### Frontend won't connect to API
- Check `VITE_API_URL` in frontend `.env`
- Ensure backend is running on port 8000
- Check browser console for CORS errors

### Authentication issues
- Verify Supabase credentials in both frontend and backend `.env` files
- Check that `SUPABASE_JWT_SECRET` matches your Supabase project
- Confirm email in Supabase if using email confirmation

### No satellites showing
- Run `python seed_satellites.py` to populate the database
- Check backend logs for TLE fetch errors
- Verify CelesTrak API is accessible

## Next Steps

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for the complete development roadmap.

**Immediate next features:**
- Phase 4: Real-time satellite tracking map with Leaflet.js
- Phase 5: Email notification system
- Phase 6: VPS deployment configuration

## Contributing

This is a personal project, but feel free to fork and adapt it for your needs!

## Resources

- [Skyfield Documentation](https://rhodesmill.org/skyfield/)
- [CelesTrak TLE Data](https://celestrak.org/)
- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue 3 Documentation](https://vuejs.org/)

## License

MIT License - feel free to use this for your own projects!
