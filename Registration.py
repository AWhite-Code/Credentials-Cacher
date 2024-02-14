import tkinter as tk
from tkinter import messagebox
from placeholder_entry import PlaceholderEntry
import re
import pickle
from Hashing import Hashing

class RegistrationFrame(tk.Frame):
    def __init__(self, master, on_show_other_frame):
        super().__init__(master)
        self.on_show_other_frame = on_show_other_frame

        # Set the frame to expand to the available space
        self.grid(row=0, column=0, sticky='nsew')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

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

        self.password_entry = PlaceholderEntry(self, placeholder="Password...")
        self.password_entry.grid(row=4, column=0, columnspan=3, padx=20, pady=10)

        self.confirm_password_entry = PlaceholderEntry(self, placeholder="Confirm Password...")
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

    def on_resize(self, event):
        # Calculate the new widths based on the new window size
        text_field_width = event.width * 0.5
        button_width = event.width * 0.4

        # Update the width of the text fields and button
        self.username_entry.config(width=int(min(text_field_width, self.max_text_field_width)))
        self.password_entry.config(width=int(min(text_field_width, self.max_text_field_width)))
        self.confirm_password_entry(width=int(min(text_field_width, self.max_text_field_width)))
        self.register_button.config(width=int(min(button_width, self.max_button_width)))
        
    # Takes inputs from GUI and validates them, if correct saves them to binary file and moves user to Login frame    
    def register_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if password != confirm_password:
            messagebox.showerror("Registration Failed", "Password and Confirm password do not match")
        elif not self.validate_password(password):  # Using 'not' for clarity
            messagebox.showerror("Registration Failed", "Password does not meet requirements, please try again")
        else:
            self.clear_credentials()  # Clear any existing credentials
            hashed_password = Hashing.hash_password(password)  # Hash the password
            self.save_credentials(username, hashed_password)  # Save the new credentials
            messagebox.showinfo("Registration Success", "You have been registered successfully.")
            
            # For demonstration purposes, show the username and hashed password
            self.show_credentials(username, hashed_password)
            
            #self.on_show_other_frame()  # Optionally switch to login frame after successful registration

    
    def clear_credentials(self):
        open('credentials.bin', 'wb').close()     
        
    def show_credentials(self, username, hashed_password):
        # Construct the message string with the username and hashed password
        credentials_info = f"Username: {username}\nHashed Password: {hashed_password}"
        
        # Display the credentials in a popup message box
        messagebox.showinfo("Registration Details", credentials_info)
    

    ''' 
    Password must adhear to the following requirements:
    8 or more characters
    Must feature a number
    Must have 1 or more special characters
    '''
    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search("[0-9]", password):
            return False
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    # After validate, this will save user inputs to credentials.bin, seperating details with "username" and "password" <- This is will change with hashing later
    def save_credentials(self, username, hashed_password):
        # Here, `hashed_password` already contains the salt and hash
        credentials = {'username': username, 'password': hashed_password}
        with open('credentials.bin', 'wb') as file:
            pickle.dump(credentials, file)

    # Calls Window.py function to swap to Login.py
    def on_show_other_frame(self):
        self.master.toggle_frames()