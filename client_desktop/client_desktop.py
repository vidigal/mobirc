from threading import Thread
from tkinter import *

import time

import select

from client import Client

class Message_Manager(Thread):

    def __init__(self, client, t_chat):
        Thread.__init__(self)
        self.client = client
        self.t_chat = t_chat

    def run(self):
        while True:
            print('Verificando msgs')
            time.sleep(2)
            self.t_chat.insert('1.0', self.client.receive_message().decode()+'\n')
            print('verificou msg')


class Client_Desktop:
    def __init__(self):
        self.client = None

        self.root = Tk()
        self.root.geometry('+200+200')

        #Top frame
        self.f_top = LabelFrame(self.root, text='Configurações', bg='red', bd="3")
        self.f_top.pack()

        self.l_server = Label(self.f_top, text='Servidor')
        self.l_server.grid(row=0, column=0)
        self.e_server = Entry(self.f_top)
        self.e_server.insert(0, "0.0.0.0")
        self.e_server.grid(row=0, column=1)

        self.l_port = Label(self.f_top, text='Porta')
        self.l_port.grid(row=1, column=0)
        self.e_port = Entry(self.f_top)
        self.e_port.insert(0, 38267)
        self.e_port.grid(row=1, column=1)

        self.l_identifier = Label(self.f_top, text='Identificador')
        self.l_identifier.grid(row=2, column=0)
        self.e_identifier = Entry(self.f_top)
        self.e_identifier.insert(0, '1')
        self.e_identifier.grid(row=2, column=1)

        self.l_to = Label(self.f_top, text='Para')
        self.l_to.grid(row=3, column=0)
        self.e_to = Entry(self.f_top)
        self.e_to.insert(0, '2')
        self.e_to.grid(row=3, column=1)

        self.b_connect = Button(self.f_top, text='Conectar', command=self.connect)
        self.b_connect.grid(row=4, column=1)

        #Main frame
        self.f_main = LabelFrame(self.root, text='Mensagens', bg='blue', bd='3')
        self.f_main.pack()

        self.t_chat = Text(self.f_main)
        self.t_chat.grid(row=0)

        self.e_message = Entry(self.f_main)
        self.e_message.grid(row=1)

        #Bottom frame
        self.f_bottom = Frame(self.root, bg='yellow', bd="3")
        self.f_bottom.pack(side=BOTTOM)

        self.b_send = Button(self.f_bottom, text="Enviar", command=self.send_message)
        self.b_send.grid()

        self.root.mainloop()

    def connect(self):
        self.client = Client(self.e_server.get(), int(self.e_port.get()), self.e_identifier.get())
        self.client.connect()
        self.t_chat.insert('1.0', 'Conectado')
        self.t_chat.insert('1.0', '\n')
        message_manager = Message_Manager(self.client, self.t_chat)
        message_manager.start()

    def send_message(self):
        print('Enviando msg:', self.e_message.get())
        self.client.send_message(self.e_identifier.get(), self.e_to.get(), self.e_message.get())


client_desktop = Client_Desktop()
