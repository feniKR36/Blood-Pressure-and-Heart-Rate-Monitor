
import sqlite3
from features.items.repository import ReadingRepo, PatientRepo

_conn = None

def get_conn():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect("filedata3.db")
        _conn.row_factory = sqlite3.Row
    return _conn

ReadingRepo(get_conn())
PatientRepo(get_conn())
