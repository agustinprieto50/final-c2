from db import DataBase

class UsersManager():
    def __init__(self, db: DataBase):
        self.db = db

    def get_doctors(self):
        query = '''
                SELECT * FROM Doctors;
                '''
        response = self.db.execute_query(query)
        print(response)
        return response
    


    
