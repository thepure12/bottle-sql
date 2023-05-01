class BottleSQL:
    name = "bottle_sql"
    api = 2

    SQL = 1
    SQLITE = 2

    def __init__(self, mode=SQLITE) -> None:
        if mode == self.SQLITE:
            import pymysql
        else:
            import sqlite3

    def apply(self, fn, context):
        pass
