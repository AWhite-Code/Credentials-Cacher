import tkinter as tk
from tkinter import messagebox

# This will 
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Credentials Cacher")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        init_width = int(screen_width * 0.4)
        init_height = int(screen_height * 0.2)

        position_x = int((screen_width - init_width) / 2)
        position_y = int((screen_height - init_height) / 2)

        self.root.geometry(f"{init_width}x{init_height}+{position_x}+{position_y}")
        self.root.minsize(300, 150)

        self.setup_ui()

    def setup_ui(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_columnconfigure(2, weight=1)

        # Username Entry with inline label
        self.username_entry = PlaceholderEntry(self.root, placeholder="Username")
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Password Entry with inline label
        self.password_entry = PlaceholderEntry(self.root, placeholder="Password", show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Login Button with proportional width
        self.login_button_frame = tk.Frame(self.root)
        self.login_button_frame.grid(row=2, column=1, pady=10, sticky="ew")

        # Use frame to control button width proportionally
        self.login_button_frame.grid_columnconfigure(0, weight=3)  # padding
        self.login_button_frame.grid_columnconfigure(1, weight=1)  # button width
        self.login_button_frame.grid_columnconfigure(2, weight=3)  # padding

        self.login_button = tk.Button(self.login_button_frame, text="Login", command=self.login_action)
        self.login_button.grid(row=0, column=1, sticky="ew")

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "Username *" or password == "Password *":
            messagebox.showinfo("Login Failed", "Please enter your username and password.")
        else:
            messagebox.showinfo("Login info", f"Username: {username}, Password: {password}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()