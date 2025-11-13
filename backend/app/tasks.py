"""
Celery tasks for automated data updates
"""
from celery import Celery
from celery.schedules import crontab
import logging

from app.db.database import SessionLocal
from app.scrapers.data_aggregator import update_all_data

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    'fantasy_assistant',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Rome',
    enable_utc=True,
)

@celery_app.task(name='update_player_data')
def update_player_data_task():
    """
    Task to update player data from all sources
    Runs daily at 2 AM
    """
    logger.info("Starting scheduled player data update")

    db = SessionLocal()
    try:
        stats = update_all_data(db)
        logger.info(f"Player data updated: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Error updating player data: {e}")
        raise
    finally:
        db.close()

@celery_app.task(name='update_match_ratings')
def update_match_ratings_task(matchday: int = None):
    """
    Task to update player ratings after matches
    Runs on Monday mornings after weekend matches
    """
    logger.info(f"Updating match ratings for matchday {matchday}")

    from app.scrapers.gazzetta_scraper import scrape_gazzetta

    db = SessionLocal()
    try:
        data = scrape_gazzetta()

        # Update ratings
        from app.scrapers.data_aggregator import DataAggregator
        aggregator = DataAggregator(db)

        for player_rating in data.get('players', []):
            aggregator._update_player_rating(player_rating)

        db.commit()
        logger.info(f"Updated ratings for {len(data.get('players', []))} players")

        return {'updated': len(data.get('players', []))}

    except Exception as e:
        logger.error(f"Error updating ratings: {e}")
        db.rollback()
        raise
    finally:
        db.close()

@celery_app.task(name='update_injury_status')
def update_injury_status_task():
    """
    Task to check and update player injury/suspension status
    Runs multiple times per day
    """
    logger.info("Checking injury and suspension updates")

    from app.scrapers.gazzetta_scraper import scrape_gazzetta

    db = SessionLocal()
    try:
        data = scrape_gazzetta()

        # Update injury status
        from app.scrapers.data_aggregator import DataAggregator
        aggregator = DataAggregator(db)

        for injury_update in data.get('injuries', []):
            aggregator._update_injury_status(injury_update)

        db.commit()
        logger.info(f"Updated injury status for {len(data.get('injuries', []))} players")

        return {'updated': len(data.get('injuries', []))}

    except Exception as e:
        logger.error(f"Error updating injury status: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Schedule periodic tasks
celery_app.conf.beat_schedule = {
    # Update all player data daily at 2 AM
    'update-players-daily': {
        'task': 'update_player_data',
        'schedule': crontab(hour=2, minute=0),
    },

    # Update match ratings on Monday mornings at 6 AM
    'update-ratings-monday': {
        'task': 'update_match_ratings',
        'schedule': crontab(day_of_week=1, hour=6, minute=0),
    },

    # Check injuries 3 times a day (9 AM, 3 PM, 9 PM)
    'check-injuries-morning': {
        'task': 'update_injury_status',
        'schedule': crontab(hour=9, minute=0),
    },
    'check-injuries-afternoon': {
        'task': 'update_injury_status',
        'schedule': crontab(hour=15, minute=0),
    },
    'check-injuries-evening': {
        'task': 'update_injury_status',
        'schedule': crontab(hour=21, minute=0),
    },
}
