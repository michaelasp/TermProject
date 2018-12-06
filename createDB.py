#Initializes Database
import sqlite3
from sqlite3 import Error

#Creating db from tutorial http://www.sqlitetutorial.net/sqlite-python/create-tables/
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def createDB():
    database = "db/user.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

    sql_create_gpx_table = """ CREATE TABLE IF NOT EXISTS gpxFiles (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        file text NOT NULL,
                                        miles_ridden real NOT NULL,
                                        min_lat real NOT NULL,
                                        min_lon real NOT NULL,
                                        max_lat real NOT NULL,
                                        max_lon real NOT NULL,
                                        user_id integer NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES users (id)
                                    ); """

    conn = create_connection(database)
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_users_table)
        # create tasks table
        create_table(conn, sql_create_gpx_table)
    else:
        print("Error! cannot create the database connection.")