from astropy.io import ascii
from astropy.coordinates import SkyCoord
from astropy import units as u

class StarDatabase:
    def __init__(self, file_path='bsc5.dat'):
        self.stars = self._load_stars(file_path)

    def _load_stars(self, file_path):
        data = ascii.read(file_path, format='fixed_width',
                          col_starts=(0, 4, 75, 83, 102),
                          col_ends=(4, 14, 83, 90, 107),
                          names=['id', 'name', 'ra', 'dec', 'magnitude'])
        
        stars = []
        for row in data:
            coords = SkyCoord(row['ra'], row['dec'], unit=(u.hourangle, u.deg))
            stars.append((row['id'], row['name'], coords.ra.deg, coords.dec.deg, row['magnitude']))
        return stars

    def get_all_stars(self):
        return self.stars

    def get_star(self, star_id):
        for star in self.stars:
            if star[0] == star_id:
                return star
        return None

    def close(self):
        self.conn.close()
