import sqlite3
from sqlite3 import Error
from createDB import create_connection
import os
import gpxpy
import models

def create_user(conn, user):
    sql = ''' INSERT INTO users(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

def create_gpxFile(conn, gpxFile):
    sql = ''' INSERT INTO gpxFiles(name,file,miles_ridden,min_lat,min_lon,max_lat,max_lon,user_id)
              VALUES(?,?,?,?,?,?,?,?) '''
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
        (milesRidden, min_lat, min_lon, max_lat, max_lon) = findGpxData(gpxFile)
        gpx = (name, gpxFile, milesRidden, min_lat, min_lon, max_lat, max_lon, user)
        gpx_id = create_gpxFile(conn, gpx)
    return gpx_id

def findGpxData(gpxFile):

    gpx = gpxpy.parse(gpxFile)
    #gpxpy starter code https://github.com/tkrajina/gpxpy
    dx = (0,None)
    max_lat = None
    max_lon = None
    min_lat = None
    min_lon = None
    i = 0
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                    if dx[1] == None:
                        dx = (0,(point.latitude, point.longitude))
                    else:	
                        distance = models.findDistance(dx[1][0], dx[1][1], point.latitude, point.longitude)
                        dx = (dx[0] + distance, (point.latitude, point.longitude))
                    if min_lat == None or point.latitude < min_lat:
                        min_lat = point.latitude
                    if min_lon == None or point.longitude < min_lon:
                        min_lon = point.longitude
                    if max_lat == None or point.latitude > max_lat:
                        max_lat = point.latitude
                    if max_lon == None or point.longitude > max_lon:
                        max_lon = point.longitude        

    return (dx[0], min_lat, min_lon, max_lat, max_lon)


