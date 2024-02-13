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
        self.window_width = int(self.master.winfo_screenwidth() * 0.4)
        self.window_height = int(self.master.winfo_screenheight() * 0.25)
        self.master.geometry(f"{self.window_width}x{self.window_height}")

        # Define maximum widths for widgets based on a percentage of the window's width
        self.max_text_field_width = self.window_width * 0.2
        self.max_button_width = self.window_width * 0.4

        self.create_widgets()

        # Bind the resize event
        self.master.bind('<Configure>', self.on_resize)

    def create_widgets(self):
        # Get the desired width of the window
        window_width = self.master.winfo_width()

        # Calculate the desired width for the text fields and button
        text_field_width = window_width * 0.5
        button_width = window_width * 0.4
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        # Create the username and password entries
        self.username_entry = PlaceholderEntry(self, placeholder="Username...")
        self.username_entry.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10))
        self.username_entry.config(width=int(min(text_field_width, self.max_text_field_width)))

        self.password_entry = PlaceholderEntry(self, placeholder="Password...", show="*")
        self.password_entry.grid(row=1, column=0, columnspan=3, padx=20, pady=10)
        self.password_entry.config(width=int(min(text_field_width, self.max_text_field_width)))

        # Create a remember username checkbox
        self.remember_var = tk.BooleanVar()
        self.remember_check = tk.Checkbutton(self, text="Remember Username", variable=self.remember_var)
        self.remember_check.grid(row=2, column=0, padx=20, pady=10, sticky='w')

        # Create the login button
        self.login_button = tk.Button(self, text="Login", command=self.login_action)
        self.login_button.grid(row=3, column=0, columnspan=3, padx=20, pady=(10, 20))
        self.login_button.config(width=int(min(button_width, self.max_button_width)))

        # Create the switch to registration button in the lower left corner
        self.switch_button = tk.Button(self, text="Switch to Registration", command=self.on_show_other_frame)
        self.switch_button.grid(row=4, column=0, padx=20, pady=10, sticky='sw')

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "Username..." or password == "Password...":
            messagebox.showinfo("Login Failed", "Please enter your username and password.")
        else:
            messagebox.showinfo("Login info", f"Username: {username}, Password: {password}")
            
    def on_resize(self, event):
        # Calculate the new widths based on the new window size
        text_field_width = event.width * 0.5
        button_width = event.width * 0.4

        # Update the width of the text fields and button
        self.username_entry.config(width=int(min(text_field_width, self.max_text_field_width)))
        self.password_entry.config(width=int(min(text_field_width, self.max_text_field_width)))
        self.login_button.config(width=int(min(button_width, self.max_button_width)))
                