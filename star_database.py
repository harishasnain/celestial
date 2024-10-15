import sqlite3

class StarDatabase:
    def __init__(self, file_path='bsc5.dat'):
        self.stars = self._load_stars(file_path)

    def _load_stars(self, file_path):
        stars = []
        with open(file_path, 'r') as file:
            for line in file:
                # Parse each line of the bsc5.dat file
                # The format is fixed-width, so we'll use string slicing
                star_id = int(line[0:4])
                ra_hours = float(line[75:77])
                ra_minutes = float(line[77:79])
                ra_seconds = float(line[79:83])
                dec_degrees = float(line[84:86])
                dec_minutes = float(line[86:88])
                dec_seconds = float(line[88:90])
                magnitude = float(line[102:107])

                # Convert RA and Dec to decimal degrees
                ra = (ra_hours + ra_minutes/60 + ra_seconds/3600) * 15  # 15 degrees per hour
                dec = dec_degrees + dec_minutes/60 + dec_seconds/3600
                if line[83] == '-':
                    dec = -dec

                stars.append((star_id, None, ra, dec, magnitude))
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
