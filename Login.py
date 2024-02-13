import tkinter as tk
from tkinter import messagebox
from placeholder_entry import PlaceholderEntry

class LoginFrame(tk.Frame):
    def __init__(self, master, on_show_other_frame):
        super().__init__(master)
        self.on_show_other_frame = on_show_other_frame
        
        # Set the frame to expand to the available space
        self.grid(row=0, column=0, sticky='nsew')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        
        # Set minsize
        self.master.minsize(300, 150)
        
        # Scale the window based on screen size
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = int(screen_width * 0.4)
        window_height = int(screen_height * 0.25)
        self.master.geometry(f"{window_width}x{window_height}")
        
        self.create_widgets()

    def create_widgets(self):
        # Configure the grid layout for scalability
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # Create the username and password entries
        self.username_entry = PlaceholderEntry(self, placeholder="Username...")
        self.username_entry.grid(row=0, column=0, padx=20, pady=(20, 10), sticky='ew')

        self.password_entry = PlaceholderEntry(self, placeholder="Password...", show="*")
        self.password_entry.grid(row=1, column=0, padx=20, pady=10, sticky='ew')

        # Create a remember username checkbox
        self.remember_var = tk.BooleanVar()
        self.remember_check = tk.Checkbutton(self, text="Remember Username", variable=self.remember_var)
        self.remember_check.grid(row=2, column=0, padx=20, pady=10, sticky='w')

        # Create the login button
        self.login_button = tk.Button(self, text="Login", command=self.login_action)
        self.login_button.grid(row=3, column=0, padx=20, pady=(10, 20), sticky='ew')

        # Create the switch to registration button
        self.switch_button = tk.Button(self, text="Switch to Registration", command=self.on_show_other_frame)
        self.switch_button.grid(row=4, column=0, padx=20, pady=10, sticky='sw')

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "Username *" or password == "Password *":
            messagebox.showinfo("Login Failed", "Please enter your username and password.")
        else:
            messagebox.showinfo("Login info", f"Username: {username}, Password: {password}")