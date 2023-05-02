import unittest
import bottle
import src.bottle_sql as bottle_sql
import pymysql
import pymysql.cursors

HOST = "localhost"
USER = "bottle_sql"
PASS = ""
DB = "bottle_sql"


class TestSQL(unittest.TestCase):
    def setUp(self) -> None:
        self.app = bottle.Bottle(catchall=False)
        self.plugin = self.app.install(bottle_sql.sqlPlugin(USER, PASS, HOST, DB))

        conn = pymysql.connect(user=USER, password=PASS, host=HOST, database=DB)
        with conn.cursor() as db:
            db.execute("DROP TABLE IF EXISTS todo")
            db.execute(
                "CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL)"
            )
        conn.commit()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_keyword(self):
        self.app.get(
            "/",
            callback=lambda db: self.assertEqual(type(db), pymysql.cursors.DictCursor),
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
            db.execute("INSERT INTO todo (id, task) VALUES (1, %s)", (task,))
            db.execute("SELECT * FROM todo")
            count = len(db.fetchall())
            self.assertEqual(count, 1)

        self.app.get("/", callback=test)
        self._request("/")

    def _request(self, path, method="GET"):
        return self.app(
            {"PATH_INFO": path, "REQUEST_METHOD": method}, lambda x, y: None
        )
