#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

top = tkinter.Tk()
top.title("Chat Room")

def callback(event):
    print("Clicked!")
    my_msg.delete(0, 'end')

def key(event):
    print("pressed", repr(event.char))

def on_closing():
    """This function is to be called when the window is closed."""
    # my_msg.set("{quit}")
    top.destroy()

messages_frame = tkinter.Frame(top)
# For the messages to be sent.
my_msg = tkinter.StringVar()  
my_msg.set("Type your messages here.")
tkinter.Label(top, textvariable = my_msg).pack()
# To navigate through past messages.
scrollbar = tkinter.Scrollbar(messages_frame)  
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)

# Packing
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Key>", key)
entry_field.pack()

send_button = tkinter.Button(top, text="Send", command=key)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

tkinter.mainloop()  # Starts GUI execution.