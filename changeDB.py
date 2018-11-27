import sqlite3
from sqlite3 import Error
from createDB import create_connection
import os
from math import sin, cos, sqrt, atan2, radians
import gpxpy

def create_user(conn, user):
    sql = ''' INSERT INTO users(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

def create_gpxFile(conn, gpxFile):
    sql = ''' INSERT INTO gpxFiles(name,file,miles_ridden,user_id)
              VALUES(?,?,?,?) '''
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
        milesRidden = findMilesRidden(gpxFile)
        gpx = (name, gpxFile, milesRidden, user)
        gpx_id = create_gpxFile(conn, gpx)
    return gpx_id

def findMilesRidden(gpxFile):
    R = 6373.0
    milesRidden = 0
    gpx = gpxpy.parse(gpxFile)
    #gpxpy starter code https://github.com/tkrajina/gpxpy
    dx = (0,None)
    i = 0
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                    if dx[1] == None:
                        dx = (0,(point.latitude, point.longitude))
                    #Find distance from lattitude longitude https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
                    else:	
                        lat1 = radians(dx[1][0])
                        lon1 = radians(dx[1][1])
                        lat2 = radians(point.latitude)
                        lon2 = radians(point.longitude)
                        dlon = lon2 - lon1
                        dlat = lat2 - lat1
                        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                        c = 2 * atan2(sqrt(a), sqrt(1 - a))
                        distance = R * c
                        dx = (dx[0] + distance, (point.latitude, point.longitude))
    return dx[0]