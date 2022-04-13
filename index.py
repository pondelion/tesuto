from typing import Optional
import sqlite3

from fastapi import FastAPI

app = FastAPI()

con = sqlite3.connect('./test.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS item(id integer primary key autoincrement,name text)")
con.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_item(id: Optional[int] = None, name: Optional[str] = None):
    con = sqlite3.connect('./test.db')
    cur = con.cursor()
    if id is None and name is None:
        cur.execute("select * from item")
    elif id is not None:
        cur.execute("select * from item where id=:id", {"id": id})
    else:
        cur.execute("select * from item where name=:name", {"name": name})
    records = cur.fetchall()
    con.close()
    return {'items': records}


@app.post("/items")
def register_item(name: str):
    con = sqlite3.connect('./test.db')
    cur = con.cursor()
    cur.execute("insert into item (name) values (?)", (name,))
    con.commit()
    con.close()
    return {'message': f'registered item {name}'}
