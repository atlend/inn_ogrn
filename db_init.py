import os
import sqlite3

DB_PATH = os.path.abspath('nalog.db')


class DBInit(object):
    def __enter__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.curs = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.curs.close()
        self.conn.close()

    def create_table(self):
        self.curs.execute(f"CREATE TABLE IF NOT EXISTS journal("
                          f"number TEXT, "
                          f"type TEXT, "
                          f"status TEXT, "
                          f"time_stamp TEXT);")
        self.conn.commit()

    def drop_table(self):
        self.curs.execute(f"DROP TABLE IF EXISTS journal;")
        self.conn.commit()


if __name__ == '__main__':
    with DBInit() as db:
        db.drop_table()
        db.create_table()
