import math

def dms_to_decimal(degrees, minutes, seconds):
    """Convert degrees, minutes, seconds to decimal degrees"""
    return degrees + minutes / 60 + seconds / 3600

def decimal_to_dms(decimal_degrees):
    """Convert decimal degrees to degrees, minutes, seconds"""
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = ((decimal_degrees - degrees) * 60 - minutes) * 60
    return degrees, minutes, seconds

def ra_to_decimal(hours, minutes, seconds):
    """Convert right ascension to decimal degrees"""
    return (hours + minutes / 60 + seconds / 3600) * 15