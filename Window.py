import tkinter as tk
from Login import LoginFrame
from Registration import RegistrationFrame

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Credentials Cacher")

        # Initialize frames
        self.frames = {}
        self.frames['registration'] = RegistrationFrame(self.root, self.toggle_frames)
        self.frames['login'] = LoginFrame(self.root, self.toggle_frames)

        # Display initial frame
        self.show_frame('login')      
        self.current_frame = 'login'  # Initialize current frame

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
