# P2PChat
## Written by Ryan Ewing and David Li
## EC441 Final Project 

Python - not actual read threading, uses locking, smart switching between processes - pretend they work

There are three files in this application:
* Client.py - 
* GUI.py - 
* Server.py - 

# Client.py
def connect - connects to an ip and a port (a server essentially)

def host_server - starts a server

def run() - main loop to receive data and write data to a socket

def process_message() - processes a recevied message; depending on the type, takes a different action 
* Message
* Private
* login
* transfer 
* connect

def send_message() - sends a message

def notify_server() - log in and log out, notifies the server of an action, changes the client itself, in most cases, just places the action in the queue

# Server.py
def init - binds the socket to a host and port (address) and listens to it for connections

def run() - main thread, keeps the server alive while you want it to

### Each a separate thread
    def listen() - thread listening to incoming connections
    def receive() - receives data and calls process_data on the data
    def send() - sends a message from the queue if there is one to be sent

def send_to_all - sends the data to all the users

def send_to_one - specified function that sends to one specific target
    Used for whisper and transfer of server

def process_data - similar to process_message
    When sending data across sockets, most have an encoding, cannot just send strings

def remove_connection - removes a user / socket that disconnected from the list

def update_login_list - tell users about a new person who joins the lobby, tells users to update list

# GUI.py

Tricking part 
### Run function 

First creates a LogInWindow, expect it to move on
However, the login window keeps running until a button is pressed
This is how the windows "Switch"

def run() - login window starts, keeps running until button pressed, then chat_window is built, not run yet, then server is notified of login, and then the chat window starts

