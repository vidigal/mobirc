# -*- coding: UTF-8 -*-
import socket
import client_config as config
from threading import Thread


class Client(Thread):
    def __init__(self, server_host, server_port, identify):
        Thread.__init__(self)
        self.server_host = server_host
        self.server_port = server_port
        self.identify = identify
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accepting = True

    def run(self):
        self.connect()
        self.receive_message()

    def connect(self):
        self.sock.connect((self.server_host, self.server_port))
        self.sock.send(self.identify.encode())  # Envia o identificador do cliente para o servidor
        print('Conectado ao servidor %s:%s' % (self.server_host, self.server_port))

    def close(self):
        print('Fechar')
        self.sock.close()
        self.accepting = False

    def send_message(self, sender, to, message):
        msg = {'sender': sender, 'to': to, 'msg': message}
        self.sock.send(str(msg).encode())

    def receive_message(self):
        while self.accepting:
            print(self.sock.recv(1024))


# Criar objeto da classe cliente
client = Client(config.address['host'], config.address['port'], '1')
client.daemon = True
client.start()

msg = input()
while msg != '/quit':
    client.send_message('1', '2', msg)
    msg = input()

client.close()