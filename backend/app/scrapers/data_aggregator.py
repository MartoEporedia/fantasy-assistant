"""
Data aggregator and updater - combines data from multiple sources
"""
from sqlalchemy.orm import Session
from typing import List, Dict
import logging
from datetime import datetime

from app.db.models import Player, Fixture, CommunityData
from app.scrapers.fantacalcio_scraper import scrape_fantacalcio
from app.scrapers.gazzetta_scraper import scrape_gazzetta

logger = logging.getLogger(__name__)

class DataAggregator:
    """Aggregates and updates player data from multiple sources"""

    def __init__(self, db: Session):
        self.db = db

    def update_all_players(self) -> Dict[str, int]:
        """
        Update all players from all available sources
        Returns statistics about updated data
        """
        stats = {
            'updated': 0,
            'created': 0,
            'errors': 0,
        }

        # Fetch from Fantacalcio.it
        try:
            fantacalcio_players = scrape_fantacalcio()
            logger.info(f"Fetched {len(fantacalcio_players)} players from Fantacalcio.it")

            for player_data in fantacalcio_players:
                try:
                    result = self._upsert_player(player_data)
                    if result == 'created':
                        stats['created'] += 1
                    elif result == 'updated':
                        stats['updated'] += 1
                except Exception as e:
                    logger.error(f"Error upserting player: {e}")
                    stats['errors'] += 1

            self.db.commit()

        except Exception as e:
            logger.error(f"Error fetching from Fantacalcio: {e}")
            self.db.rollback()

        # Fetch from Gazzetta
        try:
            gazzetta_data = scrape_gazzetta()

            # Update player ratings
            for player_rating in gazzetta_data.get('players', []):
                try:
                    self._update_player_rating(player_rating)
                except Exception as e:
                    logger.error(f"Error updating rating: {e}")

            # Update injury status
            for injury_update in gazzetta_data.get('injuries', []):
                try:
                    self._update_injury_status(injury_update)
                except Exception as e:
                    logger.error(f"Error updating injury: {e}")

            # Update fixture difficulty
            self._update_fixtures(gazzetta_data.get('fixture_difficulty', {}))

            self.db.commit()

        except Exception as e:
            logger.error(f"Error processing Gazzetta data: {e}")
            self.db.rollback()

        logger.info(f"Update complete: {stats}")
        return stats

    def _upsert_player(self, player_data: Dict) -> str:
        """
        Insert or update player
        Returns 'created' or 'updated'
        """
        # Try to find existing player
        existing = self.db.query(Player).filter(
            Player.name == player_data['name'],
            Player.team == player_data['team']
        ).first()

        if existing:
            # Update existing player
            for key, value in player_data.items():
                if hasattr(existing, key) and value is not None:
                    setattr(existing, key, value)

            existing.updated_at = datetime.utcnow()
            return 'updated'
        else:
            # Create new player
            new_player = Player(**player_data)
            self.db.add(new_player)
            return 'created'

    def _update_player_rating(self, rating_data: Dict):
        """Update player's current rating and stats"""
        player = self.db.query(Player).filter(
            Player.name == rating_data['name']
        ).first()

        if player:
            # Update current season stats
            if 'rating' in rating_data and rating_data['rating'] > 0:
                # Calculate new average rating
                if player.avg_rating and player.matches_played > 0:
                    total_rating = player.avg_rating * player.matches_played
                    player.matches_played += 1
                    player.avg_rating = (total_rating + rating_data['rating']) / player.matches_played
                else:
                    player.avg_rating = rating_data['rating']
                    player.matches_played = 1

            if 'goals' in rating_data:
                player.goals = (player.goals or 0) + rating_data['goals']

            if 'assists' in rating_data:
                player.assists = (player.assists or 0) + rating_data['assists']

            if 'fantasy_points' in rating_data:
                player.fantasy_points = (player.fantasy_points or 0) + rating_data['fantasy_points']

            player.updated_at = datetime.utcnow()

    def _update_injury_status(self, injury_data: Dict):
        """Update player injury/suspension status"""
        player = self.db.query(Player).filter(
            Player.name == injury_data['name']
        ).first()

        if player:
            player.is_injured = injury_data.get('is_injured', False)
            player.is_suspended = injury_data.get('is_suspended', False)

            if injury_data.get('is_injured'):
                player.injury_info = injury_data.get('status', 'Injured')
            else:
                player.injury_info = None

            player.updated_at = datetime.utcnow()

    def _update_fixtures(self, fixture_data: Dict):
        """Update fixture difficulty ratings"""
        for team, data in fixture_data.items():
            for fixture in data.get('next_5', []):
                # Check if fixture exists
                existing = self.db.query(Fixture).filter(
                    Fixture.home_team == team if fixture['home'] else Fixture.away_team == team,
                    Fixture.status == 'scheduled'
                ).first()

                if existing:
                    if fixture['home']:
                        existing.difficulty_home = fixture['difficulty']
                    else:
                        existing.difficulty_away = fixture['difficulty']

    def get_update_statistics(self) -> Dict:
        """Get statistics about data freshness"""
        from sqlalchemy import func

        total_players = self.db.query(func.count(Player.id)).scalar()

        # Players updated in last 24 hours
        from datetime import timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)

        recent_updates = self.db.query(func.count(Player.id)).filter(
            Player.updated_at >= yesterday
        ).scalar()

        injured_players = self.db.query(func.count(Player.id)).filter(
            Player.is_injured == True
        ).scalar()

        suspended_players = self.db.query(func.count(Player.id)).filter(
            Player.is_suspended == True
        ).scalar()

        return {
            'total_players': total_players,
            'updated_last_24h': recent_updates,
            'injured': injured_players,
            'suspended': suspended_players,
        }


def update_all_data(db: Session) -> Dict:
    """Main function to update all data"""
    aggregator = DataAggregator(db)
    return aggregator.update_all_players()
