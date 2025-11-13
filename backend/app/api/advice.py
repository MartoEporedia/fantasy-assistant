from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Player, Roster, Bid, User
from app.schemas.auction import BidAdvice
from app.schemas.roster import RosterAnalysis, TradeAdvice
from app.api.auth import get_current_user
from app.ml.valuation import calculate_player_value, get_bid_recommendation
from app.ml.roster_analyzer import analyze_roster

router = APIRouter()

@router.get("/bid/{player_id}", response_model=BidAdvice)
def get_bid_advice(
    player_id: int,
    auction_id: int,
    remaining_budget: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get player value estimation
    estimated_value = calculate_player_value(player)

    # Get bid recommendation based on auction context
    bid_recommendation = get_bid_recommendation(
        player=player,
        estimated_value=estimated_value,
        remaining_budget=remaining_budget,
        db=db,
        auction_id=auction_id
    )

    return BidAdvice(
        player_id=player.id,
        player_name=player.name,
        recommended_min=bid_recommendation["min"],
        recommended_max=bid_recommendation["max"],
        optimal_bid=bid_recommendation["optimal"],
        confidence=bid_recommendation["confidence"],
        reasoning=bid_recommendation["reasoning"]
    )

@router.get("/roster/{roster_id}", response_model=RosterAnalysis)
def get_roster_advice(
    roster_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roster = db.query(Roster).filter(Roster.id == roster_id).first()
    if not roster:
        raise HTTPException(status_code=404, detail="Roster not found")

    if roster.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Analyze roster
    analysis = analyze_roster(roster, db)

    # Update roster with analysis scores
    roster.balance_score = analysis["balance_score"]
    roster.strength_analysis = {
        "strengths": analysis["strengths"],
        "weaknesses": analysis["weaknesses"]
    }
    db.commit()

    return RosterAnalysis(
        roster_id=roster.id,
        balance_score=analysis["balance_score"],
        role_distribution=analysis["role_distribution"],
        strengths=analysis["strengths"],
        weaknesses=analysis["weaknesses"],
        suggested_improvements=analysis["suggested_improvements"],
        quality_score=analysis["quality_score"],
        depth_score=analysis["depth_score"]
    )

@router.get("/trades/{roster_id}", response_model=List[TradeAdvice])
def get_trade_advice(
    roster_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roster = db.query(Roster).filter(Roster.id == roster_id).first()
    if not roster:
        raise HTTPException(status_code=404, detail="Roster not found")

    if roster.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # TODO: Implement trade recommendation algorithm
    # For now, return empty list
    return []

@router.get("/lineup/{roster_id}/{matchday}")
def get_lineup_advice(
    roster_id: int,
    matchday: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roster = db.query(Roster).filter(Roster.id == roster_id).first()
    if not roster:
        raise HTTPException(status_code=404, detail="Roster not found")

    if roster.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # TODO: Implement lineup recommendation based on fixtures, form, injuries
    # For now, return basic structure
    return {
        "matchday": matchday,
        "recommended_lineup": {
            "goalkeeper": [],
            "defenders": [],
            "midfielders": [],
            "forwards": []
        },
        "captain_suggestion": None,
        "notes": []
    }
