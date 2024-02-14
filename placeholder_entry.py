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

    # Add place holder to text box
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self['show'] =  '*' if self.hide_text and self.get() != self.placeholder else ''     # Only apply masking if hide_text is True and it's not displaying placeholder

    # User focused/selected the text box
    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            self['show'] = '*' if self.hide_text else ''        # Apply masking based on the hide_text flag

    # User unfocused/selected the text box
    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
            self['show'] = ''                                   # Ensure masking removed if showing placeholder again
