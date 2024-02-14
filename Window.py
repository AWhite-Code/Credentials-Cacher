import tkinter as tk
from Login import LoginFrame
from Registration import RegistrationFrame
import os
import pickle

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Credentials Cacher")

        # Initialize frames
        self.frames = {}
        self.frames['registration'] = RegistrationFrame(self.root, self.toggle_frames)
        self.frames['login'] = LoginFrame(self.root, self.toggle_frames)

        # Decide which frame to show on start
        self.current_frame = 'login' if self.check_credentials_exist() else 'registration'
        self.show_frame(self.current_frame)

    def show_frame(self, frame_key):
        frame = self.frames[frame_key]
        frame.tkraise()

    def toggle_frames(self):
        if self.current_frame == 'login':
            self.show_frame('registration')
            self.current_frame = 'registration'
        else:
            self.show_frame('login')
            self.current_frame = 'login'

    def check_credentials_exist(self):
        # Check if the binary file exists and is not empty
        if os.path.exists('credentials.bin'):
            try:
                with open('credentials.bin', 'rb') as file:
                    # Try to load the credentials
                    credentials = pickle.load(file)
                    return bool(credentials)  # Return True if credentials are not empty
            except EOFError:
                # Empty file
                return False
        return False

# Usage example
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()