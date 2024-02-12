import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # Dynamically set the window size based on screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Define window size as a fraction of screen size
        window_width = int(screen_width * 0.3)  # 30% of screen width
        window_height = int(screen_height * 0.2)  # 20% of screen height
        position_x = int((screen_width - window_width) / 2)
        position_y = int((screen_height - window_height) / 2)

        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.setup_ui(window_width, window_height)

    def setup_ui(self, window_width, window_height):
        # Calculate positions and sizes for UI elements dynamically
        label_width = int(window_width * 0.2)
        entry_width = int(window_width * 0.6)
        button_width = int(window_width * 0.3)
        vertical_spacing = int(window_height * 0.15)
        
        # Username label and entry
        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.place(x=10, y=vertical_spacing, width=label_width)

        self.username_entry = tk.Entry(self.root)
        self.username_entry.place(x=label_width + 20, y=vertical_spacing, width=entry_width)

        # Password label and entry
        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.place(x=10, y=vertical_spacing * 2, width=label_width)

        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.place(x=label_width + 20, y=vertical_spacing * 2, width=entry_width)

        # Login button
        self.login_button = tk.Button(self.root, text="Login", command=self.login_action)
        self.login_button.place(x=window_width/2 - button_width/2, y=vertical_spacing * 3, width=button_width)

    def login_action(self):
        # Placeholder for login logic
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Here, you should include your logic to check the username and password
        messagebox.showinfo("Login info", f"Username: {username}, Password: {password}")