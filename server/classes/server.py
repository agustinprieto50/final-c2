from socket import (socket, AF_INET, SOCK_STREAM)
from json import (loads, dumps)
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from db import DataBase
import authentication as auth
from appointments_manager import AppointmentsManager
from db import DataBase
from redis import Redis


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
            raw = conn.recv(4096)
            data = loads(raw.decode('utf-8'))
            operation = data['operation']
            if operation == 'log_in':
                email = data['email']
                password = data['password']
                response = self.authenticator.log_in(email, password)
                print('response: ', response)
                user_token = response['token']
                print('user_token: ', user_token)
                if user_token:
                    authenticated = True
                    response_data = dumps(response)
                    print('response_data: ', response_data)
                    conn.sendall(response_data.encode('utf-8'))
            if authenticated:
                response_data = self.appointments_manager[operation](**data)
                conn.sendall(response_data.encode('utf-8'))
            else: 
                response_data = dumps({'status': 'error', 'message': 'You are not logged in'})
                conn.sendall(response_data.encode('utf-8'))
                conn.close()

            # else:
            #     raise ValueError("Unsupported operation")

        except Exception as e:
            error_response = dumps({'status': 'error', 'message': str(e)})
            conn.sendall(error_response.encode('utf-8'))
        finally:
            conn.close()

    def connect_to_redis_server(self):
        return Redis(host='localhost', port=6379, db=0, decode_responses=True)

def main():
    server = Server(5500).serve()

if __name__ == '__main__':
    main()