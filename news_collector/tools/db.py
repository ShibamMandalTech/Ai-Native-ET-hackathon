# tools/db.py

import mysql.connector
from mysql.connector import pooling

pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host="localhost",
    user="root",
    password="Shibamishere4231",
    database="newsroom"
)

def get_connection():
    return pool.get_connection()