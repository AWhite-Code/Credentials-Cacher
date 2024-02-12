import tkinter as tk

class MainWindow:
    def __init__(self, root):
        self.root = root

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate window size and position
        window_width = int(screen_width * 0.6)  # 60% of screen width
        window_height = int(screen_height * 0.6)  # 60% of screen height
        position_x = int((screen_width - window_width) / 2)
        position_y = int((screen_height - window_height) / 2)

        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        self.root.title("Credentials Cacher")

        self.setup_ui(window_width, window_height)

    def setup_ui(self, window_width, window_height):
        # Example of positioning a button dynamically
        button_width = int(window_width * 0.1)  # 10% of window width
        button_height = 2  # Assuming a standard height for simplicity
        button_x = int(window_width * 0.45)  # Center horizontally
        button_y = int(window_height * 0.8)  # Position towards the bottom

        self.example_button = tk.Button(self.root, text="Example Button")
        self.example_button.place(width=button_width, height=button_height, x=button_x, y=button_y)