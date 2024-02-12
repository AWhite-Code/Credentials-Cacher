# login.py
import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # Calculate initial window size as 50% of screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        init_width = int(screen_width * 0.5)
        init_height = int(screen_height * 0.5)

        # Calculate position to center the window on the screen
        position_x = int((screen_width - init_width) / 2)
        position_y = int((screen_height - init_height) / 2)

        # Apply calculated dimensions and position
        self.root.geometry(f"{init_width}x{init_height}+{position_x}+{position_y}")
        self.root.minsize(300, 150)  # Ensure a reasonable minimum size

        self.setup_ui()

    def setup_ui(self):
        # Grid layout configuration
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)

        # Username Label and Entry
        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Password Label and Entry
        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Login Button
        self.login_button = tk.Button(self.root, text="Login", command=self.login_action)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def login_action(self):
        # Placeholder for login logic
        username = self.username_entry.get()
        password = self.password_entry.get()
        messagebox.showinfo("Login info", f"Username: {username}, Password: {password}")