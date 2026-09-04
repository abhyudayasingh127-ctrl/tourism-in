from models.db import get_db_connection

class Restaurant:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM restaurants")
        restaurants = cursor.fetchall()
        cursor.close()
        conn.close()
        return restaurants

    @staticmethod
    def create(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """INSERT INTO restaurants (name, location, cuisine, price_range, rating, contact, latitude, longitude)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (data['name'], data['location'], data['cuisine'], data['price_range'], 
                  data['rating'], data['contact'], data['latitude'], data['longitude'])
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id
