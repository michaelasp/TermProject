import sqlite3
from sqlite3 import Error
from createDB import create_connection
import os

def select_gpx(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM gpxFiles WHERE user_id=?",(id,))
    rows = cur.fetchall()
    return rows

def select_name(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT name FROM users WHERE id=?",(id,))
    user = cur.fetchall()
    print(user[0][1])
    return user[0]

def select_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return users




