from models.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def create(name, email, password, phone=""):
        conn = get_db_connection()
        cursor = conn.cursor()
        pwd_hash = generate_password_hash(password)
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password_hash, phone) VALUES (%s, %s, %s, %s)",
                (name, email, pwd_hash, phone)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, phone, is_admin, created_at FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def verify_password(stored_hash, password):
        return check_password_hash(stored_hash, password)
