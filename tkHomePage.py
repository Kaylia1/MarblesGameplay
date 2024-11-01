import tkUtil
import tkinter as tk
import points
import globals

class HomePage(tkUtil.Page):
    def __init__(self, root):
        super().__init__(root, "Home", "Homies, it's marblin time")
        
        self.historicData = tk.Label(self.frame, text="Historic Data:", font=("Arial", 12))
        self.historicData.place(x=tkUtil.WIDTH/2, y=100.0, anchor="center")
        
        
        self.reminderMsg = tk.Label(self.frame, text="Did you finish copying marbles output to data/marbles_output.txt?", font=("Arial", 12))
        self.reminderMsg.place(x=tkUtil.WIDTH/2, y=400.0, anchor="center")
        
        self.statsLabels = []
        
        points.load_state()
        self.showSummonerData()
        print("running this")
    
    def showSummonerData(self):
        self.gridframe = tk.Frame(self.root)
        self.gridframe.place(x=tkUtil.WIDTH/2, y=200.0, anchor="center")
        headers = ["Name", "Money", "Kills", "Deaths", "Assists"]
        for col, header in enumerate(headers):
            self.statsLabels.append(tk.Label(self.gridframe, text=header, font=("Arial", 10, "bold"), anchor="w").grid(row=0, column=col, padx=5, pady=5, sticky="w"))

        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            # Display each attribute of the Summoner object in a new column
            self.statsLabels.append(tk.Label(self.gridframe, text=summoner.name).grid(row=row, column=0, padx=5, pady=5))
            self.statsLabels.append(tk.Label(self.gridframe, text="$"+str(summoner.money)).grid(row=row, column=1, padx=5, pady=5))
            self.statsLabels.append(tk.Label(self.gridframe, text=summoner.kills).grid(row=row, column=2, padx=5, pady=5))
            self.statsLabels.append(tk.Label(self.gridframe, text=summoner.deaths).grid(row=row, column=3, padx=5, pady=5))
            self.statsLabels.append(tk.Label(self.gridframe, text=summoner.assists).grid(row=row, column=4, padx=5, pady=5))

def createHomePage(root):
    return HomePage(root)