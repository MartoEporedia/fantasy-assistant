from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    rosters = relationship("Roster", back_populates="user")
    bids = relationship("Bid", back_populates="user")
    auctions = relationship("Auction", back_populates="creator")

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    team = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False, index=True)  # P, D, C, A
    secondary_role = Column(String)  # For multi-role players
    age = Column(Integer)
    nationality = Column(String)

    # Stats current season
    matches_played = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    avg_rating = Column(Float)
    fantasy_points = Column(Float, default=0)

    # Status
    is_injured = Column(Boolean, default=False)
    injury_info = Column(String)
    is_suspended = Column(Boolean, default=False)

    # Market data
    market_value = Column(Float)  # Estimated market value
    avg_auction_price = Column(Float)  # Average price in auctions

    # Additional data
    stats_history = Column(JSON)  # Historical stats
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    bids = relationship("Bid", back_populates="player")

class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    auction_type = Column(String, nullable=False)  # classic, snake, sealed, hybrid
    total_budget = Column(Integer, default=500)
    num_teams = Column(Integer, default=10)
    roster_size = Column(Integer, default=25)

    # Configuration
    roles_required = Column(JSON)  # {"P": 3, "D": 8, "C": 8, "A": 6}
    status = Column(String, default="pending")  # pending, active, completed

    creator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))

    # Relationships
    creator = relationship("User", back_populates="auctions")
    bids = relationship("Bid", back_populates="auction")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    amount = Column(Integer, nullable=False)
    is_winning = Column(Boolean, default=False)
    is_sealed = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    auction = relationship("Auction", back_populates="bids")
    user = relationship("User", back_populates="bids")
    player = relationship("Player", back_populates="bids")

class Roster(Base):
    __tablename__ = "rosters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    auction_id = Column(Integer, ForeignKey("auctions.id"))
    name = Column(String, nullable=False)

    players = Column(JSON)  # List of player IDs with purchase prices
    total_spent = Column(Integer, default=0)
    remaining_budget = Column(Integer)

    # Analysis scores
    balance_score = Column(Float)  # 0-100 score
    strength_analysis = Column(JSON)  # Detailed strength/weakness

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="rosters")

class CommunityData(Base):
    __tablename__ = "community_data"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))

    # Aggregated community stats
    times_purchased = Column(Integer, default=0)
    avg_purchase_price = Column(Float)
    min_purchase_price = Column(Float)
    max_purchase_price = Column(Float)
    popularity_score = Column(Float)  # 0-100

    week = Column(Integer)  # For weekly trends
    season = Column(String)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Fixture(Base):
    __tablename__ = "fixtures"

    id = Column(Integer, primary_key=True, index=True)
    matchday = Column(Integer, nullable=False, index=True)
    season = Column(String, nullable=False)

    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)

    match_date = Column(DateTime(timezone=True))
    home_score = Column(Integer)
    away_score = Column(Integer)

    status = Column(String, default="scheduled")  # scheduled, live, completed
    difficulty_home = Column(Float)  # 1-5 difficulty rating
    difficulty_away = Column(Float)
