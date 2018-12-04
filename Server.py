#!/usr/bin/env python3
"""Server for multi-threaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Server:
    def __init__(self, host='', port=33000):
        self.clients = {}
        self.addresses = {}

        self.BUFSIZ = 1024
        self.addr = (host, port)

        self.SERVER = None

    def run_server(self):
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(self.addr)

        self.SERVER.listen(5)
        print("Waiting for connection...")
        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()
        # ACCEPT_THREAD.join()
        # self.SERVER.close()

    def shutdown(self):
        self.SERVER.close()


    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = self.SERVER.accept()
            print("%s:%s has connected." % client_address)
            client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):  # Takes client socket as argument.
        """Handles a single client connection."""

        name = client.recv(self.BUFSIZ).decode("utf8")
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!" % name
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name

        while True:
            msg = client.recv(self.BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                self.broadcast(msg, name + ": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del self.clients[client]
                self.broadcast(bytes("%s has left the chat." % name, "utf8"))
                break

    def broadcast(self, msg, prefix=""):  # prefix is for name identification.
        """Broadcasts a message to all the clients."""

        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    server = Server()
    server.run_server()
