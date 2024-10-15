import math
from datetime import datetime
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy import units as u
from star_database import StarDatabase

def calculate_location(solved_data, observation_time):
    db = StarDatabase()
    stars = db.get_all_stars()

    # Find matching stars in the database
    matched_stars = []
    for solved_star in solved_data['stars']:
        solved_coord = SkyCoord(solved_star['ra'], solved_star['dec'], unit=(u.deg, u.deg))
        for db_star in stars:
            db_coord = SkyCoord(db_star[2], db_star[3], unit=(u.deg, u.deg))
            if solved_coord.separation(db_coord) < 0.1 * u.deg:
                matched_stars.append((solved_star, db_star))

    if len(matched_stars) < 3:
        raise ValueError("Not enough stars matched for location calculation")

    # Initial guess (center of the Earth)
    lat_guess, lon_guess = 0, 0

    for _ in range(3):  # Iterate to improve accuracy
        location = EarthLocation(lat=lat_guess*u.deg, lon=lon_guess*u.deg)
        obstime = Time(observation_time)

        sum_dlat, sum_dlon, weight_sum = 0, 0, 0

        for solved_star, db_star in matched_stars:
            star_coord = SkyCoord(db_star[2], db_star[3], unit=(u.deg, u.deg))
            
            altaz = star_coord.transform_to(AltAz(obstime=obstime, location=location))
            
            # Calculate intercept
            observed_altitude = solved_star['altitude']
            calculated_altitude = altaz.alt.deg
            intercept = observed_altitude - calculated_altitude

            # Calculate azimuth
            azimuth = altaz.az.deg

            # Calculate position line endpoints
            dlat = intercept * math.cos(math.radians(azimuth))
            dlon = intercept * math.sin(math.radians(azimuth)) / math.cos(math.radians(lat_guess))

            # Weight based on star brightness (lower magnitude = brighter = higher weight)
            weight = 1 / (db_star[4] + 1)  # Add 1 to avoid division by zero

            sum_dlat += dlat * weight
            sum_dlon += dlon * weight
            weight_sum += weight

        # Calculate weighted average corrections
        avg_dlat = sum_dlat / weight_sum
        avg_dlon = sum_dlon / weight_sum

        # Apply corrections
        lat_guess += avg_dlat
        lon_guess += avg_dlon

    return lat_guess, lon_guess
