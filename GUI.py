import tkinter


class GUI:
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


    def update_msg(self):
        while True:
            msg = self.client.receive()
            self.msg_list.insert(tkinter.END, msg)

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

