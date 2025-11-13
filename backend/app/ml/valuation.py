"""
Player valuation module using ML for bid recommendations
"""
from typing import Dict
from sqlalchemy.orm import Session
from app.db.models import Player, Bid
import numpy as np

def calculate_player_value(player: Player) -> float:
    """
    Calculate estimated value for a player based on stats and attributes.
    This is a simplified heuristic model. In production, use trained ML model.
    """
    base_value = 1.0

    # Role multipliers
    role_multipliers = {
        "P": 1.0,  # Goalkeeper
        "D": 1.1,  # Defender
        "C": 1.3,  # Midfielder
        "A": 1.5   # Forward
    }

    role_mult = role_multipliers.get(player.role, 1.0)
    base_value *= role_mult

    # Stats contribution
    if player.matches_played and player.matches_played > 0:
        # Goals and assists
        goal_value = player.goals * 3.0
        assist_value = player.assists * 2.0

        # Average rating bonus
        if player.avg_rating:
            rating_bonus = max(0, (player.avg_rating - 6.0) * 5.0)
        else:
            rating_bonus = 0

        # Fantasy points
        fantasy_bonus = (player.fantasy_points / 10.0) if player.fantasy_points else 0

        stats_value = goal_value + assist_value + rating_bonus + fantasy_bonus
        base_value += stats_value

    # Market value consideration
    if player.market_value:
        market_factor = player.market_value / 10.0
        base_value = (base_value + market_factor) / 2.0

    # Historical auction price
    if player.avg_auction_price:
        base_value = (base_value + player.avg_auction_price) / 2.0

    # Age factor (peak at 25-28)
    if player.age:
        if 25 <= player.age <= 28:
            age_factor = 1.1
        elif player.age < 23:
            age_factor = 0.9
        elif player.age > 30:
            age_factor = 0.85
        else:
            age_factor = 1.0
        base_value *= age_factor

    # Status penalties
    if player.is_injured:
        base_value *= 0.7
    if player.is_suspended:
        base_value *= 0.8

    return max(1.0, base_value)  # Minimum value of 1


def get_bid_recommendation(
    player: Player,
    estimated_value: float,
    remaining_budget: int,
    db: Session,
    auction_id: int
) -> Dict:
    """
    Get bid recommendation with min, max, and optimal values.
    """
    # Base recommendations around estimated value
    optimal_bid = int(estimated_value)
    min_bid = max(1, int(estimated_value * 0.8))
    max_bid = int(estimated_value * 1.3)

    # Adjust based on remaining budget
    if remaining_budget < max_bid:
        max_bid = remaining_budget

    if remaining_budget < optimal_bid:
        optimal_bid = remaining_budget

    # Check recent bids in this auction
    recent_bids = db.query(Bid).filter(
        Bid.auction_id == auction_id,
        Bid.player_id == player.id
    ).order_by(Bid.created_at.desc()).limit(5).all()

    if recent_bids:
        highest_bid = max(bid.amount for bid in recent_bids)
        # Adjust recommendations if there's active bidding
        if highest_bid > min_bid:
            min_bid = highest_bid + 1
            optimal_bid = max(optimal_bid, highest_bid + 2)

    # Confidence based on data availability
    confidence = 0.5
    if player.matches_played and player.matches_played > 5:
        confidence += 0.2
    if player.avg_rating:
        confidence += 0.1
    if player.avg_auction_price:
        confidence += 0.2

    confidence = min(1.0, confidence)

    # Generate reasoning
    reasoning_parts = []
    if player.avg_rating and player.avg_rating > 6.5:
        reasoning_parts.append(f"Strong performer with {player.avg_rating:.1f} avg rating")
    if player.goals > 5:
        reasoning_parts.append(f"{player.goals} goals this season")
    if player.is_injured:
        reasoning_parts.append("Currently injured - risky pick")
    if remaining_budget < estimated_value * 1.5:
        reasoning_parts.append("Budget constrained")

    reasoning = ". ".join(reasoning_parts) if reasoning_parts else "Based on statistical analysis"

    return {
        "min": min_bid,
        "max": max_bid,
        "optimal": optimal_bid,
        "confidence": confidence,
        "reasoning": reasoning,
        "estimated_value": estimated_value
    }


def train_valuation_model(db: Session):
    """
    Train ML model for player valuation.
    This is a placeholder for future ML implementation using scikit-learn or similar.
    """
    # TODO: Implement ML model training
    # - Collect historical auction data
    # - Feature engineering (stats, role, age, team, etc.)
    # - Train regression model
    # - Save model for inference
    pass
