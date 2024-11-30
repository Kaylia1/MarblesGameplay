import tkinter as tk

class StyledButton(tk.Button):
    def __init__(self, parent=None, text="Button", bg="#4CAF50", activeforeground="#ffffff", **kwargs):
        # Set up the default styling parameters
        default_style = {
            "font": ("Helvetica", 12, "bold"),
            "fg": activeforeground,
            "bg": bg,
            "activebackground": "#45a049",
            "activeforeground": activeforeground,
            "relief": "raised",
            "bd": 3,
            "padx": 10,
            "pady": 5,
            "width": None,
            "height": None,
            "highlightbackground": bg,
            "highlightthickness": 0,
        }
        
        self.inactive_style = {
            "fg": "#aaaaaa",
            "bg": "#555555",
            "activebackground": "#555555",
            "activeforeground": "#aaaaaa",
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
            # Disable the button and apply the inactive style
            # self.config(state="normal", **self.inactive_style)
            self.config(state="disabled", **self.inactive_style)
            
    
    def on_enter(self, event):
        def hex_to_rgb(hex_color):
            """Convert hex color string to RGB tuple"""
            return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        def rgb_to_hex(r, g, b):
            """Convert RGB tuple to hex color string"""
            return f'#{r:02x}{g:02x}{b:02x}'
        def make_color_darker(color, factor):
            """Takes the current color and adjusts the green component to make it 'more green'"""
            r, g, b = hex_to_rgb(color)
            g = min(255, int(g * factor))  # Increase green component
            return rgb_to_hex(r, g, b)
        
        current_color = self.cget("bg")
        
        # Adjust the color to make it more green
        # We can make the green more intense by adding a bit more to the RGB green component
        new_color = make_color_darker(current_color, 1.4)  # Example: Increase the green

        # Change background to more green shade
        self.config(bg=new_color)

    def on_leave(self, event):
        current_state = self.cget("state")
        
        if current_state == "normal":
            # Button is active, revert to original active color
            self.config(bg=self.active_style["bg"])
        else:
            # Button is inactive (disabled), stay in inactive color
            self.config(bg=self.inactive_style["bg"])
