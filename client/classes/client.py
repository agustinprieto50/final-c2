from argparse import ArgumentParser
from socket import (socket, AF_INET, SOCK_STREAM)
from json import (loads, dumps, JSONDecodeError)

class Client():
    def __init__(self):
        pass

    def create_parser(self):
        parser = ArgumentParser(description="Client for managing users and appointments")
        subparsers = parser.add_subparsers(dest='manager', required=True, help='Manager type')

        users_parser = subparsers.add_parser('users', help='User operations')
        users_parser.add_argument('operation', choices=['log_in', 'log_out', 'sign_in'], help='User operation')

        appointments_parser = subparsers.add_parser('appointments', help='Appointment operations')
        appointments_parser.add_argument('operation', choices=['get_appointments', 'confirm_appointment', 'cancel_appointment', 'get_appointments_per_doctor'], help='Appointment operation')

        appointments_parser.add_argument('--appointment_id', type=int, help='ID of the appointment to confirm or cancel')

        return parser
    
    def run(self):
        parser = self.create_parser()
        args = parser.parse_args()

        request_data = {
            'operation': args.operation
        }

        if hasattr(args, 'appointment_id') and args.appointment_id is not None:
            request_data['appointment_id'] = args.appointment_id

        request_json = dumps(request_data)

        try:
            with socket(AF_INET, SOCK_STREAM) as s:
                s.connect(('localhost', 5500))
                s.sendall(request_json.encode('utf-8'))

                response = []
                while True:
                    chunk = s.recv(1024)
                    if b"END_OF_MESSAGE" in chunk:
                        response.append(chunk[:chunk.find(b"END_OF_MESSAGE")])
                        break
                    response.append(chunk)

                
                response = b''.join(response).decode('utf-8')
                if response:
                    response_data = loads(response)
                    if response_data['status'] == 'success':
                        print(f"Response: {response_data['response']}")
                    else:
                        print(f"Error: {response_data['message']}")
                    
        except ConnectionError as e:
            print(f"Connection failed: {e}")
        except JSONDecodeError as e:
            print(f"Error decoding response: {e}")


if __name__ == "__main__":
    client = Client()
    client.run()
