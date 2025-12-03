"""
Database setup script for AuroraSync OS.
Creates all database tables based on SQLAlchemy models.

Usage:
    python scripts/setup_db.py
    python scripts/setup_db.py --drop  # Drop all tables first (WARNING: deletes data)
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db, drop_db, engine
from app.config import settings
from app.models import Base, Vehicle, Prediction, UEBAEvent


def setup_database(drop_first: bool = False):
    """
    Set up the database by creating all tables.
    
    Args:
        drop_first: If True, drop all existing tables before creating new ones
    """
    print("=" * 60)
    print("🔧 AuroraSync OS - Database Setup")
    print("=" * 60)
    print()
    
    # Display configuration
    print(f"📊 Project: {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"🗄️  Database URL: {settings.DATABASE_URL}")
    print(f"🌍 Environment: {settings.ENVIRONMENT}")
    print()
    
    # Check if we should drop tables first
    if drop_first:
        print("⚠️  WARNING: Dropping all existing tables...")
        response = input("Are you sure? This will delete all data! (yes/no): ")
        if response.lower() == "yes":
            drop_db()
            print()
        else:
            print("❌ Operation cancelled")
            return
    
    # Create tables
    print("📦 Creating database tables...")
    print()
    
    try:
        # Import all models to ensure they're registered
        print("📋 Registered models:")
        print(f"   - Vehicle")
        print(f"   - Prediction")
        print(f"   - UEBAEvent")
        print()
        
        # Create all tables
        init_db()
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print("✅ Successfully created tables:")
        for table in tables:
            print(f"   ✓ {table}")
        print()
        
        print("=" * 60)
        print("🎉 Database setup complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Start the API server: uvicorn app.main:app --reload")
        print("  2. Visit the API docs: http://localhost:8000/docs")
        print("  3. Check database connection: http://localhost:8000/api/v1/db-check")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ Error during database setup!")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        print("Troubleshooting:")
        print("  1. Ensure PostgreSQL is running")
        print("  2. Check DATABASE_URL in .env file")
        print("  3. Verify database credentials")
        print("  4. Create database if it doesn't exist:")
        print("     psql -U postgres -c 'CREATE DATABASE aurorasync;'")
        print()
        sys.exit(1)


def main():
    """
    Main function to parse arguments and run setup.
    """
    parser = argparse.ArgumentParser(
        description="Set up AuroraSync OS database"
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all existing tables before creating new ones (WARNING: deletes all data)"
    )
    
    args = parser.parse_args()
    setup_database(drop_first=args.drop)


if __name__ == "__main__":
    main()
