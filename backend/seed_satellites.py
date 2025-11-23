#!/usr/bin/env python3
"""
Script to seed the database with curated satellites.
Run this to populate the database with initial satellite data.
"""
import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.services.satellite_service import SatelliteService


async def main():
    """Seed the database with satellites."""
    print("Starting satellite database seeding...")

    db = SessionLocal()
    try:
        count = await SatelliteService.seed_curated_satellites(db)
        print(f"✅ Successfully added/updated {count} satellites!")

        # Display what was added
        from app.models.satellite import Satellite

        satellites = db.query(Satellite).all()
        print(f"\nTotal satellites in database: {len(satellites)}\n")

        # Group by category
        by_category = {}
        for sat in satellites:
            if sat.category not in by_category:
                by_category[sat.category] = []
            by_category[sat.category].append(sat.name)

        for category, names in sorted(by_category.items()):
            print(f"{category.upper()}:")
            for name in sorted(names):
                print(f"  - {name}")
            print()

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
