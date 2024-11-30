import tkinter as tk

class StyledLabel(tk.Label):
    def __init__(self, parent, text="", **kwargs):
        # Default style attributes
        style_defaults = {
            "text": text,
            "font": ("Helvetica", 12, "bold"),
            "fg": "black",
            "bg": "white",
            "borderwidth": 2,
            "relief": "flat",         # options: flat, groove, raised, ridge, solid, or sunken
            "padx": 5,
            "pady": 5,
            "anchor": "center",       # options: n, ne, e, se, s, sw, w, nw, or center
            "justify": "center",      # options: left, center, or right
            "width": None,
            "height": None,
            "wraplength": 0,          # wrap text in pixels
            "underline": -1,          # index to underline, -1 means no underline
            "bitmap": None,           # bitmap name if you want to use a bitmap instead of text
            "compound": "none",       # display bitmap and text together; options: bottom, center, left, none, right, top
            "cursor": "arrow"         # mouse cursor when hovering over the label
        }

        # Override defaults with any provided style kwargs
        style = {**style_defaults, **kwargs}
        
        # Initialize Label with all style parameters
        super().__init__(parent, **style)

# Creating a StyledLabel with custom parameters
# label = StyledLabel(
#     root,
#     text="Hello, Styled Label!",
#     font=("Helvetica", 14, "bold"),
#     fg="blue",
#     bg="lightgray",
#     borderwidth=4,
#     relief="groove",
#     padx=10,
#     pady=10,
#     anchor="w",
#     justify="left",
#     wraplength=150,
#     underline=6,
#     cursor="hand2"
# )
# label.pack(pady=20)
