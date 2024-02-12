# login.py
import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x150")

        self.setup_ui()

    def setup_ui(self):
        # Username field
        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1)

        # Password field
        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1)

        # Login button
        self.login_button = tk.Button(self.root, text="Login", command=self.login_action)
        self.login_button.grid(row=2, column=1)

    def login_action(self):
        # Placeholder for login logic
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Here, you should include your logic to check the username and password
        messagebox.showinfo("Login info", f"Username: {username}, Password: {password}")