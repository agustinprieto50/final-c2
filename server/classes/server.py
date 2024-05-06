from socket import (socket, AF_INET, SOCK_STREAM)
from json import (loads, dumps)
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from db import DataBase
from users_manager import UsersManager
from appointments_manager import AppointmentsManager
from db import DataBase


"""
Codigo del servidor.
Instancia un socket que se encargara de manejar las conexiones.
Por cada conexion, se instanciara un objeto de la clase Manager,
y se agregara al ThreadPoolExecutor como un Thread.
"""

operation_mapping = {
    'log_in': (UsersManager, 'log_in'),
    'log_out': (UsersManager, 'log_out'),
    'get_appointments': (AppointmentsManager, 'get_appointments'),
    'confirm_appointment': (AppointmentsManager, 'confirm_appointment'),
    'cancel_appointment': (AppointmentsManager, 'cancel_appointment'),
    'get_appointments_per_doctor': (AppointmentsManager, 'get_appointments_per_doctor')
}

class Server():
    def __init__(self, port):
        self.port = port
        self.host = "localhost"

    def serve(self):
        print('Starting server...')

        db_conn = DataBase()

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
            raw = conn.recv(4096)
            print(raw)
            data = loads(raw.decode('utf-8'))
            print('data: ', data)
            operation = data['operation']

            if operation in operation_mapping:
                manager_class, method_name = operation_mapping[operation]
                manager = manager_class(db_conn)
                method = getattr(manager, method_name)
                response = method(**data.get('params', {}))
                response_data = dumps({'status': 'success', 'response': response})
                conn.sendall(response_data.encode('utf-8'))
                conn.sendall(b"END_OF_MESSAGE")  

            else:
                raise ValueError("Unsupported operation")

        except Exception as e:
            error_response = dumps({'status': 'error', 'message': str(e)})
            conn.sendall(error_response.encode('utf-8'))
        finally:
            conn.close()


if __name__ == '__main__':
    server = Server(5500).serve()