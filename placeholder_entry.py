import tkinter as tk

# Custom text box widget that displays a placeholder string inside of it as grey text.
# Once user starts writing it is overwritten, if required it can be masked. 
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
        self['show'] = ''  # No masking when showing the placeholder

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            self['show'] = '*'  # Mask input after placeholder is removed

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()