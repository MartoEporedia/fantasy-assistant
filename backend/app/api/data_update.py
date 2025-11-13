from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.scrapers.data_aggregator import update_all_data, DataAggregator
from app.api.auth import get_current_user
from app.db.models import User

router = APIRouter()

@router.post("/update/all")
def trigger_full_update(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manually trigger a full data update from all sources.
    This runs in the background.
    """
    background_tasks.add_task(update_all_data, db)

    return {
        "message": "Data update started in background",
        "status": "processing"
    }

@router.get("/update/status")
def get_update_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get statistics about data freshness and last update
    """
    aggregator = DataAggregator(db)
    stats = aggregator.get_update_statistics()

    return {
        "status": "ok",
        "statistics": stats
    }

@router.post("/update/injuries")
def update_injuries(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update only injury and suspension status
    """
    from app.scrapers.gazzetta_scraper import scrape_gazzetta

    def update_task():
        data = scrape_gazzetta()
        aggregator = DataAggregator(db)

        for injury_update in data.get('injuries', []):
            aggregator._update_injury_status(injury_update)

        db.commit()

    background_tasks.add_task(update_task)

    return {
        "message": "Injury status update started",
        "status": "processing"
    }

@router.post("/update/ratings/{matchday}")
def update_matchday_ratings(
    matchday: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update player ratings for a specific matchday
    """
    from app.scrapers.gazzetta_scraper import scrape_gazzetta

    def update_task():
        data = scrape_gazzetta()
        aggregator = DataAggregator(db)

        for player_rating in data.get('players', []):
            aggregator._update_player_rating(player_rating)

        db.commit()

    background_tasks.add_task(update_task)

    return {
        "message": f"Ratings update for matchday {matchday} started",
        "matchday": matchday,
        "status": "processing"
    }
