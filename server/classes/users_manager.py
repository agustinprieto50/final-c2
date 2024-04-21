from db import DataBase

class UsersManager():
    def __init__(self, db: DataBase):
        self.db = db

    def get_patients(self):
        query = '''
                SELECT * FROM Doctors;
                '''
        response = self.db.execute_query(query)
        print(response)
        return response
    

db = DataBase()

manager = UsersManager(db)
manager.get_patients()
    
