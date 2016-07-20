# -*- coding: UTF-8 -*-
import socket
import client_config as config


class Client:
    def __init__(self, server_host, server_port, identify):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accepting = True

        self.server_host = server_host
        self.server_port = server_port
        self.identify = identify

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
        return self.sock.recv(config.MESSAGE_BUFFER)


# Criar objeto da classe cliente
'''
client = Client(config.address['host'], config.address['port'], '1')
client.daemon = True
client.start()

msg = input()
while msg != '/quit':
    client.send_message('1', '2', msg)
    msg = input()

client.close()
'''