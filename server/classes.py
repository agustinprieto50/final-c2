# from socket import (socket, AF_INET, SOCK_STREAM)
# from concurrent.futures import ThreadPoolExecutor
# from threading import Lock


# class AppointmentsManagerServer():
#     def __init__(self, port):
#         self.port = port
#         self.host = "0.0.0.0"

#     def serve(self):
#         print('Starting server...')

#         with socket(AF_INET, SOCK_STREAM) as server:
#             server.bind(self.host, self.port)
#             server.listen()

#             with ThreadPoolExecutor(max_workers=10) as executor:
#                 while True:
#                     conn, addr = server.accept()
#                     print (f'New connection accepted from: {addr[0]}:{addr[1]}')
#                     manager = Manager()
#                     executor.submit()


# class Manager():
#     def __init__(self, db_path):
#         self.lock = Lock()
#         self.db_path = db_path
#         self.create_db()

#     def create_db(self):
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         c.execute('''CREATE TABLE IF NOT EXISTS doctors (doctor_id INTEGER PRIMARY KEY, full_name TEXT);
#                   CREATE TABLE IF NOT EXISTS patients (patient_id INTEGER PRIMARY KEY, full_name TEXT);
#                   CREATE TABLE IF NOT EXISTS appointments
#                   (doctor_id INTEGER, specialization TEXT, appointment_date DATETIME, patient_id INTEGER, FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id), FOREIGN KEY(patient_id) REFERENCES patients(patient_id), PRIMARY KEY(doctor_id, appointment_date));''')
#         conn.commit()
#         conn.close()

#     def db_query(self, query, params=(), commit=False):
#         with self.lock, sqlite3.connect(self.db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             if commit:
#                 conn.commit()
#             return cursor.fetchall()
        
#     def get_appointments(self, doctor_id, from_date, to_date, speciality):
#         # Get existing appointments
#         query = """
#                 SELECT * FROM appointments
#                 JOIN doctors ON appointments.doctor_id = doctors.doctor_id
#                 WHERE doctors.name = ? AND 
#                 appointments.appointment_date >= ? AND
#                 appointments.appointment_date < ?' AND 
#                 appointments.speciality = ?' AND 
#                 """
#         appointments = self.db_query(query, (doctor_id, from_date, to_date, speciality))
#         return appointments

#     def handle_client():
#         return
    
#     def run(self, ):
#         return


# class 

# # #import threading

# # class Manager:
# #     def __init__(self):
# #         # Dictionary to hold appointments for different doctors
# #         self.appointments = {}
# #         # Dictionary to hold locks for each doctor
# #         self.locks = {}

# #     def get_lock(self, doctor_id):
# #         """Ensure that each doctor has their own lock."""
# #         if doctor_id not in self.locks:
# #             self.locks[doctor_id] = threading.Lock()
# #         return self.locks[doctor_id]

# #     def add_appointment(self, doctor_id, date, patient_name):
# #         doctor_lock = self.get_lock(doctor_id)
# #         with doctor_lock:
# #             if doctor_id not in self.appointments:
# #                 self.appointments[doctor_id] = {}
# #             if date in self.appointments[doctor_id]:
# #                 return f"Doctor {doctor_id}: Slot on {date} is already booked."
# #             else:
# #                 self.appointments[doctor_id][date] = patient_name
# #                 return f"Doctor {doctor_id}: Appointment set for {patient_name} on {date}."

# #     def cancel_appointment(self, doctor_id, date):
# #         doctor_lock = self.get_lock(doctor_id)
# #         with doctor_lock:
# #             if doctor_id in self.appointments and date in self.appointments[doctor_id]:
# #                 patient = self.appointments[doctor_id].pop(date)
# #                 return f"Doctor {doctor_id}: Appointment for {patient} on {date} canceled."
# #             else:
# #                 return f"Doctor {doctor_id}: No appointment found on {date} to cancel."

# #     def process_request(self, data):
# #         # Example command: "ADD 1 2023-04-15 Alice" where 1 is doctor_id
# #         command, doctor_id, date, *params = data.split()
# #         if command == "ADD":
# #             return self.add_appointment(doctor_id, date, " ".join(params))
# #         elif command == "CANCEL":
# #             return self.cancel_appointment(doctor_id, date)
# #         else:
# #             return "Invalid command"
