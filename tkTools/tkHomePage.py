import tkTools.tkUtil as tkUtil
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals

class HomePage(tkUtil.Page):
    def __init__(self, root):
        super().__init__(root, "Home", "Homies, it's marblin time")
        
        self.historicData = tk.Label(self.frame, text="Historic Data:", font=("Arial", 12))
        self.historicData.place(x=tkUtil.WIDTH/2, y=100.0, anchor="center")
        
        
        self.reminderMsg = tk.Label(self.frame, text="Did you finish copying marbles output to data/marbles_output.txt?", font=("Arial", 12))
        self.reminderMsg.place(x=tkUtil.WIDTH/2, y=400.0, anchor="center")
        
        self.statsLabels = {}
        
        points.load_state()
        self.gridframe = tk.Frame(self.frame)
        self.init_labels()
    
    def init_labels(self):
        """Initializes and packs the header and summoner stat labels."""
        self.gridframe.pack(padx=10, pady=10)
        
        # Headers
        headers = ["Name", "Money", "Kills", "Deaths", "Assists"]
        for col, header in enumerate(headers):
            label = tk.Label(self.gridframe, text=header, font=("Arial", 10, "bold"), anchor="w")
            label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
        
        # Initialize and place summoner stat labels
        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            self.statsLabels[key] = {
                "name": tk.Label(self.gridframe, text=key),
                "money": tk.Label(self.gridframe, text=f"${summoner.money}"),
                "kills": tk.Label(self.gridframe, text=summoner.kills),
                "deaths": tk.Label(self.gridframe, text=summoner.deaths),
                "assists": tk.Label(self.gridframe, text=summoner.assists),
            }
            
            # Position each label in the grid
            self.statsLabels[key]["name"].grid(row=row, column=0, padx=5, pady=5)
            self.statsLabels[key]["money"].grid(row=row, column=1, padx=5, pady=5)
            self.statsLabels[key]["kills"].grid(row=row, column=2, padx=5, pady=5)
            self.statsLabels[key]["deaths"].grid(row=row, column=3, padx=5, pady=5)
            self.statsLabels[key]["assists"].grid(row=row, column=4, padx=5, pady=5)

    def update_labels(self):
        """Updates the displayed data for each summoner."""
        for key, summoner in globals.summoners.items():
            self.statsLabels[key]["money"].config(text=f"${summoner.money}")
            self.statsLabels[key]["kills"].config(text=summoner.kills)
            self.statsLabels[key]["deaths"].config(text=summoner.deaths)
            self.statsLabels[key]["assists"].config(text=summoner.assists)

    def hide(self):
        super().hide()
        self.gridframe.place_forget()
    
    def show(self):
        super().show()
        self.gridframe.place(x=tkUtil.WIDTH/2, y=200.0, anchor="center")
        self.update_labels()
        
        # write game money adjustment to file
        output = points.map_to_json(globals.summoners)
        points.save_state(output)

def createHomePage(root):
    return HomePage(root)