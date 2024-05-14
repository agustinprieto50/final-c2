import datetime
import bcrypt
import jwt
import os
from psycopg2.extras import RealDictCursor
from db import DataBase
from redis import Redis

class Authentication():
    def __init__(self, db: DataBase, redis_conn: Redis):
        self.db = db
        self.redis_conn = redis_conn
        self.secret_key = os.getenv('SECRET_KEY')

    def sign_up(self, patient_id, first_name, last_name, email, password):
        full_name = f"{first_name} {last_name}"
        hashed_password = self.hash_password(password)
        query = "INSERT INTO users (patient_id, first_name, last_name, full_name, email, password_hash) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(query, (patient_id, first_name, last_name, full_name, email, hashed_password))
                self.db.db_conn.commit()
                print("Signup successful!")
        except Exception as e:
            print("Error signing up:", e)


    def log_in(self, email, password):
        query = "SELECT user_id, password FROM users WHERE email = %s"
        try:
            result = self.db.execute_query(query, (email,)) 
            if result:
                user = [dict(row) for row in result][0]
                user_id, hashed_password = user['user_id'], user['password']
                if self.check_pw(password, hashed_password):
                    token = self.generate_token(user_id, email)
                    self.redis_conn.setex(token, 86400, email)  
                    print("Login successful! User ID:", user_id)
                    # print("Token:", token)
                    return {'status': 'success', 'token': token}
                else:
                    print("Invalid password.")
                    return {'status': 'error', 'message': 'Invalid password'}
            else:
                print("User not found.")
                return {'status': 'error', 'message': 'User not found'}
        except Exception as e:
            print("Error logging in:", e)
            return {'status': 'error', 'message': str(e)}


    def log_out(self, token):
        self.redis_conn.delete(token)
        print("Logged out successfully!")
        return {'status': 'success', 'message': 'Logged out successfully'}

    def generate_token(self, patient_id, email):
        payload = {
            'patient_id': patient_id,
            'email': email,
            'exp':datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1) 
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def validate_token(self, token):
        token_exists = self.redis_conn.exists(token)
        return token_exists

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def check_pw(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
