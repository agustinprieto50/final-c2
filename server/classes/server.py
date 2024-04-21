from socket import (socket, AF_INET, SOCK_STREAM)
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from db import DataBase
from manager import Manager

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

        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            db = DataBase()

            with ThreadPoolExecutor(max_workers=10) as executor:
                while True:
                    conn, addr = s.accept()
                    print (f'New connection accepted from: {addr[0]}:{addr[1]}')
                    manager = Manager(db_cursor=db.get_cursor())
                    executor.submit()

server = Server(5500).serve()