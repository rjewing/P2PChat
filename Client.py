#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM


class Client:
    def __init__(self, addr):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(addr)
        self.BUFSIZ = 1024

        self.msg = ""

    def receive(self):
        """Handles receiving of messages."""
        try:
            return self.client_socket.recv(self.BUFSIZ).decode("utf8")
        except OSError:  # Possibly client has left the chat.
            return ""

    def send(self, msg="", event=None):  # event is passed by binders.
        """Handles sending of messages."""
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    def get_msg(self):
        return self.msg




