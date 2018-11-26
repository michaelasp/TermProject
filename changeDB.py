import sqlite3
from sqlite3 import Error
from createDB import create_connection
import os

def create_user(conn, user):
    sql = ''' INSERT INTO users(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

def create_gpxFile(conn, gpxFile):
    sql = ''' INSERT INTO gpxFiles(name,file,user_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, gpxFile)
    return cur.lastrowid

def test():
    database = "db/user.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        user = ('Bepis Man',)
        user_id = create_user(conn, user)
        # tasks
        gpx = open('gpx/nstar.gpx', 'r')
        add_gpxFile(conn, 'nstar', gpx, user_id )

def add_user(conn, name):
    with conn:
        user = (name,)
        user_id = create_user(conn, user)
    return user_id

def add_gpxFile(conn, name, gpxFile, user):
    with conn:
        gpxFile = gpxFile.read()
        gpx = (name, gpxFile, user)
        gpx_id = create_gpxFile(conn, gpx)
    return gpx_id
test()