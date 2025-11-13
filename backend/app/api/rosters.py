from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Roster, User, Player, Bid
from app.schemas.roster import RosterCreate, RosterResponse, RosterAnalysis
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=RosterResponse, status_code=201)
def create_roster(
    roster: RosterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_roster = Roster(
        **roster.dict(),
        user_id=current_user.id,
        players=[],
        total_spent=0
    )
    db.add(db_roster)
    db.commit()
    db.refresh(db_roster)
    return db_roster

@router.get("/", response_model=List[RosterResponse])
def get_user_rosters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rosters = db.query(Roster).filter(Roster.user_id == current_user.id).all()
    return rosters

@router.get("/{roster_id}", response_model=RosterResponse)
def get_roster(
    roster_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roster = db.query(Roster).filter(Roster.id == roster_id).first()
    if not roster:
        raise HTTPException(status_code=404, detail="Roster not found")

    if roster.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return roster

@router.get("/{roster_id}/details")
def get_roster_details(
    roster_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roster = db.query(Roster).filter(Roster.id == roster_id).first()
    if not roster:
        raise HTTPException(status_code=404, detail="Roster not found")

    if roster.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Get full player details
    player_ids = [p["player_id"] for p in roster.players] if roster.players else []
    players = db.query(Player).filter(Player.id.in_(player_ids)).all() if player_ids else []

    players_details = []
    for player in players:
        player_info = next((p for p in roster.players if p["player_id"] == player.id), None)
        players_details.append({
            "id": player.id,
            "name": player.name,
            "team": player.team,
            "role": player.role,
            "purchase_price": player_info["purchase_price"] if player_info else 0,
            "current_stats": {
                "goals": player.goals,
                "assists": player.assists,
                "avg_rating": player.avg_rating,
                "fantasy_points": player.fantasy_points
            }
        })

    return {
        "roster": roster,
        "players": players_details
    }

@router.post("/{roster_id}/import-from-auction/{auction_id}")
def import_roster_from_auction(
    roster_id: int,
    auction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roster = db.query(Roster).filter(Roster.id == roster_id).first()
    if not roster:
        raise HTTPException(status_code=404, detail="Roster not found")

    if roster.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Get winning bids for this user in the auction
    winning_bids = db.query(Bid).filter(
        Bid.auction_id == auction_id,
        Bid.user_id == current_user.id,
        Bid.is_winning == True
    ).all()

    players_list = []
    total_spent = 0

    for bid in winning_bids:
        player = db.query(Player).filter(Player.id == bid.player_id).first()
        if player:
            players_list.append({
                "player_id": player.id,
                "player_name": player.name,
                "role": player.role,
                "purchase_price": bid.amount
            })
            total_spent += bid.amount

    roster.players = players_list
    roster.total_spent = total_spent
    roster.auction_id = auction_id
    db.commit()

    return {"message": "Roster imported successfully", "players_count": len(players_list)}
