from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Auction, Bid, User, Player
from app.schemas.auction import AuctionCreate, AuctionResponse, BidCreate, BidResponse
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=AuctionResponse, status_code=201)
def create_auction(
    auction: AuctionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_auction = Auction(
        **auction.dict(),
        creator_id=current_user.id
    )
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    return db_auction

@router.get("/", response_model=List[AuctionResponse])
def get_auctions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    auctions = db.query(Auction).offset(skip).limit(limit).all()
    return auctions

@router.get("/{auction_id}", response_model=AuctionResponse)
def get_auction(auction_id: int, db: Session = Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    return auction

@router.post("/{auction_id}/bids", response_model=BidResponse, status_code=201)
def create_bid(
    auction_id: int,
    bid: BidCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify auction exists
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")

    # Verify player exists
    player = db.query(Player).filter(Player.id == bid.player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Check if user has enough budget (simplified logic)
    # TODO: Add proper budget validation

    # Mark previous bids for this player as not winning
    if not bid.is_sealed:
        db.query(Bid).filter(
            Bid.auction_id == auction_id,
            Bid.player_id == bid.player_id,
            Bid.is_winning == True
        ).update({"is_winning": False})

    # Create new bid
    db_bid = Bid(
        auction_id=auction_id,
        user_id=current_user.id,
        player_id=bid.player_id,
        amount=bid.amount,
        is_sealed=bid.is_sealed,
        is_winning=not bid.is_sealed  # Open bids are immediately winning
    )
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    return db_bid

@router.get("/{auction_id}/bids", response_model=List[BidResponse])
def get_auction_bids(
    auction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify auction exists
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")

    # Return only public bids (not sealed) or user's own sealed bids
    bids = db.query(Bid).filter(
        Bid.auction_id == auction_id
    ).filter(
        (Bid.is_sealed == False) | (Bid.user_id == current_user.id)
    ).all()

    return bids

@router.post("/{auction_id}/start")
def start_auction(
    auction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")

    if auction.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    from datetime import datetime
    auction.status = "active"
    auction.started_at = datetime.utcnow()
    db.commit()

    return {"message": "Auction started", "auction_id": auction_id}

@router.post("/{auction_id}/complete")
def complete_auction(
    auction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")

    if auction.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    from datetime import datetime
    auction.status = "completed"
    auction.ended_at = datetime.utcnow()
    db.commit()

    return {"message": "Auction completed", "auction_id": auction_id}
