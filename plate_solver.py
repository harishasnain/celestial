
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy import units as u

def solve_plate(image_path):
    # Load the image
    hdul = fits.open(image_path)
    header = hdul[0].header
    
    # Create a WCS object
    wcs = WCS(header)
    
    # Get the center coordinates
    center = wcs.pixel_to_world(header['NAXIS1']/2, header['NAXIS2']/2)
    
    # Get the image scale
    scale = wcs.pixel_scale_matrix[0][0] * 3600  # Convert to arcseconds per pixel
    
    # Get the rotation angle
    rotation = wcs.rotation_matrix[0][0]
    
    # Find stars in the image
    # This is a simplified example. You might need to use a more sophisticated method
    # to detect stars, such as SEP (Source Extraction and Photometry) library
    threshold = 3 * hdul[0].data.std()
    stars = np.array(np.where(hdul[0].data > threshold)).T
    
    star_coords = []
    for star in stars:
        coord = wcs.pixel_to_world(star[1], star[0])
        star_coords.append({
            'ra': coord.ra.deg,
            'dec': coord.dec.deg
        })
    
    hdul.close()
    
    return {
        'ra': center.ra.deg,
        'dec': center.dec.deg,
        'rotation': rotation,
        'scale': scale,
        'stars': star_coords
    }
