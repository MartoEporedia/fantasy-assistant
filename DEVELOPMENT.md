# 🛠️ Development Guide

This guide covers advanced development topics and how to extend the Fantasy Assistant application.

## Project Structure

```
fantasy-assistant/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── players.py     # Player management
│   │   │   ├── auctions.py    # Auction logic
│   │   │   ├── rosters.py     # Roster management
│   │   │   ├── advice.py      # AI recommendations
│   │   │   └── community.py   # Community features
│   │   ├── core/              # Core utilities
│   │   │   ├── config.py      # Configuration
│   │   │   └── security.py    # Auth & security
│   │   ├── db/                # Database
│   │   │   ├── database.py    # DB connection
│   │   │   └── models.py      # SQLAlchemy models
│   │   ├── ml/                # Machine learning
│   │   │   ├── valuation.py   # Player valuation
│   │   │   └── roster_analyzer.py
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── scrapers/          # Data importers
│   │   └── main.py            # App entry point
│   ├── alembic/               # Database migrations
│   ├── scripts/               # Utility scripts
│   ├── requirements.txt       # Python dependencies
│   └── docker-compose.yml     # Docker setup
│
└── frontend/                   # React Native frontend
    ├── src/
    │   ├── config/            # Configuration
    │   ├── contexts/          # React contexts
    │   ├── navigation/        # App navigation
    │   ├── screens/           # Screen components
    │   │   ├── auth/          # Login/Register
    │   │   ├── players/       # Player screens
    │   │   ├── auctions/      # Auction screens
    │   │   ├── rosters/       # Roster screens
    │   │   └── profile/       # User profile
    │   └── theme.ts           # App theme
    ├── App.tsx                # Root component
    └── package.json           # Node dependencies
```

---

## Adding New Features

### Backend: Adding a New API Endpoint

1. **Create Schema** (`app/schemas/feature.py`)

```python
from pydantic import BaseModel

class FeatureCreate(BaseModel):
    name: str
    value: int

class FeatureResponse(FeatureCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

2. **Create API Route** (`app/api/feature.py`)

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=FeatureResponse)
def create_feature(feature: FeatureCreate, db: Session = Depends(get_db)):
    # Implementation
    pass

@router.get("/{feature_id}", response_model=FeatureResponse)
def get_feature(feature_id: int, db: Session = Depends(get_db)):
    # Implementation
    pass
```

3. **Register Router** (`app/main.py`)

```python
from app.api import feature

app.include_router(feature.router, prefix="/api/features", tags=["features"])
```

### Frontend: Adding a New Screen

1. **Create Screen Component** (`src/screens/feature/FeatureScreen.tsx`)

```typescript
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text } from 'react-native-paper';

export default function FeatureScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      <Text variant="headlineMedium">Feature Screen</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
});
```

2. **Add to Navigation** (`src/navigation/AppNavigator.tsx`)

```typescript
import FeatureScreen from '../screens/feature/FeatureScreen';

// Add to stack or tab navigator
<Stack.Screen name="Feature" component={FeatureScreen} />
```

3. **Create API Hook** (optional)

```typescript
import { useQuery } from '@tanstack/react-query';
import api from '../config/api';

export const useFeature = (id: number) => {
  return useQuery({
    queryKey: ['feature', id],
    queryFn: async () => {
      const response = await api.get(`/features/${id}`);
      return response.data;
    },
  });
};
```

---

## Machine Learning Integration

### Training a New Model

1. **Collect Training Data**

```python
# backend/app/ml/training/collect_data.py
from sqlalchemy.orm import Session
from app.db.models import Player, Bid
import pandas as pd

def collect_training_data(db: Session):
    players = db.query(Player).all()

    data = []
    for player in players:
        data.append({
            'role': player.role,
            'age': player.age,
            'goals': player.goals,
            'assists': player.assists,
            'avg_rating': player.avg_rating,
            'market_value': player.market_value
        })

    return pd.DataFrame(data)
```

2. **Train Model**

```python
# backend/app/ml/training/train.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def train_valuation_model(data):
    X = data[['role_encoded', 'age', 'goals', 'assists', 'avg_rating']]
    y = data['market_value']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, 'models/valuation_model.pkl')

    return model
```

3. **Use Model for Predictions**

```python
# backend/app/ml/valuation.py
import joblib

model = joblib.load('models/valuation_model.pkl')

def predict_value(player):
    features = prepare_features(player)
    return model.predict([features])[0]
```

---

## Data Scraping

### Adding a New Data Source

1. **Create Scraper** (`app/scrapers/source_name.py`)

```python
import requests
from bs4 import BeautifulSoup

def scrape_source():
    url = "https://example.com/api/players"
    response = requests.get(url)

    # Parse data
    data = response.json()

    players = []
    for item in data['players']:
        players.append({
            'name': item['name'],
            'team': item['team'],
            'role': item['position'],
            # ... more fields
        })

    return players
```

2. **Import to Database**

```python
from app.scrapers import source_name
from app.scrapers.player_importer import import_players_to_db

def update_from_source(db):
    players = source_name.scrape_source()
    imported_count = import_players_to_db(db, players)
    return imported_count
```

3. **Schedule Updates** (using Celery)

```python
# backend/app/tasks.py
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def update_player_data():
    db = SessionLocal()
    try:
        update_from_source(db)
    finally:
        db.close()

# Run daily
celery.conf.beat_schedule = {
    'update-players-daily': {
        'task': 'tasks.update_player_data',
        'schedule': crontab(hour=2, minute=0),
    },
}
```

---

## Testing

### Backend Tests

```python
# backend/tests/test_players.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_players():
    response = client.get("/api/players")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_player():
    player_data = {
        "name": "Test Player",
        "team": "Test Team",
        "role": "A"
    }
    response = client.post("/api/players", json=player_data)
    assert response.status_code == 201
```

Run tests:
```bash
cd backend
pytest
```

### Frontend Tests

```typescript
// frontend/__tests__/LoginScreen.test.tsx
import React from 'react';
import { render } from '@testing-library/react-native';
import LoginScreen from '../src/screens/auth/LoginScreen';

describe('LoginScreen', () => {
  it('renders correctly', () => {
    const { getByText } = render(<LoginScreen />);
    expect(getByText('Sign in to your account')).toBeTruthy();
  });
});
```

---

## Performance Optimization

### Backend

1. **Add Caching**

```python
from functools import lru_cache
import redis

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

@lru_cache(maxsize=100)
def get_player_cached(player_id: int):
    cache_key = f"player:{player_id}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    player = db.query(Player).filter(Player.id == player_id).first()
    redis_client.setex(cache_key, 3600, json.dumps(player))

    return player
```

2. **Database Indexing**

```python
# In models.py
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Add index
    team = Column(String, index=True)  # Add index
```

### Frontend

1. **Memoization**

```typescript
import { useMemo } from 'react';

const filteredPlayers = useMemo(() => {
  return players.filter(p => p.role === selectedRole);
}, [players, selectedRole]);
```

2. **Lazy Loading**

```typescript
import React, { lazy, Suspense } from 'react';

const PlayerDetailScreen = lazy(() => import('./screens/players/PlayerDetailScreen'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <PlayerDetailScreen />
    </Suspense>
  );
}
```

---

## Deployment

### Backend Deployment (Railway)

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Add PostgreSQL: `railway add postgresql`
5. Deploy: `railway up`

### Frontend Deployment (EAS)

```bash
# Configure EAS
eas build:configure

# Build
eas build --platform all

# Submit to stores
eas submit --platform ios
eas submit --platform android
```

---

## Best Practices

### Code Style

- **Backend**: Follow PEP 8
- **Frontend**: Use ESLint + Prettier
- **Commits**: Conventional Commits format

### Security

- Never commit `.env` files
- Use environment variables for secrets
- Validate all user inputs
- Use parameterized queries
- Implement rate limiting

### Documentation

- Document all API endpoints
- Add JSDoc/docstrings to functions
- Update README when adding features
- Keep CHANGELOG.md updated

---

## Common Tasks

### Reset Database

```bash
cd backend
python scripts/reset_db.py
python scripts/init_db.py
```

### Update Dependencies

```bash
# Backend
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# Frontend
npm update
```

### Generate API Documentation

```bash
# Access at http://localhost:8000/docs
# Or generate static docs:
cd backend
python -m pydoc -w app
```

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Native Documentation](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [React Navigation](https://reactnavigation.org/)

---

Happy developing! 🚀
