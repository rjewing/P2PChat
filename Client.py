#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM, error
import queue
import time
import select

from GUI import *
# from server_select import Server
# from server_multi import Server
from server_multithreaded import Server

ENCODING = 'utf-8'


class Client(threading.Thread):
    def __init__(self, host='localhost', port=33000):
        super().__init__(daemon=True, target=self.run)

        self.addr = (host, int(port))
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.connected = False

        self.buffer_size = 1024

        self.queue = queue.Queue()
        self.lock = threading.RLock()

        self.login = ''
        self.target = ''
        self.login_list = []

        self.gui = GUI(self)
        self.start()
        self.gui.start()

        self.server = None

    def connect(self, host, port):
        try:
            self.addr = (host, int(port))
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.addr)
            self.connected = True
            print("Connected!")
        except ConnectionRefusedError:
            print("Server is inactive, unable to connect")
            return False
        return True

    def host_server(self, host, port):
        self.server = Server(host, int(port))
        return self.server

    def run(self):
        """Handle client-server communication using select module"""
        while not self.connected:
            pass
        inputs = [self.client_socket]
        outputs = [self.client_socket]
        while inputs:
            try:
                if self.client_socket != inputs[0] or self.client_socket != outputs[0]:
                    inputs = [self.client_socket]
                    outputs = [self.client_socket]
                read, write, exceptional = select.select(inputs, outputs, inputs)
            # if server unexpectedly quits, this will raise ValueError exception (file descriptor < 0)
            except ValueError:
                print('Server error: select')
                GUI.display_alert('Server error has occurred. Exit app')
                self.client_socket.close()
                break

            if self.client_socket in read:
                with self.lock:
                    try:
                        data = self.client_socket.recv(self.buffer_size)
                    except error:
                        print("Socket error: read")
                        GUI.display_alert('Socket error has occurred. Exit app')
                        self.client_socket.close()
                        break

                self.process_message(data)

            if self.client_socket in write:
                if not self.queue.empty():
                    data = self.queue.get()
                    self.send_message(data)
                    self.queue.task_done()
                else:
                    time.sleep(0.05)

            if self.client_socket in exceptional:
                print('Server error: exception')
                GUI.display_alert('Server error has occurred. Exit app')
                self.client_socket.close()
                break

    def process_message(self, data):
        if data:
            message = data.decode(ENCODING)
            message = message.split('\n')

            for msg in message:
                if msg != '':
                    msg = msg.split(';')
                    if msg[0] == 'msg':
                        text = msg[1] + ': ' + msg[3] + '\n'
                        print(msg)
                        self.gui.display_message(text)

                        # if chosen login is already in use
                        if msg[2] != self.login and msg[2] != 'ALL':
                            self.login = msg[2]
                    elif msg[0] == 'priv':
                        text = '[whisper] ' + msg[1] + ': ' + msg[3] + '\n'
                        print(msg)
                        self.gui.display_message(text)
                    elif msg[0] == 'login':
                        self.gui.main_window.update_login_list(msg[1:])
                    elif msg[0] == 'transfer':
                        self.host_server(host='', port=33000)
                        self.gui.server = self.server
                    elif msg[0] == 'connect':
                        addr = msg[3].split('|')
                        host = addr[0]
                        port = int(addr[1])
                        print(host)
                        print(port)
                        self.client_socket.close()
                        self.connect(host, port)
                        print('Login = ' + self.login)
                        self.gui.login(self.login)

    def send_message(self, data, event=None):  # event is passed by binders.
        """Handles sending of messages."""
        with self.lock:
            try:
                self.client_socket.send(data)
            except error:
                self.client_socket.close()
                GUI.display_alert('Server error has occurred. Exit app')

    def notify_server(self, action, action_type):
        """Notify server if action is performed by client"""
        self.queue.put(action)
        print(action)
        if action_type == "login":
            self.login = action.decode(ENCODING).split(';')[1]
            print(self.login)
        elif action_type == "logout":
            self.client_socket.close()


if __name__ == '__main__':
    client = Client()
