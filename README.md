# P2PChat
## EC441 Final Project 
### Written by Ryan Ewing and David Li
#### 12.11.18

This project uses the Python 3 interpreter. 

There are three files in this application:
* Client.py - 
* GUI.py - 
* Server.py - 

The functions in each file is described below.

## Client.py
#### def connect()
Connects to an ip and a port (a server essentially)

#### def host_server()
Starts a server

#### def run() 
Main loop to receive data and write data to a socket

#### def process_message()
Processes a recevied message; depending on the type, takes a different action 
* Message
* Private
* login
* transfer 
* connect

#### def send_message()
Sends a message

#### def notify_server()
Log in and log out, notifies the server of an action, changes the client itself, in most cases, just places the action in the queue

## Server.py
#### def init()
Binds the socket to a host and port (address) and listens to it for connections

#### def run()
Main thread, keeps the server alive while you want it to

### Each of these functions is a separate thread:
* **def listen()**
    Thread listening to incoming connections
* **def receive()** 
    Receives data and calls process_data on the data
* **def send()**
    Sends a message from the queue if there is one to be sent

#### def send_to_all()
Sends the data to all the users

#### def send_to_one() 
Specified function that sends to one specific target. Used for whisper and transfer of server

#### def process_data()
Similar to process_message
When sending data across sockets, most have an encoding, cannot just send strings

#### def remove_connection()
Removes a user / socket that disconnected from the list

#### def update_login_list()
Tell users about a new person who joins the lobby, tells users to update list

## GUI.py

### Run function 

First creates a LogInWindow, expect it to move on
However, the login window keeps running until a button is pressed
This is how the windows "Switch"

#### def run() - login window starts, keeps running until button pressed, then chat_window is built, not run yet, then server is notified of login, and then the chat window starts

