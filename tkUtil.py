import tkinter as tk
from tkinter import messagebox

WIDTH = 600
HEIGHT = 600

root = None
curPage = 0
pages = []


def popup(title, msg):
    messagebox.showinfo(title, msg)
    
def getLabelTxt(label):
    return label.cget("text")


class Page:
    def __init__(self, root, title, message):
        self.root = root
        self.frame = tk.Frame(root)
        
        # Title
        self.title_label = tk.Label(self.frame, text=title, font=("Arial", 18, "bold"))
        self.title_label.place(x=5.0, y=5.0, anchor="nw")

        # Message
        self.message_label = tk.Label(self.frame, text=message, font=("Arial", 12),
                                bg="lightblue", wraplength=200)
        self.message_label.pack(pady=5)

        # Next button in the bottom-right corner
        self.next_button = tk.Button(self.frame, text="Ok", font=("Arial", 12), 
                                    command=next_page)
        self.next_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def init_animations(self):
        if(not getLabelTxt(self.message_label) == ""):
            self.animate_message(self.message_label)

    # slide westwards
    def animate_message(self, label):
        start_x = WIDTH + 100
        target_x = WIDTH
        y_position = 60
        
        # Move the label in increments to create the slide-in effect
        def slide():
            nonlocal start_x
            if start_x > target_x:
                start_x -= 5  # Adjust step size for smoother/faster animation
                label.place(x=start_x, y=y_position, anchor="ne")
                self.root.after(10, slide)  # Repeat the slide function every 10 milliseconds
            else:
                label.place(x=target_x, y=y_position, anchor="ne")  # Final position

        # Start the sliding animation
        slide()

    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()

def next_page():
    global curPage
    curPage = (curPage + 1)%len(pages)
    show_page(curPage)

def show_page(page_num):
    # Hide all pages
    for frame in pages:
        frame.hide()
    
    # Show the selected page
    pages[page_num].show()
    
    # animate any new messages
    pages[page_num].animate_message(pages[page_num].message_label)