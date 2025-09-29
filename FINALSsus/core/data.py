import sqlite3
from typing import Tuple
conn = sqlite3.connect("filedata.db")

def init_table():
    stmt = """
        CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT DEFAULT ''
        )
    """
    conn.execute(stmt)
init_table()
def input_data() -> dict:
    title = input("Enter title: ")
    description = input("Enter description: ")

    data = {"title" : title,
            "description" : description}
    return data
def find(id: int) ->Tuple | None:
    stmt = "SELECT * FROM todo WHERE id=?"
    row = conn.execute(stmt, (id,)).fetchone()
    if row:
        return row
    return None

def create():
    data = input_data()

    if not data["title"]:
        print("Title is required!")
        return
    stmt = "INSERT INTO todo(title, description)VALUES(?,?)"

    conn.execute(stmt, (data["title"], data["description"]))
    conn.commit()

#create()
    
def read():
    stmt = "SELECT * FROM todo"
    rows = conn.execute(stmt).fetchall()

    print(f"{'ID':>5} | {'TITLE':20} | {'DESCRIPTION':20}")
    for row in rows:
        id, title, description = row
        print(f"{id:>5} | {title:20} | {description:20}")

#read()

def update():
    input_id = int(input("Enter id: "))
    old_data = find(input_id)
    new_data = input_data()

    id, title, description = old_data

    if new_data["title"]:
        title = new_data["title"]
    if new_data["description"]:
        description = new_data["description"]

        stmt = "UPDATE todo SET title=?, description=? WHERE id=?"
        conn.execute(stmt, (title, description, id))
        conn.commit()

def delete():
    id = int(input("Enter id: "))

    stmt = "DELETE FROM todo WHERE id=?"
    conn.execute(stmt, (id,))
    conn.commit()
#delete()