import tkTools.tkUtil as tkUtil
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals
import backendTools.rules as rules
import backendTools.parseChampStats as parseChampStats
import tkTools.tkPickingPage as tkPickingPage

# is this actually less efficient since it is creating a whole new class that also has stat data?

class AdjustmentsPage(tkPickingPage.PickingPage):
    def __init__(self, root):
        super().__init__(root) #, "Adjustments Page", "Wheel or Bribe?")
    
    # =================== CONTROL ==========================
    
    def hide(self):
        super().hide()
    
    def show(self):
        tkUtil.Page.show(self) # bypass the tkPickingPage show method
        self.gridframe.place(x=0, y=200.0, anchor="w")
        self.show_stat_frames()

def createAdjustmentsPage(root):
    return AdjustmentsPage(root)