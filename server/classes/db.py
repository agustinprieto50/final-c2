import psycopg2 as pg
from psycopg2 import extras
import os
from dotenv import load_dotenv

# Env Variables
load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')

class DataBase():
    def __init__(self):
        print('Starting connection to DataBase...')

        self.db_conn = pg.connect(database=DATABASE_NAME,
                                  host=DATABASE_HOST,
                                  port=DATABASE_PORT,
                                  user=DATABASE_USER,
                                  password=DATABASE_PASSWORD)
        
        if (self.db_conn):
            print('Connection to Data Base succesful!')

    def get_cursor(self):
        print('Getting cursor...')
        return self.db_conn.cursor(cursor_factory=extras.RealDictCursor)
        
    
    def execute_query(self, query, params=None):
        with self.get_cursor() as cursor:
            try:
                cursor.execute(query, params)
                if cursor.description:
                    data = cursor.fetchall()
                else:
                    data = None
                self.db_conn.commit()
                print('response', data)
                return data
            except pg.Error as e:
                print('An error occured while making a petition to the DB')
                self.db_conn.rollback()
        
    def close_conn(self):
        return self.db_conn.close()


            