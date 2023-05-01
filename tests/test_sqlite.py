import unittest
import bottle
import src.bottle_sql as bottle_sql
import sqlite3
import tempfile
import os


class TestSQLite(unittest.TestCase):
    def setUp(self):
        self.app = bottle.Bottle(catchall=False)
        _, dbfile = tempfile.mkstemp(suffix=".sqlite")
        self.dbfile = dbfile
        self.plugin = self.app.install(bottle_sql.sqlitePlugin(dbfile))

        self.conn = sqlite3.connect(dbfile)
        self.conn.execute(
            "CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL)"
        )
        self.conn.commit()

    def tearDown(self):
        os.unlink(self.dbfile)

    def test_keyword(self):
        self.app.get(
            "/",
            callback=lambda db: self.assertEqual(
                type(db), type(sqlite3.connect(":memory:").cursor())
            ),
        )
        self._request("/")

    def test_noKeyword(self):
        self.app.get("/", callback=lambda: "")
        self._request("/")

    def test_otherKwargs(self):
        self.app.get("/", callback=lambda **kwargs: self.assertFalse("db" in kwargs))

    def test_dictrows(self):
        def test(db):
            task = "Do it!"
            db.execute("INSERT INTO todo (id, task) VALUES (1, ?)", (task,))
            db.execute("SELECT * FROM todo")
            count = len(db.fetchall())
            self.assertEqual(count, 1)

        self.app.get("/", callback=test)
        self._request("/")

    def _request(self, path, method="GET"):
        return self.app(
            {"PATH_INFO": path, "REQUEST_METHOD": method}, lambda x, y: None
        )


if __name__ == "__main__":
    unittest.main()
