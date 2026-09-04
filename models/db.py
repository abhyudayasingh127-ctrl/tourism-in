import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DB', 'varanasi_tourism'),
        port=int(os.getenv('MYSQL_PORT', 20357))
    )
