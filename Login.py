import tkinter as tk
from tkinter import messagebox
from placeholder_entry import PlaceholderEntry
import pickle

class LoginFrame(tk.Frame):
    def __init__(self, master, on_show_other_frame):
        super().__init__(master)
        self.on_show_other_frame = on_show_other_frame

        # Set the frame to expand to the available space
        self.grid(row=0, column=0, sticky='nsew')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Set minsize
        self.master.minsize(450, 450)
        self.master.maxsize(1000,700)

        # Scale the window based on screen size
        self.window_width = int(self.master.winfo_screenwidth() * 0.3)
        self.window_height = int(self.master.winfo_screenheight() * 0.25)
        self.master.geometry(f"{self.window_width}x{self.window_height}")

        # Define maximum widths for widgets based on a percentage of the window's width
        self.max_text_field_width = self.window_width * 0.1
        self.max_button_width = self.window_width * 0.1

        # Draw widgets onto the screen
        self.create_widgets()

        # Bind the resize event
        self.master.bind('<Configure>', self.on_resize)

    def create_widgets(self):
        # Get the desired width of the window
        window_width = self.master.winfo_width()

        # Calculate the desired width for the text fields and button
        text_field_width = window_width * 0.5
        button_width = window_width * 0.4
        
        # Generate the three columns. column 1 has a higher weight to improve spacing
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        
        # Generate all the rows for GUI grid
        for i in range(7):
            self.rowconfigure(i, weight=1)
        
        title_label = tk.Label(self, text="Credential Cacher", font=("Helvetica", 24, "bold"))
        title_label.grid(row=1, column=0, columnspan=3, pady=(10, 20), sticky='nsew')

        # Create the username and password entries
        self.username_entry = PlaceholderEntry(self, placeholder="Username...")
        self.username_entry.grid(row=3, column=0, columnspan=3, padx=20, pady=(20, 10))
        self.username_entry.config(width=int(min(text_field_width, self.max_text_field_width)))

        self.password_entry = PlaceholderEntry(self, placeholder="Password...", show="*")
        self.password_entry.grid(row=4, column=0, columnspan=3, padx=20, pady=10)
        self.password_entry.config(width=int(min(text_field_width, self.max_text_field_width)))
        
        # Create the forgot my password "hyperlink"
        self.forgot_password_label = tk.Label(self, text="Forgot my password", fg="blue", cursor="hand2")
        self.forgot_password_label.grid(row=5, column=1, sticky='nesw')
        self.forgot_password_label.bind("<Button-1>", lambda event: self.on_show_other_frame())

        # Create a remember username checkbox
        self.remember_var = tk.BooleanVar()
        self.remember_check = tk.Checkbutton(self, text="Remember Username", variable=self.remember_var)
        self.remember_check.grid(row=6, column=0, columnspan=3, padx=20, pady=10)

        # Create the login button
        self.login_button = tk.Button(self, text="Login", command=self.login_action)
        self.login_button.grid(row=7, column=0, columnspan=3, padx=20, pady=(10, 20))
        self.login_button.config(width=int(min(button_width, self.max_button_width)))
    
    # Calls Window.py function to swap frame to registration
    def forgot_password(self, event=None):
        self.on_show_other_frame()
        
    # This method should be passed to the LoginFrame upon initialization, sort of an artifact now and needs to be cleaned up on next refactor   
    def on_show_other_frame(self):
        self.master.toggle_frames()        
            
    # Logic for changing UI when window is resized, not much functionality right now.        
    def on_resize(self, event):
        # Calculate the new widths based on the new window size
        text_field_width = event.width * 0.5
        button_width = event.width * 0.4

        # Update the width of the text fields and button
        self.username_entry.config(width=int(min(text_field_width, self.max_text_field_width)))
        self.password_entry.config(width=int(min(text_field_width, self.max_text_field_width)))
        self.login_button.config(width=int(min(button_width, self.max_button_width)))
    
    # Function to read from user input and call validation function    
    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate the login information
        if self.validate_login(username, password):
            messagebox.showinfo("Access Granted", "Welcome! Your login information is correct.")
        else:
            messagebox.showinfo("Login Failed", "The username or password is incorrect.")

    # Reads credentails file and validates that passed inputs are the same as data stored in file. 
    # WARNING THIS IS UNENCRYPTED, ADD HASHING NEXT AND PASS DECRYPT FUNCITON INTO HERE.
    def validate_login(self, username, password):
        try:
            with open('credentials.bin', 'rb') as file:
                credentials = pickle.load(file)
                if credentials['username'] == username and credentials['password'] == password:
                    return True
        except FileNotFoundError: # File not found
            messagebox.showerror("Error", "Credentials file not found.")
        except Exception as e: # Unknown error
            messagebox.showerror("Error", f"An error occurred: {e}")
        return False
                