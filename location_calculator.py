import math
from datetime import datetime
from spherical_trig import angular_distance, spherical_triangle_solve
from star_database import StarDatabase
from utils import ra_to_decimal

def calculate_location(solved_data, observation_time):
    db = StarDatabase()
    stars = db.get_all_stars()

    # Find matching stars in the database
    matched_stars = []
    for solved_star in solved_data['stars']:
        for db_star in stars:
            if angular_distance(solved_star['ra'], solved_star['dec'], db_star[2], db_star[3]) < 0.1:
                matched_stars.append((solved_star, db_star))
                break

    if len(matched_stars) < 3:
        raise ValueError("Not enough stars matched for location calculation")

    # Calculate Greenwich Sidereal Time (GST)
    j2000 = datetime(2000, 1, 1, 12, 0, 0)
    days_since_j2000 = (observation_time - j2000).total_seconds() / 86400
    gst = (18.697374558 + 24.06570982441908 * days_since_j2000) % 24

    # Initial guess for latitude and longitude (can be arbitrary)
    lat_guess, lon_guess = 0, 0

    # Iterate to improve the position estimate
    for _ in range(5):  # Number of iterations can be adjusted
        lat_guess, lon_guess = iterate_position(matched_stars, gst, lat_guess, lon_guess)

    return lat_guess, lon_guess

def iterate_position(matched_stars, gst, lat_guess, lon_guess):
    sum_dlat, sum_dlon = 0, 0
    weight_sum = 0

    for solved_star, db_star in matched_stars:
        # Calculate Local Hour Angle (LHA)
        lha = (gst * 15 + lon_guess - ra_to_decimal(*db_star[2])) % 360

        # Calculate altitude and azimuth
        sin_alt = (math.sin(math.radians(lat_guess)) * math.sin(math.radians(db_star[3])) +
                   math.cos(math.radians(lat_guess)) * math.cos(math.radians(db_star[3])) *
                   math.cos(math.radians(lha)))
        alt_calc = math.degrees(math.asin(sin_alt))

        # Observed altitude from the solved plate
        alt_obs = 90 - angular_distance(solved_data['ra'], solved_data['dec'], db_star[2], db_star[3])

        # Calculate intercept (difference between observed and calculated altitude)
        intercept = alt_obs - alt_calc

        # Calculate azimuth
        cos_az = (math.sin(math.radians(db_star[3])) - 
                  math.sin(math.radians(lat_guess)) * math.sin(math.radians(alt_calc))) / 
                 (math.cos(math.radians(lat_guess)) * math.cos(math.radians(alt_calc)))
        azimuth = math.degrees(math.acos(cos_az))
        if math.sin(math.radians(lha)) > 0:
            azimuth = 360 - azimuth

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
    new_lat = lat_guess + avg_dlat
    new_lon = lon_guess + avg_dlon

    return new_lat, new_lon