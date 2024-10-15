from astropy.coordinates import SkyCoord
from astropy import units as u

def angular_distance(ra1, dec1, ra2, dec2):
    """Calculate angular distance between two points on a sphere"""
    c1 = SkyCoord(ra1*u.deg, dec1*u.deg)
    c2 = SkyCoord(ra2*u.deg, dec2*u.deg)
    return c1.separation(c2).deg

def spherical_triangle_solve(a, b, C):
    """Solve spherical triangle given two sides and included angle"""
    # This function might not be necessary with Astropy
    # You can use Astropy's SkyCoord and EarthLocation for most calculations
    pass
