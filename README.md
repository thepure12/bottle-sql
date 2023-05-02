# BottleSQL
SQL plugin for Bottle. Supports MySQL/MariaDB and SQLite.

## Installation
### PyPi
``` bash
pip install pip install bottle-sql==0.0.1
```
### Source
```bash
wget https://raw.githubusercontent.com/thepure12/bottle-sql/main/src/bottle_sql/bottle_sql.py
```

## Usage
### SQL
```python
from bottle import Bottle
from bottle_sql import sqlPlugin

app = Bottle()
user, pw, host, db = ("root", "", "localhost", "mydb")
sql_plugin = sqlPlugin(user=user, password=pw, host=host, database=db)
app.install(sql_plugin)
```

### SQLite
```python
from bottle import Bottle
from bottle_sql import sqlitePlugin

app = Bottle()
dbfile= ":memory:"
sql_plugin = sqlitePlugin(dbfile)
app.install(sql_plugin)
```
