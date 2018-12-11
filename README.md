# P2PChat
## EC441 Final Project 
### Written by Ryan Ewing and David Li
#### 12.11.18

This project uses the Python 3 interpreter. 

How to use:
1. 
2. 
3. 
4. 
5. 
6. 

There are three files in this application:
* Client.py 
* GUI.py 
* Server.py

The functions in each file is described below.

## Client.py
This file is responsible for 
* **def connect()** - Connects to an ip and a port (this is a server essentially).
* **def host_server()** - Starts a server.
* **def run()** - Main loop to receive data and write data to a socket.
* **def process_message()** - Processes a recevied message; depending on the type, takes a different action. Here are the different types of messages:
    * Message
    * Private
    * login
    * transfer 
    * connect

* **def send_message()** - Sends a message.
* **def notify_server()** - Log in and log out, notifies the server of an action, and changes the client itself. In most cases, just places an action in the queue.

## Server.py
This file is responsible for 

* **def init()** - Binds the socket to a host and port (address) and listens to it for connections.
* **def run()** - Main thread, keeps the server alive while you want it to.

### Each of these functions is a separate thread:
* **def listen()** - Thread listening to incoming connections.
* **def receive()** - Receives data and calls process_data on the data.
* **def send()** - Sends a message from the queue if there is one to be sent.

* **def send_to_all()** - Sends the data to all the users.
* **def send_to_one()** - Specified function that sends to one specific target. Used for whisper and transfer of server.
* **def process_data()** - Functionality is similar to process_message. When sending data across sockets, most have an encoding. You cannot just send strings across the connection.
* **def remove_connection()** - Removes a user / socket that disconnected from the list.
* **def update_login_list()** - Tell users about a new person who joins the lobby and tells users to update their list.

## GUI.py
This file is responsible for 

There are four different classes in this file:
1. GUI

    * **def run()** - 
    * *static methods* - 
    * **logout()** - 
    * **center()** -  
2. Window
    Initializes the window. Sets the parameters for the font and title.

3. LoginWindow

    * **def build_window()** - 
    * **def run()** - 
    * **def join_server()** - 
    * **def start_server()** - 
    
4. ChatWindow

    * **def build_window()** - 
    * **def run()** - 
    * **def display_message()** - 
    * **def transfer_server()** - 
    * **def display_message()** - 
    * **def on_closing_event()** - 
    * **def exit_event()** - 
    * **def send_entry_event()** - 
    * **def selected_login_event()** - 
    * **def update_login_list()** - 


First creates a LogInWindow, expect it to move on
However, the login window keeps running until a button is pressed
This is how the windows "Switch"

#### def run() 
Login window starts, keeps running until button pressed, then chat_window is built, not run yet, then server is notified of login, and then the chat window starts

