from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.db.models import Player
from app.schemas.player import PlayerResponse, PlayerFilter, PlayerCreate

router = APIRouter()

@router.get("/", response_model=List[PlayerResponse])
def get_players(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = Query(None, description="Filter by role: P, D, C, A"),
    team: Optional[str] = Query(None, description="Filter by team"),
    search: Optional[str] = Query(None, description="Search by name"),
    db: Session = Depends(get_db)
):
    query = db.query(Player)

    if role:
        query = query.filter(Player.role == role.upper())
    if team:
        query = query.filter(Player.team == team)
    if search:
        query = query.filter(Player.name.ilike(f"%{search}%"))

    players = query.offset(skip).limit(limit).all()
    return players

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/{player_id}/stats")
def get_player_stats(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return {
        "player_id": player.id,
        "name": player.name,
        "current_season": {
            "matches_played": player.matches_played,
            "goals": player.goals,
            "assists": player.assists,
            "yellow_cards": player.yellow_cards,
            "red_cards": player.red_cards,
            "avg_rating": player.avg_rating,
            "fantasy_points": player.fantasy_points
        },
        "history": player.stats_history or {},
        "market_value": player.market_value,
        "avg_auction_price": player.avg_auction_price
    }

@router.post("/", response_model=PlayerResponse, status_code=201)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_player = Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player
