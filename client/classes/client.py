from argparse import ArgumentParser
from socket import (socket, AF_INET, SOCK_STREAM)
from json import (loads, dumps, JSONDecodeError)

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
        print('request_data', request_data)
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
                print('full_response', full_response)
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
        print(response)
        if response and response['status'] == 'success':
            self.token = response['token']
            print("Login successful!")

        else:
            print("Login failed.")

    def display_appointments(self):
        response = self.send_request({'operation': 'get_appointments', 'token': self.token, 'params': {}})
        if response and response['status'] == 'success':
            appointments = response['data']
            for idx, appointment in enumerate(appointments):
                print(f"{idx+1}. Appointment ID: {appointment['appointment_id']} Doctor: {appointment['doctor_full_name']}, Date: {appointment['appointment_date']}")
        else:
            print("No response from server.")

    def confirm_appointment(self, appointment_id):
        response = self.send_request({'operation': 'confirm_appointment', 'params': {'appointment_id': appointment_id, 'token': self.token}})
        if response and response['status'] == 'success':
            return response
           

    def handle_operation(self):
        while True:
            print('\n')
            operation = input("Enter operation: ")
            response = None

            if operation.lower() == 'log_out':
                self.send_request({'operation': 'log_out', 'token': self.token})
                break

            if operation.lower() == 'get_appointments':
                print(operation)
                self.display_appointments()
                continue

            if operation.lower() == 'confirm_appointment':
                appointment_id = input("Enter appointment ID: ")
                response = self.confirm_appointment(appointment_id)
                continue

            
            if response:
                print(response['message'])
            else:
                print("No response from server.")
                break

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
