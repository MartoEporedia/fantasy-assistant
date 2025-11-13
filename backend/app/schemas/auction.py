from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class AuctionBase(BaseModel):
    name: str
    auction_type: str  # classic, snake, sealed, hybrid
    total_budget: int = 500
    num_teams: int = 10
    roster_size: int = 25

class AuctionCreate(AuctionBase):
    roles_required: Dict[str, int] = {"P": 3, "D": 8, "C": 8, "A": 6}

class AuctionResponse(AuctionBase):
    id: int
    roles_required: Dict[str, int]
    status: str
    creator_id: int
    created_at: datetime
    started_at: Optional[datetime]
    ended_at: Optional[datetime]

    class Config:
        from_attributes = True

class BidCreate(BaseModel):
    player_id: int
    amount: int
    is_sealed: bool = False

class BidResponse(BaseModel):
    id: int
    auction_id: int
    user_id: int
    player_id: int
    amount: int
    is_winning: bool
    is_sealed: bool
    created_at: datetime

    class Config:
        from_attributes = True

class BidAdvice(BaseModel):
    player_id: int
    player_name: str
    recommended_min: int
    recommended_max: int
    optimal_bid: int
    confidence: float  # 0-1
    reasoning: str
