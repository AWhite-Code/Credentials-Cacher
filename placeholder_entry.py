import tkinter as tk

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', hide_text=False, **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.hide_text = hide_text  # Add a flag to control text masking

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        # Only apply masking if hide_text is True and it's not displaying placeholder
        self['show'] = '*' if self.hide_text and self.get() != self.placeholder else ''

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            # Apply masking based on the hide_text flag
            self['show'] = '*' if self.hide_text else ''

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
            # Ensure masking is removed if showing placeholder again
            self['show'] = ''
