import math

def angular_distance(ra1, dec1, ra2, dec2):
    """Calculate angular distance between two points on a sphere"""
    phi1 = math.radians(90 - dec1)
    phi2 = math.radians(90 - dec2)
    theta1 = math.radians(ra1)
    theta2 = math.radians(ra2)

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2))
    return math.degrees(math.acos(cos))

def spherical_triangle_solve(a, b, C):
    """Solve spherical triangle given two sides and included angle"""
    a_rad = math.radians(a)
    b_rad = math.radians(b)
    C_rad = math.radians(C)

    c_rad = math.acos(math.cos(a_rad) * math.cos(b_rad) + 
                      math.sin(a_rad) * math.sin(b_rad) * math.cos(C_rad))
    
    return math.degrees(c_rad)