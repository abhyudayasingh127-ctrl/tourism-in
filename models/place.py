from models.db import get_db_connection

class Place:
    @staticmethod
    def get_all(category=None):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        if category:
            cursor.execute("SELECT * FROM tourist_places WHERE category = %s", (category,))
        else:
            cursor.execute("SELECT * FROM tourist_places")
        places = cursor.fetchall()
        cursor.close()
        conn.close()
        return places

    @staticmethod
    def get_by_id(place_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tourist_places WHERE id = %s", (place_id,))
        place = cursor.fetchone()
        cursor.close()
        conn.close()
        return place

    @staticmethod
    def create(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """INSERT INTO tourist_places 
                   (name, description, category, location, latitude, longitude, visiting_hours, estimated_duration, image_url) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (data['name'], data['description'], data['category'], data['location'], 
                  data['latitude'], data['longitude'], data['visiting_hours'], 
                  data['estimated_duration'], data['image_url'])
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id

    @staticmethod
    def delete(place_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tourist_places WHERE id = %s", (place_id,))
        conn.commit()
        cursor.close()
        conn.close()
