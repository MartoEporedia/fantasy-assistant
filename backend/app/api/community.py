from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.db.database import get_db
from app.db.models import CommunityData, Player, Bid

router = APIRouter()

@router.get("/trends")
def get_community_trends(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    # Get most popular players
    popular_players = db.query(
        CommunityData.player_id,
        CommunityData.times_purchased,
        CommunityData.avg_purchase_price,
        Player.name,
        Player.team,
        Player.role
    ).join(
        Player, CommunityData.player_id == Player.id
    ).order_by(
        desc(CommunityData.popularity_score)
    ).limit(limit).all()

    return {
        "popular_players": [
            {
                "player_id": p.player_id,
                "name": p.name,
                "team": p.team,
                "role": p.role,
                "times_purchased": p.times_purchased,
                "avg_price": p.avg_purchase_price
            }
            for p in popular_players
        ]
    }

@router.get("/player-trends/{player_id}")
def get_player_trends(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        return {"error": "Player not found"}

    community_data = db.query(CommunityData).filter(
        CommunityData.player_id == player_id
    ).first()

    # Get recent bids for this player
    recent_bids = db.query(Bid).filter(
        Bid.player_id == player_id,
        Bid.is_winning == True
    ).order_by(desc(Bid.created_at)).limit(10).all()

    return {
        "player": {
            "id": player.id,
            "name": player.name,
            "team": player.team,
            "role": player.role
        },
        "community_stats": {
            "times_purchased": community_data.times_purchased if community_data else 0,
            "avg_price": community_data.avg_purchase_price if community_data else None,
            "min_price": community_data.min_purchase_price if community_data else None,
            "max_price": community_data.max_purchase_price if community_data else None,
            "popularity_score": community_data.popularity_score if community_data else 0
        },
        "recent_purchases": [
            {
                "amount": bid.amount,
                "date": bid.created_at
            }
            for bid in recent_bids
        ]
    }
