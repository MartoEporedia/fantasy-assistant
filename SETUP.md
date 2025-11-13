# 🚀 Fantasy Assistant - Setup Guide

This guide will help you set up and run the Fantasy Assistant application locally.

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm/yarn
- PostgreSQL 15+ (or use Docker)
- Docker and Docker Compose (optional but recommended)

---

## Quick Start with Docker (Recommended)

The easiest way to get started is using Docker Compose:

```bash
# 1. Clone the repository
git clone <repository-url>
cd fantasy-assistant

# 2. Start all services
cd backend
docker-compose up -d

# This will start:
# - PostgreSQL database on port 5432
# - Redis on port 6379
# - FastAPI backend on port 8000
```

The backend API will be available at `http://localhost:8000`

### Initialize Database

```bash
# Run database initialization script
docker-compose exec backend python scripts/init_db.py
```

---

## Manual Setup

If you prefer to run services individually:

### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env

# Edit .env and configure:
# - DATABASE_URL: Your PostgreSQL connection string
# - SECRET_KEY: Generate a secure random key
# - REDIS_URL: Your Redis connection string

# 5. Initialize database
python scripts/init_db.py

# 6. Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Configure API endpoint
# Edit app.json and update apiUrl if needed
# Default: http://localhost:8000

# 4. Start Expo development server
npm start

# 5. Run on device/simulator
# - Press 'a' for Android
# - Press 'i' for iOS
# - Press 'w' for web
```

---

## Database Setup

### Using Docker (Included in docker-compose)

PostgreSQL is automatically set up when using `docker-compose up`.

### Manual PostgreSQL Setup

```bash
# 1. Install PostgreSQL
# On Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# On macOS:
brew install postgresql

# 2. Create database and user
sudo -u postgres psql

CREATE DATABASE fantasy_assistant;
CREATE USER fantasy_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fantasy_assistant TO fantasy_user;
\q

# 3. Update DATABASE_URL in .env
DATABASE_URL=postgresql://fantasy_user:your_password@localhost:5432/fantasy_assistant
```

### Using Supabase (Cloud PostgreSQL)

1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Get connection string from Settings > Database
4. Update `DATABASE_URL` in `.env`

---

## Testing the Setup

### Test Backend

```bash
# Check API health
curl http://localhost:8000/health

# View API documentation
# Open browser: http://localhost:8000/docs
```

### Test Database

```bash
# Check sample players imported
curl http://localhost:8000/api/players | jq
```

### Create Test User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

---

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/fantasy_assistant
SUPABASE_URL=https://your-project.supabase.co  # Optional
SUPABASE_KEY=your-supabase-key                  # Optional

# Security
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://localhost:6379

# External APIs (for future use)
FANTACALCIO_API_KEY=your-api-key

# Environment
ENVIRONMENT=development
```

### Frontend

Frontend configuration is in `app.json`:

```json
{
  "extra": {
    "apiUrl": "http://localhost:8000"
  }
}
```

For production, update this to your deployed backend URL.

---

## Running in Production

### Backend Deployment

Recommended platforms:
- **Railway**: Easy deployment with PostgreSQL included
- **Render**: Free tier available
- **Heroku**: Classic PaaS
- **AWS/GCP/Azure**: Full control

Steps:
1. Set environment variables on your platform
2. Deploy backend code
3. Run database migrations
4. Initialize database with sample data

### Frontend Deployment

#### Expo EAS Build (Mobile Apps)

```bash
# Install EAS CLI
npm install -g eas-cli

# Configure project
eas build:configure

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# Submit to stores
eas submit
```

#### Web Deployment

```bash
# Build web version
npm run web

# Deploy to Netlify, Vercel, etc.
```

---

## Troubleshooting

### Backend Issues

**Database connection error:**
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL is correct
- Check firewall/network settings

**Import errors:**
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.11+)

### Frontend Issues

**Metro bundler error:**
```bash
# Clear cache
npm start -- --clear

# Or
npx expo start -c
```

**Network error connecting to API:**
- If running on physical device, use local network IP instead of localhost
- Update `apiUrl` in `app.json` to your computer's IP: `http://192.168.1.X:8000`

**Dependencies error:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

---

## Development Tips

### Hot Reload

- **Backend**: FastAPI auto-reloads on code changes when using `--reload` flag
- **Frontend**: Expo auto-refreshes on save

### Database Migrations

```bash
# Create new migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Add New Dependencies

**Backend:**
```bash
pip install package-name
pip freeze > requirements.txt
```

**Frontend:**
```bash
npm install package-name
```

---

## Next Steps

1. ✅ Complete setup
2. 📱 Run the app and explore features
3. 🎨 Customize theme in `frontend/src/theme.ts`
4. 🔌 Integrate real data sources (Serie A APIs)
5. 🤖 Train ML models with actual data
6. 🚀 Deploy to production

---

## Support

For issues and questions:
- Check existing documentation
- Review error logs
- Create issue on GitHub repository

---

Happy coding! ⚽🚀
