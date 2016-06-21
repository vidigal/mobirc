# -*- coding: UTF-8 -*-
import socket

import server_config as config
from message_manager import MessageManager


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.accepting = True
        self.message_manager = MessageManager(self)

    def connect(self):
        print('Starting up on %s port %s' % (self.host, self.port))
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)  # Put socket into server mode
        while self.accepting:
            client_connected = self.sock.accept()
            print('Connection from', client_connected)
            client_identify = client_connected[0].recv(config.IDENTIFY_BUFFER).decode()  # Isso depois pode virar uma função de autenticação
            self.clients.append((client_connected, client_identify))

    def start_message_manager(self):
        self.message_manager.start()

    def close(self):
        print('Closing server socket')
        self.accepting = False
        self.sock.close()



# Criar objeto da classe server e startar servidor
server = Server(config.address['host'], config.address['port'])
server.start_message_manager()
server.connect()

server.close()

#Está faltando fechar o connection
