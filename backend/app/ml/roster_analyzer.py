"""
Roster analysis module for evaluating team balance and quality
"""
from typing import Dict, List
from sqlalchemy.orm import Session
from app.db.models import Roster, Player

def analyze_roster(roster: Roster, db: Session) -> Dict:
    """
    Analyze roster balance, quality, and depth.
    Returns scores and recommendations.
    """
    if not roster.players:
        return {
            "balance_score": 0,
            "role_distribution": {},
            "strengths": [],
            "weaknesses": ["No players in roster"],
            "suggested_improvements": ["Add players to your roster"],
            "quality_score": 0,
            "depth_score": 0
        }

    # Get player IDs from roster
    player_ids = [p["player_id"] for p in roster.players]
    players = db.query(Player).filter(Player.id.in_(player_ids)).all()

    # Role distribution
    role_distribution = {"P": 0, "D": 0, "C": 0, "A": 0}
    for player in players:
        role_distribution[player.role] = role_distribution.get(player.role, 0) + 1

    # Calculate balance score
    ideal_distribution = {"P": 3, "D": 8, "C": 8, "A": 6}
    balance_scores = []

    for role, ideal_count in ideal_distribution.items():
        actual_count = role_distribution.get(role, 0)
        if ideal_count > 0:
            role_balance = min(1.0, actual_count / ideal_count)
            balance_scores.append(role_balance)

    balance_score = (sum(balance_scores) / len(balance_scores)) * 100 if balance_scores else 0

    # Quality score (based on player stats)
    quality_scores = []
    for player in players:
        player_quality = 50  # Base score

        if player.avg_rating:
            player_quality += (player.avg_rating - 6.0) * 10

        if player.fantasy_points:
            player_quality += min(20, player.fantasy_points / 10)

        quality_scores.append(min(100, max(0, player_quality)))

    quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0

    # Depth score (how many quality players per role)
    depth_score = 0
    for role, count in role_distribution.items():
        role_players = [p for p in players if p.role == role]
        quality_players = [
            p for p in role_players
            if p.avg_rating and p.avg_rating > 6.0
        ]
        role_depth = (len(quality_players) / max(1, count)) * 100
        depth_score += role_depth

    depth_score = depth_score / 4 if depth_score > 0 else 0  # Average across 4 roles

    # Identify strengths
    strengths = []
    if quality_score > 70:
        strengths.append("High quality players overall")
    if depth_score > 70:
        strengths.append("Good depth in all positions")

    for role, count in role_distribution.items():
        ideal = ideal_distribution.get(role, 0)
        if count >= ideal:
            role_name = {"P": "Goalkeepers", "D": "Defenders", "C": "Midfielders", "A": "Forwards"}[role]
            strengths.append(f"Good coverage in {role_name}")

    # Identify weaknesses
    weaknesses = []
    for role, count in role_distribution.items():
        ideal = ideal_distribution.get(role, 0)
        if count < ideal * 0.7:
            role_name = {"P": "Goalkeepers", "D": "Defenders", "C": "Midfielders", "A": "Forwards"}[role]
            weaknesses.append(f"Lacking {role_name} ({count}/{ideal})")

    injured_players = [p for p in players if p.is_injured]
    if len(injured_players) > 3:
        weaknesses.append(f"Too many injured players ({len(injured_players)})")

    # Suggested improvements
    suggested_improvements = []
    for role, count in role_distribution.items():
        ideal = ideal_distribution.get(role, 0)
        if count < ideal:
            role_name = {"P": "Goalkeeper", "D": "Defender", "C": "Midfielder", "A": "Forward"}[role]
            needed = ideal - count
            suggested_improvements.append(f"Add {needed} more {role_name}(s)")

    if quality_score < 60:
        suggested_improvements.append("Consider upgrading low-performing players")

    if not suggested_improvements:
        suggested_improvements.append("Roster looks balanced!")

    return {
        "balance_score": round(balance_score, 1),
        "role_distribution": role_distribution,
        "strengths": strengths if strengths else ["Building a competitive roster"],
        "weaknesses": weaknesses if weaknesses else ["No major weaknesses detected"],
        "suggested_improvements": suggested_improvements,
        "quality_score": round(quality_score, 1),
        "depth_score": round(depth_score, 1)
    }
