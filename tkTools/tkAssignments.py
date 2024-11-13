import tkinter as tk
import tkTools.tkUtil as tkUtil
import backendTools.rules as rules
import backendTools.globals as globals

class AssignmentsPage(tkUtil.Page):
    def __init__(self, root, pageName, messageText):
        super().__init__(root, pageName, messageText)
        
        self.curAssignments = tk.Label(self.frame, text="Current assignments:", font=("Arial", 12))
        self.curAssignments.place(x=0, y=90.0, anchor="w")
        
        self.gridframe = None # assignments grid
        
        self.headers = []
        self.assignmentHeadLabels = []
        self.assignmentLabels = {}
        
        self.initAssignmentLabels()
        
        
    def initAssignmentLabels(self):
        self.gridframe = tk.Frame(self.root)
        self.headers = ["Name", "Position", "Letter", "Level"]
        for col, header in enumerate(self.headers):
            self.assignmentHeadLabels.append(tk.Label(self.gridframe, text=header, font=("Arial", 10, "bold"), anchor="w").grid(row=0, column=col, padx=5, pady=5, sticky="w"))

        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            # Display each attribute of the Summoner object in a new column
            self.assignmentLabels[key] = {}
            self.assignmentLabels[key][self.headers[0]] = tk.Label(self.gridframe, text=key)
            self.assignmentLabels[key][self.headers[0]].grid(row=row, column=0, padx=5, pady=5)
            
            self.assignmentLabels[key][self.headers[1]] = tk.Label(self.gridframe, text="")
            self.assignmentLabels[key][self.headers[1]].grid(row=row, column=1, padx=5, pady=5)
            
            self.assignmentLabels[key][self.headers[2]] = tk.Label(self.gridframe, text="")
            self.assignmentLabels[key][self.headers[2]].grid(row=row, column=2, padx=5, pady=5)

            self.assignmentLabels[key][self.headers[3]] = tk.Label(self.gridframe, text="")
            self.assignmentLabels[key][self.headers[3]].grid(row=row, column=3, padx=5, pady=5)

    def updateAssignments(self, unpickedSummoners=globals.allSummoners):
        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            # Update each attribute of the Summoner object
            bgd = "SystemButtonFace"
            if not key in unpickedSummoners:
                bgd = "#90EE90"
            self.assignmentLabels[key][self.headers[0]].config(bg=bgd)
            self.assignmentLabels[key][self.headers[1]].config(text=rules.marbles[summoner.curMarble].position, bg=bgd)
            self.assignmentLabels[key][self.headers[2]].config(text=rules.marbles[summoner.curMarble].letter, bg=bgd)
            self.assignmentLabels[key][self.headers[3]].config(text=rules.marbles[summoner.curMarble].level, bg=bgd)
            print(rules.marbles[summoner.curMarble].marbleDesc)

    def show(self):
        super().show()
        print("UPDATING ASSIGNMENTS ")
        self.updateAssignments()
        self.gridframe.place(x=0, y=200.0, anchor="w")
    
    def hide(self):
        super().hide()
        self.gridframe.place_forget()