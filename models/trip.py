from models.db import get_db_connection

class Trip:
    @staticmethod
    def create_trip(user_id, name, start_date, days, budget, budget_amount, interests, place_assignments):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # budget_amount column aur parameter (%s) add kiya gaya h
            cursor.execute(
                """
                INSERT INTO trips (user_id, trip_name, start_date, number_of_days, budget, budget_amount, interests) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (user_id, name, start_date, days, budget, budget_amount, interests)
            )
            trip_id = cursor.lastrowid

            for assignment in place_assignments:
                cursor.execute(
                    "INSERT INTO trip_places (trip_id, place_id, day_number, visit_order) VALUES (%s, %s, %s, %s)",
                    (trip_id, assignment['place_id'], assignment['day_number'], assignment['visit_order'])
                )
            conn.commit()
            return trip_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM trips WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        trips = cursor.fetchall()
        for trip in trips:
            cursor.execute("""
                SELECT tp.*, p.name, p.category, p.image_url, p.latitude, p.longitude
                FROM trip_places tp
                JOIN tourist_places p ON tp.place_id = p.id
                WHERE tp.trip_id = %s
                ORDER BY tp.day_number, tp.visit_order
            """, (trip['id'],))
            trip['places'] = cursor.fetchall()
        cursor.close()
        conn.close()
        return trips
