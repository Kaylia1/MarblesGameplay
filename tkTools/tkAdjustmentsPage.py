import tkTools.tkUtil as tkUtil
import tkTools.tkPickingPage as tkPickingPage
import backendTools.wheelMap as wheelMap
import tkTools.uiMoney as uiMoney
import tkTools.uiWinrates as uiWinrates
import tkTools.uiAssignments as uiAssignments
# import tkTools.tkMoney as tkMoney
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals
import backendTools.rules as rules
import backendTools.parseChampStats as parseChampStats
import tkTools.tkWheelPage as tkWheelPage

class AdjustmentsPage(tkUtil.Page):
    def __init__(self, root):
        super().__init__(root, "Wheel / Bribe Page", "huh")
        self.entry = tk.Entry(self.frame, width=30)
        self.entry.place(x=300, y=540.0, anchor="w")
        
        self.submit_button = tk.Button(self.frame, text="Spin!", command=self.submit)
        self.submit_button.place(x=500, y=540.0, anchor="w")
        self.button_pressed = tk.StringVar()
        self.entered_text = ""
        
        # bribery
        self.initBribery()
        
        # money, assignments, winrates items in display
        self.moneyDisplay = uiMoney.Money(self.frame)
        self.assignmentsDisplay = uiAssignments.Assignments(self.frame)

        # put winrates on the bottom so it is ok if the ui is too large
        self.winratesDisplay = uiWinrates.Winrates()

    def updateAssignments(self, unpickedSummoners=globals.allSummoners):
        self.assignmentsDisplay.updateAssignmentLabels(unpickedSummoners)
        self.winratesDisplay.updateWinrateGrid()
    
    def submit(self):
        self.button_pressed.set("button pressed")
        # print("SPINNING WHEEL???")
        self.entered_text = self.entry.get()  # Get the text from the entry box
        # print("Read input:", self.entered_text)
        for summonerName in globals.allSummoners:
            if(self.entered_text.lower() == summonerName.lower() and globals.summoners[(self.entered_text[0].upper() + self.entered_text[1:].lower())].money >= 100):
                wheelMap.lastSpinner = self.entered_text[0].upper() + self.entered_text[1:].lower() # TODO bad coding practice to manually make first letter uppercase
                globals.summoners[wheelMap.lastSpinner].money -= 100
                tkUtil.trigger_wheel_page()
                break
        self.entry.delete(0, tk.END)
    
    # =================== BRIBE BUTTON ==========================
    def initBribery(self):
        # List of valid inputs
        # valid_inputs = globals.allSummoners  # Replace with your valid inputs
        self.bribeFrame = tk.Frame(self.root)

        self.bribePrompt = tk.Label(self.bribeFrame, text="Bribery\n from, to, amount")
        self.bribePrompt.pack(pady=5)

        # Create text entry boxes
        self.name1 = tk.Entry(self.bribeFrame)
        self.name1.pack(pady=5)

        self.name2 = tk.Entry(self.bribeFrame)
        self.name2.pack(pady=5)

        self.money = tk.Entry(self.bribeFrame)
        self.money.pack(pady=5)
        
        # Create submit button
        self.bribe_button = tk.Button(self.bribeFrame, text="Bribe", command=self.submit_inputs)
        self.bribe_button.pack(pady=20)
    
    # TODO NEED TO RENAME THESE
    def submit_inputs(self):
        lowercase_summoners = [summoner.lower() for summoner in globals.allSummoners]  # Convert all to lowercase

        input1 = self.name1.get().strip().lower()  # Get input and convert to lowercase
        input2 = self.name2.get().strip().lower()  # Get input and convert to lowercase
        input3 = self.money.get().strip()  # Get the third input without changing case for number check

        self.name1.delete(0, tk.END)
        self.name2.delete(0, tk.END)
        self.money.delete(0, tk.END)

        if input1 in lowercase_summoners and input2 in lowercase_summoners:
            if input3.isdigit() and int(input3) >= 0 and globals.summoners[input1[0].upper() + input1[1:].lower()].money>=int(input3):
                print(f"Inputs are valid: {input1}, {input2}, {input3}")
                # self.bribe_button.config(state=tk.DISABLED)  # Disable the submit button
                
                globals.summoners[input1[0].upper() + input1[1:].lower()].money -= int(input3)
                globals.summoners[input2[0].upper() + input2[1:].lower()].money += int(input3)
                self.setMessageLabel("Bribery accepted")
                self.updateSummonerMoney()
            else:
                self.setMessageLabel("The third input must be a non-negative number.")
        else:
            self.setMessageLabel("The first two inputs must summoner names.")
    
    # =================== CONTROL ==========================
    
    def hide(self):
        super().hide()
        self.frame.place_forget()
        self.bribeFrame.place_forget()
        # self.hide_stat_frames()
        
        self.moneyDisplay.hide()
        self.assignmentsDisplay.hide()
        self.winratesDisplay.hide()
        
    def show(self):
        super().show()
        self.winratesDisplay.assignMaster(self.frame)
        
        self.bribeFrame.place(x=800, y=600.0, anchor="w")
        
        # run main assignments program
        
        self.setMessageLabel("last wheel result:\n"+tkWheelPage.wheel_result)
        
        self.moneyDisplay.updateMoneyLabels()
        self.moneyDisplay.show()
        self.updateAssignments()
        self.assignmentsDisplay.show()
        self.winratesDisplay.show()
        

def createAdjustmentsPage(root):
    return AdjustmentsPage(root)