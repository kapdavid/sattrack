from skyfield.api import load, wgs84, EarthSatellite, utc
from skyfield.toposlib import GeographicPosition
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

# Load Skyfield timescale (will download data files on first run)
ts = load.timescale()


class OrbitalService:
    """Service for calculating satellite positions and pass predictions."""

    @staticmethod
    def create_satellite(name: str, tle_line1: str, tle_line2: str) -> EarthSatellite:
        """
        Create a Skyfield EarthSatellite object from TLE data.

        Args:
            name: Satellite name
            tle_line1: First line of TLE
            tle_line2: Second line of TLE

        Returns:
            EarthSatellite object
        """
        return EarthSatellite(tle_line1, tle_line2, name, ts)

    @staticmethod
    def get_current_position(satellite: EarthSatellite) -> Dict[str, float]:
        """
        Get current position of a satellite.

        Args:
            satellite: Skyfield EarthSatellite object

        Returns:
            Dict with latitude, longitude, altitude_km
        """
        t = ts.now()
        geocentric = satellite.at(t)
        subpoint = wgs84.subpoint(geocentric)

        return {
            "latitude": subpoint.latitude.degrees,
            "longitude": subpoint.longitude.degrees,
            "altitude_km": subpoint.elevation.km,
            "timestamp": t.utc_datetime()
        }

    @staticmethod
    def calculate_pass_quality(max_elevation: float, duration_seconds: int) -> float:
        """
        Calculate a quality score for a satellite pass (0-100).

        Higher scores indicate better passes:
        - Higher maximum elevation = better
        - Longer duration = better

        Args:
            max_elevation: Maximum elevation in degrees (0-90)
            duration_seconds: Pass duration in seconds

        Returns:
            Quality score (0-100)
        """
        # Elevation score (0-70 points)
        # Passes above 45° get near-perfect score
        elevation_score = min(70, (max_elevation / 45.0) * 70)

        # Duration score (0-30 points)
        # 10 minutes or longer gets full score
        duration_minutes = duration_seconds / 60
        duration_score = min(30, (duration_minutes / 10.0) * 30)

        return round(elevation_score + duration_score, 1)

    @staticmethod
    def find_passes(
        satellite: EarthSatellite,
        observer_lat: float,
        observer_lon: float,
        start_time: datetime,
        end_time: datetime,
        min_elevation: float = 10.0
    ) -> List[Dict]:
        """
        Find all passes of a satellite over a location.

        Args:
            satellite: Skyfield EarthSatellite object
            observer_lat: Observer latitude in degrees
            observer_lon: Observer longitude in degrees
            start_time: Start of prediction window
            end_time: End of prediction window
            min_elevation: Minimum elevation to consider (degrees)

        Returns:
            List of pass dictionaries with AOS, LOS, max_elevation, etc.
        """
        # Create observer location
        observer = wgs84.latlon(observer_lat, observer_lon)

        # Ensure datetimes are timezone-aware (UTC)
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

        # Convert times to Skyfield time objects
        t0 = ts.from_datetime(start_time)
        t1 = ts.from_datetime(end_time)

        # Find events (rise, culminate, set)
        t, events = satellite.find_events(observer, t0, t1, altitude_degrees=min_elevation)

        passes = []
        current_pass = {}

        for ti, event in zip(t, events):
            if event == 0:  # Rise (AOS - Acquisition of Signal)
                current_pass = {
                    "aos_time": ti.utc_datetime(),
                    "aos_azimuth": None,
                }

            elif event == 1:  # Culminate (maximum elevation)
                if current_pass:
                    # Calculate elevation and azimuth at culmination
                    difference = satellite.at(ti) - observer.at(ti)
                    topocentric = difference.altaz()

                    current_pass["max_elevation"] = topocentric[0].degrees
                    current_pass["max_azimuth"] = topocentric[1].degrees

            elif event == 2:  # Set (LOS - Loss of Signal)
                if current_pass and "max_elevation" in current_pass:
                    current_pass["los_time"] = ti.utc_datetime()

                    # Calculate duration
                    duration = (current_pass["los_time"] - current_pass["aos_time"]).total_seconds()
                    current_pass["duration"] = int(duration)

                    # Calculate quality score
                    current_pass["quality_score"] = OrbitalService.calculate_pass_quality(
                        current_pass["max_elevation"],
                        current_pass["duration"]
                    )

                    # Calculate AOS and LOS azimuths
                    aos_time = ts.from_datetime(current_pass["aos_time"])
                    los_time = ts.from_datetime(current_pass["los_time"])

                    aos_diff = satellite.at(aos_time) - observer.at(aos_time)
                    los_diff = satellite.at(los_time) - observer.at(los_time)

                    current_pass["aos_azimuth"] = aos_diff.altaz()[1].degrees
                    current_pass["los_azimuth"] = los_diff.altaz()[1].degrees

                    passes.append(current_pass)
                    current_pass = {}

        return passes

    @staticmethod
    def predict_passes(
        name: str,
        tle_line1: str,
        tle_line2: str,
        observer_lat: float,
        observer_lon: float,
        days_ahead: int = 7,
        min_elevation: float = 10.0
    ) -> List[Dict]:
        """
        Predict satellite passes for the next N days.

        Args:
            name: Satellite name
            tle_line1: First line of TLE
            tle_line2: Second line of TLE
            observer_lat: Observer latitude
            observer_lon: Observer longitude
            days_ahead: Number of days to predict (default 7)
            min_elevation: Minimum elevation in degrees (default 10)

        Returns:
            List of pass predictions
        """
        try:
            satellite = OrbitalService.create_satellite(name, tle_line1, tle_line2)

            start_time = datetime.now(timezone.utc)
            end_time = start_time + timedelta(days=days_ahead)

            passes = OrbitalService.find_passes(
                satellite=satellite,
                observer_lat=observer_lat,
                observer_lon=observer_lon,
                start_time=start_time,
                end_time=end_time,
                min_elevation=min_elevation
            )

            return passes

        except Exception as e:
            logger.error(f"Error predicting passes for {name}: {e}")
            return []
