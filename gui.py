import tkinter as tk


class GUI(tk.Tk):
    '''
    def __init__(self, master, client):
        self.master = master
        self.master.title = "P2P Chat"

        self.client = client

        self.messages_frame = tkinter.Frame(self.master)
        self.my_msg = tkinter.StringVar()  # For the messages to be sent.
        self.my_msg.set("")
        self.scrollbar = tkinter.Scrollbar(self.messages_frame)  # To navigate through past messages.
        # Following will contain the messages.
        self.msg_list = tkinter.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()

        self.entry_field = tkinter.Entry(self.master, textvariable=self.my_msg)
        self.entry_field.bind("<Return>", self.send_msg)
        self.entry_field.pack()
        self.send_button = tkinter.Button(self.master, text="Send", command=self.send_msg)
        self.send_button.pack()

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
    '''
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Initialize_Page)

    def switch_frame(self, frame_class):
        # Destroy the current frame and replace it with the new one
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

class Initialize_Page(tk.Frame):    
    def __init__(self, master):
        tk.Frame.__init__(self,master)
        print("Asking for inputs!")
        tk.Label(self, text="Please provide your inputs").grid(row=0, columnspan=2)
        
        # Add two text boxes
        tk.Label(self, text="Host").grid(row=1, sticky='W', padx=4)
        tk.Label(self, text="Port").grid(row=2, sticky='W',padx=4)

        self.host = tk.Entry(self)
        self.host.grid(row=1, column=1)
        self.port = tk.Entry(self)
        self.port.grid(row=2, column=1)
        
        # tk.Button(self, text="Open page one").pack()
        # tk.Button(self, text="Open page two").pack()
        tk.Button(self, text='Join', command=lambda:master.switch_frame(start_Chatroom)).grid(row=3, column=0, sticky='W', pady=4)
        tk.Button(self, text='Quit', command=master.quit).grid(row=3, column=2, pady=4, sticky='E')
        tk.Button(self, text='Check', command=lambda:self.printVal()).grid(row=3, column=1, sticky='W', pady=4)

    def printVal(self):
        print(self.host.get())
        print(self.port.get())
        
        
class start_Chatroom(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self,master)
        print("Get ready to chat!")
        tk.Label(self, text="Welcome to the chatroom!").grid(row=0, columnspan=2)
        print("Host: ")
        print("Port: ")
        tk.Button(self, text='Quit', command=master.quit).grid(row=1, column=1, pady=4, sticky='E')
        tk.Button(self, text="Return to credentials page",command=lambda: master.switch_frame(Initialize_Page)).grid(row=1, column=0, pady=4, sticky='E')

    def update_msg(self):
        while True:
            msg = self.client.receive()
            self.msg_list.insert(tkinter.END, msg)
            # Auto scrolls to the bottom of the text box
            self.msg_list.see("end")

    def send_msg(self, event=None):
        msg = self.my_msg.get()
        self.client.send(msg)
        self.my_msg.set("")
        if msg == "{quit}":
            self.master.quit()

    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.my_msg.set("{quit}")
        self.send_msg()

if __name__ == "__main__":
    app = GUI()
    app.mainloop()