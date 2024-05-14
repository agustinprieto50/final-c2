from argparse import ArgumentParser
from socket import (socket, AF_INET, SOCK_STREAM)
from json import (loads, dumps, JSONDecodeError)
from jwt import decode
import os

SECRET_KEY = os.getenv('SECRET_KEY')


class Client():
    def __init__(self, email=None, password=None, host='localhost', port=5500):
        self.email = email
        self.password = password
        self.host = host
        self.port = port
        self.token = None 
        self.connected = False

    def connect(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        try:
            self.s.connect((self.host, self.port))
            self.connected = True

        except ConnectionError as e:
            print(f"Connection failed: {e}")
            self.connected = False

    def send_request(self, request_data):
        try:
            if self.connected:
                request_json = dumps(request_data) + '\n'
                self.s.sendall(request_json.encode('utf-8'))
                full_response = b''
                while True:
                    part = self.s.recv(4096)
                    if not part:
                        print("No more data; the server may have closed the connection.")
                        break                        
                    full_response += part
                    if b'\n' in part:
                        break

                full_response = full_response.split(b'\n')[0]
                return loads(full_response.decode('utf-8'))
            else:
                return None
            
        except BrokenPipeError as e:
            self.connect()  # Attempt to reconnect
            self.s.sendall(request_json.encode('utf-8'))  # Try to send again
        
    def log_in(self):
        response = self.send_request({
            'operation': 'log_in',
            'email': self.email,
            'password': self.password
        })
        if response and response['status'] == 'success':
            self.token = response['token']
            print("Login successful!")

        else:
            print("Login failed.")

    def log_out(self):
        response = self.send_request({'operation': 'log_out', 'token': self.token})
        if response and response['status'] == 'success':
            print("Logged out successfully!")
            self.s.close()
        else:       
            print("Error logging out.")

    def display_appointments(self):
        response = self.send_request({'operation': 'get_appointments', 'token': self.token, 'params': {}})
        if response and response['status'] == 'success':
            appointments = response['data']
            for idx, appointment in enumerate(appointments):
                print(f"{idx+1}. Appointment ID: {appointment['appointment_id']} Doctor: {appointment['doctor_full_name']}, Date: {appointment['appointment_date']}")
        else:
            print("No response from server.")

    def display_appointments_per_patient(self):
        response = self.send_request({'operation': 'get_appointments_per_patient', 'params': {'token': self.token}})
        if response and response['status'] == 'success':
            appointments = response['data']
            for idx, appointment in enumerate(appointments):
                print(f"{idx+1}. Appointment ID: {appointment['appointment_id']} Doctor: {appointment['doctor_full_name']}, Date: {appointment['appointment_date']}")
        else:
            print("No appointments found.")

    def confirm_appointment(self, appointment_id):
        response = self.send_request({'operation': 'confirm_appointment', 'params': {'appointment_id': appointment_id, 'token': self.token}})
        if response and response['status'] == 'success':
            print("Appointment confirmed!")
        else:
            print("Error confirming appointment.")

    def cancel_appointment(self, appointment_id):
        response = self.send_request({'operation': 'cancel_appointment', 'params': {'appointment_id': appointment_id, 'token': self.token}})
        if response and response['status'] == 'success':
            print("Appointment cancelled!")
        else:
            print("Error cancelling appointment.")

    def handle_admin_operations(self, operation):
        if operation.lower() == 'configure_new_patient':
            self.configure_new_patient()
        elif operation.lower() == 'configure_new_doctor':
            self.configure_new_doctor()
        elif operation.lower() == 'add_new_appointment':
            self.add_new_appointment()
        elif operation.lower() == 'delete_appointment':
            self.delete_appointment()
        elif operation.lower() == 'update_appointment':
            self.update_appointment()

    def configure_new_patient(self):
        name = input("Enter patient's name: ")
        email = input("Enter patient's email: ")
        response = self.send_request({
            'operation': 'add_patient',
            'name': name,
            'email': email
        })
        if response and response['status'] == 'success':
            print("Patient added successfully!")
        else:
            print("Failed to add patient:", response.get('message', 'Unknown error'))

    def configure_new_doctor(self):
        name = input("Enter doctor's name: ")
        specialty = input("Enter doctor's specialty: ")
        response = self.send_request({
            'operation': 'add_doctor',
            'name': name,
            'specialty': specialty
        })
        if response and response['status'] == 'success':
            print("Doctor added successfully!")
        else:
            print("Failed to add doctor:", response.get('message', 'Unknown error'))

    def add_new_appointment(self):
        doctor_id = input("Enter doctor's ID: ")
        date = input("Enter appointment date (YYYY-MM-DD): ")
        response = self.send_request({
            'operation': 'add_appointment',
            'doctor_id': doctor_id,
            'date': date
        })
        if response and response['status'] == 'success':
            print("Appointment added successfully!")
        else:
            print("Failed to add appointment:", response.get('message', 'Unknown error'))

    def delete_appointment(self):
        appointment_id = input("Enter appointment ID to delete: ")
        response = self.send_request({
            'operation': 'delete_appointment',
            'appointment_id': appointment_id
        })
        if response and response['status'] == 'success':
            print("Appointment deleted successfully!")
        else:
            print("Failed to delete appointment:", response.get('message', 'Unknown error'))

    def update_appointment(self):
        appointment_id = input("Enter appointment ID to update: ")
        new_date = input("Enter new appointment date (YYYY-MM-DD): ")
        response = self.send_request({
            'operation': 'update_appointment',
            'appointment_id': appointment_id,
            'new_date': new_date
        })
        if response and response['status'] == 'success':
            print("Appointment updated successfully!")
        else:
            print("Failed to update appointment:", response.get('message', 'Unknown error'))


    def handle_operation(self):
        while True:
            operation = input("Enter operation: ")

            if operation.lower() == 'log_out':
                self.send_request({'operation': 'log_out', 'token': self.token})
                break

            if operation.lower() == 'get_appointments':
                self.display_appointments()
                continue

            if operation.lower() == 'confirm_appointment':
                appointment_id = input("Enter appointment ID: ")
                self.confirm_appointment(appointment_id)
                continue

            if operation.lower() == 'cancel_appointment':
                appointment_id = input("Enter appointment ID: ")
                self.cancel_appointment(appointment_id)
                continue

            if operation.lower() == 'my_appointments':
                self.display_appointments_per_patient()
                continue
            
           
    def run(self):
        self.connect()
        if not self.connected:
            return
        self.log_in()
        if self.token:
            self.handle_operation()
        self.s.close()
        
            
    def create_parser(self):
        parser = ArgumentParser(description="Client for managing users and appointments")

        parser.add_argument('--email', required=True, help='User email to log in')
        parser.add_argument('--password', required=True, help='User password to log in')

        return parser

def main():
    parser = Client().create_parser()
    args = parser.parse_args()
    client = Client(args.email, args.password)
    client.run()

if __name__ == "__main__":
    main()
