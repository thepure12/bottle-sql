from bottle import Bottle
import src.bottle_sql as sql
from sqlite3 import Cursor

app = Bottle()
sql_plugin = sql.sqlitePlugin(":memory:")
app.install(sql_plugin)


def index(db: Cursor):
    db.execute("SELECT 1")
    return {"tables": db.fetchall()}


app.route(path="/", method="GET", callback=index)
app.run(reloader=True)
