import tkinter as tk
from tkinter import messagebox
import uiTools.Assets.StyledButton as StyledButton
from PIL import Image, ImageTk, ImageEnhance

WIDTH = 1800
HEIGHT = 800

root = None
curPage = 0
pages = []

wheelPage = None
wheelResPage = None

pageDesc = {
    "0": "Homepage",
    "1": "Picking",
    "2": "Adjustments",
    "3": "Midgame",
    "4": "Postgame",
    "wheel": "Wheel",
    "wheel res": "Wheel result"
}


def popup(title, msg):
    messagebox.showinfo(title, msg)
    
def getLabelTxt(label):
    return label.cget("text")

def getCurPage():
    global curPage
    return pageDesc[str(curPage)]

class Page:
    IMAGE_PATH = "images/marblesreviews.png"
    IMAGE_SIZE = (WIDTH, HEIGHT)
    processed_image = None
    
    def __init__(self, root, title, message):
        self.root = root
        self.frame = tk.Frame(root)
        
        self.setup_background_image()
        # create label and add resize image
        self.label1 = tk.Label(self.frame, image=Page.processed_image)
        self.label1.image = Page.processed_image
        self.label1.pack()
        
        # Title
        self.title_label = tk.Label(self.frame, text=title, font=("Arial", 24, "bold"))
        self.title_label.place(x=5.0, y=5.0, anchor="nw")
        
        # Message
        self.message_label = tk.Label(self.frame, text=message, font=("Arial", 24),
                                bg="lightblue", wraplength=1000)
        # self.message_label.pack(pady=5)

        # Next button in the bottom-right corner
        self.next_button = StyledButton.StyledButton(self.frame, text="Ok", font=("Arial", 12), 
                                    command=self.handleNext)
        self.next_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    @staticmethod
    def setup_background_image():
        # Process image only once and cache the result
        if Page.processed_image is None:
            image = Image.open(Page.IMAGE_PATH)
            enhancer = ImageEnhance.Brightness(image)
            faded_image = enhancer.enhance(1.4) # inc brightness
            saturation_enhancer = ImageEnhance.Color(faded_image)
            faded_image = saturation_enhancer.enhance(0.4) # dec saturation
            resize_image = faded_image.resize(Page.IMAGE_SIZE)
            Page.processed_image = ImageTk.PhotoImage(resize_image)

    def init_animations(self):
        if(not getLabelTxt(self.message_label) == ""):
            self.animate_message(self.message_label)

    def setMessageLabel(self, newTxt):
        self.message_label.config(text=newTxt)
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
    
    def setNextButtonState(self, state):
        self.next_button.set_active(is_active=state)
            

    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()
    
    def handleNext(self):
        next_page()

def next_page():
    global curPage
    print("last page was: "+str(curPage))
    curPage = (curPage + 1)%len(pages)
    show_page(curPage)

# note: adjustments page is page 2
def show_page(page_num):
    # Hide all pages
    wheelPage.hide()
    wheelResPage.hide()
    global curPage
    curPage = page_num
    for i, page in enumerate(pages):
        if not i == page_num:
            page.hide()
    
    # Show the selected page
    pages[page_num].show()
    
    # animate any new messages
    pages[page_num].animate_message(pages[page_num].message_label)
    
def trigger_wheel_page():
    global curPage
    curPage = "wheel"
    for i, page in enumerate(pages):
        page.hide()
    wheelResPage.hide()
    wheelPage.show()

def trigger_wheel_res_page():
    global curPage
    curPage = "wheel res"
    for i, page in enumerate(pages):
        page.hide()
    wheelPage.hide()
    wheelResPage.show()