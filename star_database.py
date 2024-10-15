import sqlite3

class StarDatabase:
    def __init__(self, db_path='stars.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stars
            (id INTEGER PRIMARY KEY, name TEXT, ra REAL, dec REAL, magnitude REAL)
        ''')
        self.conn.commit()

    def add_star(self, name, ra, dec, magnitude):
        self.cursor.execute('''
            INSERT INTO stars (name, ra, dec, magnitude)
            VALUES (?, ?, ?, ?)
        ''', (name, ra, dec, magnitude))
        self.conn.commit()

    def get_star(self, name):
        self.cursor.execute('SELECT * FROM stars WHERE name = ?', (name,))
        return self.cursor.fetchone()

    def get_all_stars(self):
        self.cursor.execute('SELECT * FROM stars')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()