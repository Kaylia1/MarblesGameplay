import tkTools.tkUtil as tkUtil
import backendTools.points as points
import tkinter as tk
import backendTools.globals as globals
import firebase.firebaseTools as firebaseTools

class MidgamePage(tkUtil.Page):
    def __init__(self, root):
        super().__init__(root, "Mid-Game", "good luck mates")
        
        self.reminderMsg = tk.Label(self.frame, text="Did the game finish?", font=("Arial", 12))
        self.reminderMsg.place(x=tkUtil.WIDTH/2, y=400.0, anchor="center")
        
    def hide(self):
        super().hide()
        self.frame.place_forget()
    
    def show(self):
        super().show()
        
        # write wheel adjustment money to file
        output = points.map_to_json(globals.summoners)
        firebaseTools.fb.storeData(output)

def createMidgamePage(root):
    homepage = MidgamePage(root)
    return homepage