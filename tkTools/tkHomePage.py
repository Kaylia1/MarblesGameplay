import tkTools.tkUtil as tkUtil
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals
# import tkTools.Assets.StyledLabel as StyledLabel
import firebase.firebaseTools as firebaseTools
import backendTools.rules as rules

entered_text = ""
class HomePage(tkUtil.Page):
    def __init__(self, root):
        super().__init__(root, "Home", "Homies, it's marblin time")
        
        self.historicData = tk.Label(self.frame, text="Historic Data:", font=("Arial", 24))
        self.historicData.place(x=tkUtil.WIDTH/2, y=70.0, anchor="center")
        
        
        self.reminderMsg = tk.Label(self.frame, text="Did you finish copying marbles output to data/marbles_output.txt?", font=("Arial", 24))
        self.reminderMsg.place(x=tkUtil.WIDTH/2, y=400.0, anchor="center")
        
        self.statsLabels = {}
        
        points.load_state(firebaseTools.fb.loadData())
        self.gridframe = tk.Frame(self.frame)
        self.init_labels()
        
        self.text_box = tk.Text(self.frame, wrap="word", font=("Arial", 12))
        self.text_box.place(relx=0.05, rely=0.4, relwidth=0.9, relheight=0.5)
        
        # self.isHidden = True
    
    def read_text(self):
        # Get the text from the Text widget
        # start reading from first line
        print("Read Marble Text")
        marblesData = self.text_box.get("1.0", tk.END).strip()  # Strip removes trailing newline
        self.text_box.delete("1.0", tk.END)
        readStatus = rules.readMarbles(marblesData)
        parseStatus = rules.initGetBestMarbles()
        return readStatus and parseStatus
        
    
    def init_labels(self):
        """Initializes and packs the header and summoner stat labels."""
        self.gridframe.pack(padx=10, pady=10)
        
        # Headers
        headers = ["Name", "Money", "Kills", "Deaths", "Assists"]
        for col, header in enumerate(headers):
            label = tk.Label(self.gridframe, text=header, font=("Arial", 14, "bold"), anchor="w")
            label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
        
        # Initialize and place summoner stat labels
        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            self.statsLabels[key] = {
                "name": tk.Label(self.gridframe, text=key, font=("Arial", 14)),
                "money": tk.Label(self.gridframe, text=f"${summoner.money}", font=("Arial", 14)),
                "kills": tk.Label(self.gridframe, text=summoner.kills, font=("Arial", 14)),
                "deaths": tk.Label(self.gridframe, text=summoner.deaths, font=("Arial", 14)),
                "assists": tk.Label(self.gridframe, text=summoner.assists, font=("Arial", 14)),
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
        # if not self.isHidden: # read marble data upon click of next when homepage first goes from show->hide
        #     self.read_text()
        # self.isHidden = True
    
    def show(self):
        super().show()
        self.gridframe.place(x=tkUtil.WIDTH/2, y=200.0, anchor="center")
        self.update_labels()
        
        # write game money adjustment to file
        # output = points.map_to_json(globals.summoners)
        # firebaseTools.fb.storeData(output)
        # self.isHidden = False
    
    def handleNext(self):
        print("Handling")
        if self.read_text():
            # Move on to next page
            print("Successfully parsed input")
            super().handleNext()
        else:
            self.setMessageLabel("Failed to parse marble input due to bad format")

def createHomePage(root):
    return HomePage(root)