from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class RosterBase(BaseModel):
    name: str

class RosterCreate(RosterBase):
    auction_id: Optional[int] = None

class PlayerInRoster(BaseModel):
    player_id: int
    player_name: str
    role: str
    purchase_price: int

class RosterResponse(RosterBase):
    id: int
    user_id: int
    auction_id: Optional[int]
    players: List[Dict[str, Any]]
    total_spent: int
    remaining_budget: Optional[int]
    balance_score: Optional[float]
    strength_analysis: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class RosterAnalysis(BaseModel):
    roster_id: int
    balance_score: float  # 0-100
    role_distribution: Dict[str, int]
    strengths: List[str]
    weaknesses: List[str]
    suggested_improvements: List[str]
    quality_score: float  # 0-100
    depth_score: float  # 0-100

class TradeAdvice(BaseModel):
    give_player_id: int
    receive_player_id: int
    reasoning: str
    impact_score: float  # -100 to +100
