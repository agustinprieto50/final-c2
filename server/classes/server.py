from socket import (socket, AF_INET, SOCK_STREAM)
from json import (loads, dumps)
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from db import DataBase
from appointments_manager import AppointmentsManager
from db import DataBase
from redis import Redis
from datetime import datetime

import authentication as auth



"""
Codigo del servidor.
Instancia un socket que se encargara de manejar las conexiones.
Por cada conexion, se instanciara un objeto de la clase Manager,
y se agregara al ThreadPoolExecutor como un Thread.
"""


class Server():
    def __init__(self, port):
        self.port = port
        self.host = "localhost"

    def serve(self):
        print('Starting server...')

        db_conn = DataBase()
        redis_conn = self.connect_to_redis_server()
        self.authenticator = auth.Authentication(db_conn, redis_conn)
        self.appointments_manager = AppointmentsManager(db_conn)

        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            with ThreadPoolExecutor(max_workers=10) as executor:
                while True:
                    conn, addr = s.accept()
                    print (f'New connection accepted from: {addr[0]}:{addr[1]}')
                    executor.submit(self.handle_client, conn, db_conn)

    def handle_client(self, conn: socket, db_conn):
        try:
            authenticated = False
            user_token = None

            while True:  # Loop to keep listening for requests
                print(conn.getpeername())
                raw = conn.recv(4096)
                if not raw:
                    break  # If no data is received, break the loop to close the connection

                data = loads(raw.decode('utf-8'))
                operation = data.get('operation')

                print(f'Operation: {operation}, Data: {data}')

                if not operation:
                    raise ValueError("Operation is required")

                if operation == 'log_in':
                    email = data['email']
                    password = data['password']
                    response = self.authenticator.log_in(email, password)
                    if 'token' in response:
                        user_token = response['token']
                        authenticated = True
                    response_data = dumps(response)
                    conn.sendall(response_data.encode('utf-8') + b'\n')
                elif operation == 'log_out':
                    authenticated = False
                    user_token = None
                    response_data = dumps({'status': 'success', 'message': 'Logged out successfully'})
                    conn.sendall(response_data.encode('utf-8') + b'\n')
                    break
                elif authenticated:
                    try:
                        print(f'Operation: {operation}, Data: {data}')
                        method = getattr(self.appointments_manager, operation)
                        print('params: ', data['params'])
                        response_data = method(**data['params'])
                        print(f'Response data: {response_data}') 
                        response_data = dumps(response_data)
                        print(f'Response data: {response_data}')
                        conn.sendall(response_data.encode('utf-8') + b'\n')
                    except AttributeError:
                        response_data = dumps({'status': 'error', 'message': f'Operation {operation} not supported'})
                        conn.sendall(response_data.encode('utf-8' + b'\n'))
                else:
                    response_data = dumps({'status': 'error', 'message': 'You are not logged in'})
                    conn.sendall(response_data.encode('utf-8') + b'\n')

        except Exception as e:
            error_response = dumps({'status': 'error', 'message': str(e)})
            conn.sendall(error_response.encode('utf-8'))
        finally:
            conn.close()

    def connect_to_redis_server(self):
        return Redis(host='localhost', port=6379, db=0, decode_responses=True)
    
    def date_time_converter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

def main():
    server = Server(5500).serve()

if __name__ == '__main__':
    main()