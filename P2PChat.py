from GUI import GUI
from Client import Client
from Server import Server

from tkinter import Tk
from threading import Thread


def main():
    # ----Now comes the sockets part----
    start_server = input('Host new server (y/n): ')
    HOST = input('Enter host: ')
    PORT = input('Enter port: ')
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)

    ADDR = (HOST, PORT)

    server = None

    if start_server.lower() == 'y':
        server = Server(HOST, PORT)
        server_thread = Thread(target=server.run_server())
        server_thread.start()

    print("GOT HERE")
    client = Client(ADDR)

    root = Tk()
    my_gui = GUI(root, client)

    receive_thread = Thread(target=my_gui.update_msg)
    receive_thread.start()

    root.mainloop()

    server.shutdown()


if __name__ == "__main__":
    main()
