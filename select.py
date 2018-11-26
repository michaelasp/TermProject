import sqlite3
from sqlite3 import Error
from createDB import create_connection
import os

def select_gpx(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM gpxFiles WHERE user_id=?",(id,))
    rows = cur.fetchall()
    return rows

