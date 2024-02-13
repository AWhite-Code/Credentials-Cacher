import tkinter as tk
from tkinter import messagebox
from placeholder_entry import PlaceholderEntry

class LoginFrame(tk.Frame):
    def __init__(self, master, on_show_other_frame):
        super().__init__(master)
        self.grid(row=0, column=0, sticky='nsew')
        self.create_widgets()
        self.on_show_other_frame = on_show_other_frame

    def create_widgets(self):
        self.username_entry = PlaceholderEntry(self, placeholder="Username")
        self.username_entry.grid(row=0, column=0, padx=10, pady=10)

        self.password_entry = PlaceholderEntry(self, placeholder="Password", show="*")
        self.password_entry.grid(row=1, column=0, padx=10, pady=10)

        self.login_button = tk.Button(self, text="Login", command=self.login_action)
        self.login_button.grid(row=2, column=0, padx=10, pady=10)

        self.switch_button = tk.Button(self, text="Switch to Registration", command=self.on_show_other_frame)
        self.switch_button.grid(row=3, column=0, padx=10, pady=10)

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "Username *" or password == "Password *":
            messagebox.showinfo("Login Failed", "Please enter your username and password.")
        else:
            messagebox.showinfo("Login info", f"Username: {username}, Password: {password}")