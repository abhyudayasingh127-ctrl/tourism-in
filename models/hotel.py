from models.db import get_db_connection

class Hotel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hotels")
        hotels = cursor.fetchall()
        cursor.close()
        conn.close()
        return hotels

    @staticmethod
    def create(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """INSERT INTO hotels (name, location, price_range, rating, facilities, contact, latitude, longitude)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (data['name'], data['location'], data['price_range'], data['rating'], 
                  data['facilities'], data['contact'], data['latitude'], data['longitude'])
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id
