import tkinter as tk

class StyledButton(tk.Button):
    def __init__(self, parent, text="Button", **kwargs):
        # Set up the default styling parameters
        default_style = {
            "font": ("Helvetica", 12, "bold"),
            "fg": "white",
            "bg": "#4CAF50",
            "activebackground": "#45a049",
            "activeforeground": "white",
            "relief": "raised",
            "bd": 3,
            "padx": 10,
            "pady": 5,
            "width": None,
            "height": None,
            "highlightbackground": "#4CAF50",
            "highlightthickness": 0,
        }
        
        self.inactive_style = {
            "fg": "gray70",
            "bg": "gray50",
            "activebackground": "gray50",
            "activeforeground": "gray70",
        }
        
        # Merge user-provided kwargs with default styling
        self.active_style = {**default_style, **kwargs}
        
        # Initialize button with the parent, text, and merged styling
        super().__init__(parent, text=text, **self.active_style)

        # Bind hover effects
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    # wrapper function to change styles on active or inactive
    def set_active(self, is_active):
        if is_active:
            # Enable the button and apply the active style
            self.config(state="normal", **self.active_style)
        else:
            print("inactive styling")
            # Disable the button and apply the inactive style
            self.config(state="disabled", **self.inactive_style)
    
    def on_enter(self, event):
        self.config(bg="#45a049")

    def on_leave(self, event):
        self.config(bg="#4CAF50")
