import tkinter as tk
import threading

from tkinter import scrolledtext
from tkinter import messagebox


ENCODING = 'utf-8'


class GUI(threading.Thread):
    def __init__(self, client):
        super().__init__(daemon=False, target=self.run)
        self.font = ('Helvetica', 13)
        self.client = client
        self.server = None
        self.login_window = None
        self.main_window = None

    def run(self):
        self.login_window = LoginWindow(self, self.font)
        print("Login done")
        self.main_window = ChatWindow(self, self.font)
        print("Main window done")
        self.notify_server(self.login_window.login, 'login')
        print("Notified server of login")

        self.main_window.run()

    @staticmethod
    def display_alert(message):
        """Display alert box"""
        messagebox.showinfo('Error', message)

    def update_login_list(self, active_users):
        """Update login list in main window with list of users"""
        self.main_window.update_login_list(active_users)

    def display_message(self, message):
        """Display message in ChatWindow"""
        self.main_window.display_message(message)

    def send_message(self, message):
        """Enqueue message in client's queue"""
        self.client.queue.put(message)

    def set_target(self, target):
        """Set target for messages"""
        self.client.target = target

    def notify_server(self, message, action):
        """Notify server after action was performed"""
        data = action + ";" + message
        data = data.encode(ENCODING)
        self.client.notify_server(data, action)

    def login(self, login):
        print(login)
        self.notify_server(login, 'login')

    def logout(self, logout):
        self.notify_server(logout, 'logout')

    def center(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class Window(object):
    def __init__(self, title, font):
        self.root = tk.Tk()
        self.title = title
        self.root.title(title)
        self.font = font


class LoginWindow(Window):
    def __init__(self, gui, font):
        super().__init__("Login", font)
        self.gui = gui
        self.label = None
        self.entry = None
        self.button = None
        self.login = None

        self.host_entry = None
        self.port_entry = None

        self.host = None
        self.port = None

        self.build_window()
        self.run()

    def build_window(self):
        self.label = tk.Label(self.root, text="Select a server to join or host your own!").grid(row=0, columnspan=3)
        
        # Add two text boxes
        tk.Label(self.root, text="Host").grid(row=1, sticky='W', padx=4)
        tk.Label(self.root, text="Port").grid(row=2, sticky='W', padx=4)
        tk.Label(self.root, text="Name").grid(row=3, sticky='W', padx=4)

        self.host_entry = tk.Entry(self.root, font=self.font)
        self.host_entry.insert(0, 'localhost')
        self.host_entry.grid(row=1, column=1)
        self.port_entry = tk.Entry(self.root, font=self.font)
        self.port_entry.insert(0, '33000')
        self.port_entry.grid(row=2, column=1)

        self.entry = tk.Entry(self.root, font=self.font)
        self.entry.grid(row=3, column=1)
        self.entry.bind('<Return>', self.join_server)

        tk.Button(self.root, text='Join', command=self.join_server).grid(row=4, column=0, sticky='W', pady=4)
        tk.Button(self.root, text='Host', command=self.start_server).grid(row=4, column=1, sticky='W', pady=4)
        tk.Button(self.root, text='Quit', command=exit).grid(row=4, column=2, pady=4, sticky='E')

    def run(self):
        """Handle login window actions"""
        self.root.mainloop()
        self.root.destroy()

    def join_server(self, event=None):
        """Get login from login box and close login window"""
        self.login = self.entry.get()
        self.host = self.host_entry.get()
        self.port = self.port_entry.get()
        if not self.host:
            self.host = 'localhost'
        if not self.port:
            self.port = 33000
        if self.gui.client.connect(self.host, int(self.port)):
            print("Connected successfully...")
            self.root.quit()
        else:
            GUI.display_alert("Unable to reach server.")

    def start_server(self, event=None):
        self.host = self.host_entry.get()
        self.port = self.port_entry.get()
        if not self.port:
            self.port = 33000
        self.gui.server = self.gui.client.host_server(self.host, self.port)
        if self.gui.server is not None:
            print('Hosted server successfully...')


class ChatWindow(Window):
    def __init__(self, gui, font):
        super().__init__("P2P Chat", font)
        self.gui = gui
        self.messages_list = None
        self.logins_list = None
        self.entry = None
        self.send_button = None
        self.exit_button = None
        self.lock = threading.RLock()
        self.target = ''
        self.login = self.gui.login_window.login

        self.build_window()

    def build_window(self):
        # Size config
        self.root.geometry('800x600')
        self.root.minsize(600, 400)

        # Frames config
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # List of messages
        frame00 = tk.Frame(main_frame)
        frame00.grid(column=0, row=0, rowspan=2, sticky=tk.N + tk.S + tk.W + tk.E)

        # List of logins
        frame01 = tk.Frame(main_frame)
        frame01.grid(column=1, row=0, rowspan=3, sticky=tk.N + tk.S + tk.W + tk.E)

        # Message entry
        frame02 = tk.Frame(main_frame)
        frame02.grid(column=0, row=2, columnspan=1, sticky=tk.N + tk.S + tk.W + tk.E)

        # Buttons
        frame03 = tk.Frame(main_frame)
        frame03.grid(column=0, row=3, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)

        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=8)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # ScrolledText widget for displaying messages
        self.messages_list = scrolledtext.ScrolledText(frame00, wrap='word', font=self.font)
        self.messages_list.insert(tk.END, 'Welcome to Python Chat\n')
        self.messages_list.configure(state='disabled')

        # Listbox widget for displaying active users and selecting them
        self.logins_list = tk.Listbox(frame01, selectmode=tk.SINGLE, font=self.font,
                                      exportselection=False)
        self.logins_list.bind('<<ListboxSelect>>', self.selected_login_event)

        # Entry widget for typing messages in
        self.entry = tk.Text(frame02, font=self.font)
        self.entry.focus_set()
        self.entry.bind('<Return>', self.send_entry_event)

        # Button widget for sending messages
        self.send_button = tk.Button(frame03, text='Send', font=self.font)
        self.send_button.bind('<Button-1>', self.send_entry_event)

        # Button for exiting
        self.exit_button = tk.Button(frame03, text='Exit', font=self.font)
        self.exit_button.bind('<Button-1>', self.exit_event)

        # Positioning widgets in frame
        self.messages_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.logins_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.send_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.exit_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        # Protocol for closing window using 'x' button
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_event)

    def run(self):
        """Handle chat window actions"""
        self.root.mainloop()
        self.root.destroy()

    def display_message(self, message):
        """Display message in ScrolledText widget"""
        with self.lock:
            self.messages_list.configure(state='normal')
            self.messages_list.insert(tk.END, message)
            self.messages_list.configure(state='disabled')
            self.messages_list.see(tk.END)

    def on_closing_event(self, event=None):
        """This function is to be called when the window is closed."""
        self.exit_event()

    def exit_event(self, event=None):
        """Send logout message and quit app when "Exit" pressed"""
        self.gui.notify_server(self.login, 'logout')
        if self.gui.server is not None:
            self.gui.server.shutdown_server()
        self.root.quit()

    def send_entry_event(self, event=None):
        """Send message from entry field to target"""
        text = self.entry.get(1.0, tk.END)
        if text != '\n' and text != 'server\n':
            msg_type = 'priv;' if self.target != 'all' else 'msg;'

            message = msg_type + self.login + ';' + self.target + ';' + text[:-1]
            print(message)
            self.gui.client.send_message(message.encode(ENCODING))
            self.entry.mark_set(tk.INSERT, 1.0)
            self.entry.delete(1.0, tk.END)
            self.entry.focus_set()
        elif text == 'server\n':
            message = "transfer;{};{};{}".format(self.login, self.target, text[:-1])
            self.gui.client.send_message(message.encode(ENCODING))
            self.gui.server.shutdown_server()
        else:
            messagebox.showinfo('Warning', 'You must enter non-empty message')

        with self.lock:
            self.messages_list.configure(state='normal')
            if text != '\n':
                if self.target != 'all':
                    msg = '[whisper] ' + self.login + ': ' + text
                else:
                    msg = self.login + ': ' + text
                self.messages_list.insert(tk.END, msg)
            self.messages_list.configure(state='disabled')
            self.messages_list.see(tk.END)


        return 'break'

    def selected_login_event(self, event):
        """Set as target currently selected login on login list"""
        target = self.logins_list.get(self.logins_list.curselection())
        self.target = target
        self.gui.set_target(target)

    def update_login_list(self, active_users):
        """Update listbox with list of active users"""
        self.logins_list.delete(0, tk.END)
        for user in active_users:
            self.logins_list.insert(tk.END, user)
        self.logins_list.select_set(0)
        self.target = self.logins_list.get(self.logins_list.curselection())


if __name__ == "__main__":
    app = GUI()
