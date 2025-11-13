from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class PlayerBase(BaseModel):
    name: str
    team: str
    role: str
    secondary_role: Optional[str] = None
    age: Optional[int] = None
    nationality: Optional[str] = None

class PlayerCreate(PlayerBase):
    pass

class PlayerStats(BaseModel):
    matches_played: int = 0
    goals: int = 0
    assists: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    avg_rating: Optional[float] = None
    fantasy_points: float = 0

class PlayerResponse(PlayerBase):
    id: int
    matches_played: int
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int
    avg_rating: Optional[float]
    fantasy_points: float
    is_injured: bool
    injury_info: Optional[str]
    is_suspended: bool
    market_value: Optional[float]
    avg_auction_price: Optional[float]
    stats_history: Optional[Dict[str, Any]]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class PlayerFilter(BaseModel):
    role: Optional[str] = None
    team: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    available_only: bool = True
