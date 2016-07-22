# -*- coding: UTF-8 -*-
import socket

import server_config as config

from threading import Thread

class Server(object):

    def __init__(self, host=config.address['host'], port=config.address['port']):
        self.__host = host
        self.__port = port
        self.__clients = []
        self.__threads = []
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((host, port))
        self.__socket.listen(10)
        print('Server is open {}:{}'.format(host, port))

    @property
    def get_socket(self):
        return self.__socket

    @property
    def get_clients(self):
        return self.__clients

    @property
    def get_threads(self):
        return self.__threads

    def add_client(self, client):
        if client not in self.__clients:
            self.__clients.append(client)

    def add_threads(self, thread):
        if thread not in self.__threads:
            self.__threads.append(thread)

    def clientHandler(self, conn, addr):
        print(addr, 'is connected')

        try:
            while True:
                data = conn.recv(config.RECEIVE_BUFFER)
                if not data:
                    break
                for client in self.__clients:
                    if addr != client['addr']:
                        print(addr, ' -> ' ,data)
                        client['conn'].sendto(data, client['addr'])
        except socket.error as e:
            print('Not possible sent the msg: {}'.format(e))

    def start_threads(self):
        while True:
            conn, addr = self.get_socket.accept()
            self.add_client({'conn': conn, 'addr': addr})
            t = Thread(target=self.clientHandler, args=(conn, addr))
            self.add_threads(t)
            t.start()

    def join_threads(self):
        for t in self.get_threads:
            t.join()

if __name__ == '__main__':
    try:
        server = Server()

        server.start_threads()
        server.join_threads()

    except KeyboardInterrupt:
        server.get_socket.close()
        print('Server is closed')
