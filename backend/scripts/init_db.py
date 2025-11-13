"""
Initialize database with tables and sample data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.database import engine, SessionLocal, Base
from app.db.models import *
from app.scrapers.player_importer import import_sample_data, import_players_to_db

def init_database():
    """Create all tables and import sample data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")

    print("\nImporting sample player data...")
    db = SessionLocal()
    try:
        players_data = import_sample_data()
        imported_count = import_players_to_db(db, players_data)
        print(f"✓ Imported {imported_count} players")
    except Exception as e:
        print(f"✗ Error importing data: {e}")
        db.rollback()
    finally:
        db.close()

    print("\n✓ Database initialization complete!")

if __name__ == "__main__":
    init_database()
