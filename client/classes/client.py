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
        if self.connected:
            request_json = dumps(request_data)
            self.s.sendall(request_json.encode('utf-8'))
            response = self.s.recv(4096)
            return loads(response.decode('utf-8'))
        else:
            return None
        
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

    def handle_operation(self):
        while True:
            operation = input("Enter operation: ")

            if operation.lower() == 'log_out':
                self.send_request({'operation': 'log_out', 'token': self.token})
                break
            data = {'operation': operation, 'token': self.token}
            response = self.send_request(data)
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
