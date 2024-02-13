import tkinter as tk
from tkinter import messagebox
from placeholder_entry import PlaceholderEntry

class RegistrationFrame(tk.Frame):
    def __init__(self, master, on_show_other_frame):
        super().__init__(master)
        self.on_show_other_frame = on_show_other_frame

        # Set the frame to expand to the available space
        self.grid(row=0, column=0, sticky='nsew')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Set minsize
        self.master.minsize(300, 450)

        # Scale the window based on screen size
        self.window_width = int(self.master.winfo_screenwidth() * 0.3)
        self.window_height = int(self.master.winfo_screenheight() * 0.25)
        self.master.geometry(f"{self.window_width}x{self.window_height}")

        self.create_widgets()

        # Bind the resize event
        self.master.bind('<Configure>', self.on_resize)

    def create_widgets(self):
        # Configure the grid layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        
        for i in range(8):
            self.rowconfigure(i, weight=1)

        # Add a big title label
        title_label = tk.Label(self, text="Register", font=("Helvetica", 24, "bold"))
        title_label.grid(row=1, column=0, columnspan=3, pady=(10, 20), sticky='nsew')

        # Create the username, password, and confirm password entries
        self.username_entry = PlaceholderEntry(self, placeholder="Username...")
        self.username_entry.grid(row=3, column=0, columnspan=3, padx=20, pady=(20, 10))

        self.password_entry = PlaceholderEntry(self, placeholder="Password...", show="*")
        self.password_entry.grid(row=4, column=0, columnspan=3, padx=20, pady=10)

        self.confirm_password_entry = PlaceholderEntry(self, placeholder="Confirm Password...", show="*")
        self.confirm_password_entry.grid(row=5, column=0, columnspan=3, padx=20, pady=10)

        # Password requirements box
        password_requirements = tk.Label(self, text="Password requirements:\n- Minimum 8 characters\n- At least one number\n- At least one special character", justify=tk.LEFT)
        password_requirements.grid(row=6, column=0, columnspan=3, padx=20, pady=(5, 20), sticky='w')

        # Create the register button
        self.register_button = tk.Button(self, text="Register", command=self.register_action)
        self.register_button.grid(row=6, column=0, columnspan=3, padx=20, pady=(10, 20))

        # Create the switch to login button
        self.switch_button = tk.Button(self, text="Switch to Login", command=self.on_show_other_frame)
        self.switch_button.grid(row=7, column=0, columnspan=3, padx=20, pady=0)

    def register_action(self):
        # Perform registration logic here
        pass

    def on_resize(self, event):
        # Resizing logic, similar to login frame
        pass
