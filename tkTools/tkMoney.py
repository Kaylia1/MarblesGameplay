import tkTools.tkUtil as tkUtil
import tkTools.tkAssignments as tkAssignments
import tkinter as tk
import backendTools.globals as globals

# page with both money and assignments
class MoneyPage(tkAssignments.AssignmentsPage):
    def __init__(self, root, pageName, messageText):
        super().__init__(root, pageName, messageText)
        
        self.moneyFrame = None
        self.moneyLabels = []
        self.initSummonerMoney()

    # =================== MONEY ============================
    
    def initSummonerMoney(self):
        self.moneyFrame = tk.Frame(self.root)
        
        headers = ["Name", "Money"]
        for col, header in enumerate(headers):
            self.moneyLabels.append(tk.Label(self.moneyFrame, text=header, font=("Arial", 24, "bold"), anchor="w"))
            self.moneyLabels[-1].grid(row=0, column=col, padx=5, pady=5, sticky="w")

        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            # key is summoner name
            # Display each attribute of the Summoner object in a new column
            self.moneyLabels.append(tk.Label(self.moneyFrame, text=key, font=("Arial", 24)))
            self.moneyLabels[-1].grid(row=row, column=0, padx=5, pady=5)
            self.moneyLabels.append(tk.Label(self.moneyFrame, text="$"+str(summoner.money), font=("Arial", 24)))
            self.moneyLabels[-1].grid(row=row, column=1, padx=5, pady=5)
        
        # self.canvas2 = tk.Canvas(self.root, width=200, height=200, bd=0, highlightthickness=0)
        
    
    def updateSummonerMoney(self):
        name = ""
        for i in range(2, len(self.moneyLabels)):
            if(i%2==0):
                name = tkUtil.getLabelTxt(self.moneyLabels[i])
            else:
                self.moneyLabels[i].config(text="$"+str(globals.summoners[name].money))
    
    # =================== CONTROL ==========================
    
    def hide(self):
        super().hide()
        self.moneyFrame.place_forget()
        
    def show(self):
        super().show()
        # self.rect = self.canvas.create_rectangle(0, 600, 300, 200, fill="white", outline="white")
        # self.canvas2.place(x=0, y=600)  # Same position as the frame
        self.moneyFrame.place(x=0, y=600.0, anchor="w")
        self.updateSummonerMoney()