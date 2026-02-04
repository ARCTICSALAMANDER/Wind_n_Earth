import sqlite3


class DBManager():
    def __init__(self):
        self.con = sqlite3.connect("./game_data.sqlite")
        self.cur = self.con.cursor()

    def dbSetup(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS records (
                level INTEGER,
                time INTEGER
            )
        ''')
        self.con.commit()

    def saveRecord(self, level, time):
        self.cur.execute('SELECT time FROM records WHERE level = ?', (level,))
        old_record = self.cur.fetchone()

        if old_record is None:
            self.cur.execute('''
                INSERT INTO records (level, time) VALUES (?, ?)
            ''', (level, time))
        else:
            if time < old_record[0]:
                self.cur.execute('''
                    UPDATE records SET time = ? WHERE level = ?
                ''', (time, level))

        self.con.commit()

    def get_best_time(self, level):
        self.cur.execute('SELECT time FROM records WHERE level = ?', (level,))
        res = self.cur.fetchall()
        res.sort(key=lambda x: x[0])
        return res[0] if res else "--"