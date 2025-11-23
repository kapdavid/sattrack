import httpx
from sqlalchemy.orm import Session
from app.models.satellite import Satellite
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Curated list of satellites we want to track
# Format: {norad_id: {"name": "...", "category": "..."}}
CURATED_SATELLITES = {
    # NOAA Weather satellites (polar-orbiting)
    25338: {"name": "NOAA 15", "category": "weather"},
    28654: {"name": "NOAA 18", "category": "weather"},
    33591: {"name": "NOAA 19", "category": "weather"},
    43013: {"name": "NOAA 20 (JPSS-1)", "category": "weather"},
    54234: {"name": "NOAA 21 (JPSS-2)", "category": "weather"},

    # METEOR Weather satellites (Russian polar-orbiting)
    40069: {"name": "METEOR-M 2", "category": "weather"},
    44387: {"name": "METEOR-M2 2", "category": "weather"},
    57166: {"name": "METEOR-M2 3", "category": "weather"},
    59051: {"name": "METEOR-M2 4", "category": "weather"},

    # METOP Weather satellites (European polar-orbiting)
    38771: {"name": "METOP-B", "category": "weather"},
    43689: {"name": "METOP-C", "category": "weather"},

    # FENGYUN Weather satellites (Chinese)
    43010: {"name": "FENGYUN 3D", "category": "weather"},
    49008: {"name": "FENGYUN 3E", "category": "weather"},
    57490: {"name": "FENGYUN 3F", "category": "weather"},
    56232: {"name": "FENGYUN 3G", "category": "weather"},

    # Amateur radio satellites
    27607: {"name": "SO-50 (SAUDISAT 1C)", "category": "amateur_radio"},
    43017: {"name": "AO-91 (FOX-1B)", "category": "amateur_radio"},
    43137: {"name": "AO-92 (FOX-1D)", "category": "amateur_radio"},
    40967: {"name": "LILACSAT 2", "category": "amateur_radio"},
    43678: {"name": "MOVE-2 (MOVE-II)", "category": "amateur_radio"},

    # Popular satellites
    25544: {"name": "ISS (ZARYA)", "category": "popular"},
    20580: {"name": "HST (HUBBLE)", "category": "popular"},
}


class SatelliteService:
    """Service for fetching and managing satellite TLE data."""

    CELESTRAK_BASE_URL = "https://celestrak.org/NORAD/elements/gp.php"

    @staticmethod
    async def fetch_tle_from_celestrak(norad_id: int) -> Optional[Dict[str, str]]:
        """
        Fetch TLE data for a specific satellite from CelesTrak.

        Args:
            norad_id: NORAD catalog number

        Returns:
            Dict with 'line1' and 'line2' TLE data, or None if not found
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{SatelliteService.CELESTRAK_BASE_URL}",
                    params={
                        "CATNR": norad_id,
                        "FORMAT": "tle"
                    }
                )
                response.raise_for_status()

                lines = response.text.strip().split('\n')

                # TLE format: name, line1, line2
                if len(lines) >= 3:
                    return {
                        "name": lines[0].strip(),
                        "line1": lines[1].strip(),
                        "line2": lines[2].strip()
                    }

                logger.warning(f"Invalid TLE format for NORAD ID {norad_id}")
                return None

        except httpx.HTTPError as e:
            logger.error(f"Error fetching TLE for NORAD ID {norad_id}: {e}")
            return None

    @staticmethod
    async def fetch_group_tle(group: str) -> List[Dict[str, str]]:
        """
        Fetch TLE data for an entire group from CelesTrak.

        Args:
            group: Group name (e.g., 'weather', 'amateur', 'stations')

        Returns:
            List of dicts with TLE data
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{SatelliteService.CELESTRAK_BASE_URL}",
                    params={
                        "GROUP": group,
                        "FORMAT": "tle"
                    }
                )
                response.raise_for_status()

                lines = response.text.strip().split('\n')
                satellites = []

                # Parse TLE format (name, line1, line2 repeating)
                for i in range(0, len(lines), 3):
                    if i + 2 < len(lines):
                        # Extract NORAD ID from line 1 (columns 3-7)
                        line1 = lines[i + 1].strip()
                        if len(line1) >= 7:
                            norad_id = int(line1[2:7].strip())

                            satellites.append({
                                "norad_id": norad_id,
                                "name": lines[i].strip(),
                                "line1": line1,
                                "line2": lines[i + 2].strip()
                            })

                return satellites

        except httpx.HTTPError as e:
            logger.error(f"Error fetching TLE group '{group}': {e}")
            return []

    @staticmethod
    async def seed_curated_satellites(db: Session) -> int:
        """
        Seed the database with our curated list of satellites.

        Args:
            db: Database session

        Returns:
            Number of satellites added/updated
        """
        count = 0

        for norad_id, info in CURATED_SATELLITES.items():
            # Fetch latest TLE data
            tle_data = await SatelliteService.fetch_tle_from_celestrak(norad_id)

            if not tle_data:
                logger.warning(f"Could not fetch TLE for {info['name']} ({norad_id})")
                continue

            # Check if satellite already exists
            satellite = db.query(Satellite).filter(
                Satellite.norad_id == norad_id
            ).first()

            if satellite:
                # Update existing satellite
                satellite.tle_line1 = tle_data["line1"]
                satellite.tle_line2 = tle_data["line2"]
                satellite.name = info["name"]  # Use our curated name
                logger.info(f"Updated TLE for {info['name']}")
            else:
                # Create new satellite
                satellite = Satellite(
                    norad_id=norad_id,
                    name=info["name"],
                    category=info["category"],
                    tle_line1=tle_data["line1"],
                    tle_line2=tle_data["line2"]
                )
                db.add(satellite)
                logger.info(f"Added new satellite: {info['name']}")

            count += 1

        db.commit()
        return count

    @staticmethod
    async def update_satellite_tle(db: Session, satellite_id: int) -> bool:
        """
        Update TLE data for a specific satellite.

        Args:
            db: Database session
            satellite_id: Database ID of the satellite

        Returns:
            True if successful, False otherwise
        """
        satellite = db.query(Satellite).filter(Satellite.id == satellite_id).first()

        if not satellite:
            return False

        tle_data = await SatelliteService.fetch_tle_from_celestrak(satellite.norad_id)

        if not tle_data:
            return False

        satellite.tle_line1 = tle_data["line1"]
        satellite.tle_line2 = tle_data["line2"]
        db.commit()

        return True

    @staticmethod
    def get_satellites(
        db: Session,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Satellite]:
        """
        Get satellites from database with optional filtering.

        Args:
            db: Database session
            category: Optional category filter
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Satellite objects
        """
        query = db.query(Satellite)

        if category:
            query = query.filter(Satellite.category == category)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def search_satellites(db: Session, query: str) -> List[Satellite]:
        """
        Search satellites by name.

        Args:
            db: Database session
            query: Search query string

        Returns:
            List of matching Satellite objects
        """
        return db.query(Satellite).filter(
            Satellite.name.ilike(f"%{query}%")
        ).all()
