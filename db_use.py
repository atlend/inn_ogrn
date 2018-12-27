import os
import sqlite3

DB_PATH = os.path.abspath('nalog.db')


class DBUse(object):
    def __enter__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.curs = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.curs.close()
        self.conn.close()

    def column_keys(self):
        self.curs.execute(f"PRAGMA TABLE_INFO(journal);")
        return tuple(i[1] for i in self.curs.fetchall())

    def find_cached_status(self, number: str) -> tuple:
        self.curs.execute(f"SELECT status FROM journal "
                          f"WHERE time_stamp > datetime('now', 'localtime', '-5 minutes')"
                          f"AND number = {number};")
        return self.curs.fetchone()

    def pull_data(self):
        self.curs.execute(f"SELECT * FROM journal ORDER BY time_stamp;")
        return self.curs.fetchall()

    def push_data(self, d):
        self.curs.execute(f"INSERT INTO journal (number, type, status, time_stamp)"
                          f"VALUES ('{d['number']}', '{d['type']}', '{d['status']}', datetime('now', 'localtime'));")
        self.conn.commit()
