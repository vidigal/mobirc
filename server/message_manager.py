# -*- coding: UTF-8 -*-
import socket
from threading import Thread
import select
import time
import ast


class MessageManager(Thread):

    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock
        self.messages = []

    def run(self):
        while True:
            self.range_clients()
            self.dispatch_messages()
            time.sleep(5)  # Tirar isso depois

    def get_client_sockets(self):  # Tenho que usar esse método para passar uma lista de sockets para o select
        client_sockets = []
        for client_socket in self.sock.clients:
            client_sockets.append(client_socket[0][0])
        return client_sockets

    def range_clients(self):
        if self.sock.clients:
            receive_ready, send_ready, except_ready = select.select(self.get_client_sockets(), [], [], 0.01)
            # Receber mensagens
            for client in receive_ready:
                print('incluindo')
                self.messages.append(ast.literal_eval(client.recv(512).decode()))

    def dispatch_messages(self):
        while self.messages:
            msg = self.messages.pop()
            print(msg)
            to = self.get_client_sock_by_id(msg['to'])
            print('to', to)
            if to is not None:
                print('Enviando mensagem "%s" de %s para %s' % (msg['msg'], msg['sender'], msg['to']))
                to.send(msg['msg'].encode())

    def get_client_sock_by_id(self, id):
        for client_socket in self.sock.clients:
            print(client_socket)
            if client_socket[1][0] == id:
                return client_socket[0][0]
