import tkTools.tkUtil as tkUtil
import backendTools.webtools as webtools
import backendTools.points as points
import backendTools.globals as globals
import tkinter as tk

class PostgamePage(tkUtil.Page):
    def __init__(self, root):
        super().__init__(root, "Post-Game", "ggs")
        
        # todo show updated money
        # self.getEarnings()
        self.headers = []
        self.info_labels = {}
        self.infoFrame = tk.Frame(self.frame)
        
        self.init_labels()
    
    def init_labels(self):
        """Initializes and packs header labels and placeholders for data labels."""
        headers = ["Game Name", "Kills", "Deaths", "Assists", "Vision Score", "Is Support"]

        # Create header labels
        for col, header in enumerate(headers):
            label = tk.Label(self.infoFrame, text=header, font=('Arial', 12, 'bold'))
            label.grid(row=0, column=col, padx=10, pady=5)
            self.headers.append(label)

        # Initialize data labels for each summoner
        for row in range(1, 6):  # We know there are always 5 entries
            summonerName = globals.allSummoners[row - 1]
            self.info_labels[summonerName] = {}

            # Create labels for each column in the row
            self.info_labels[summonerName]["name"] = tk.Label(self.infoFrame, text="")
            self.info_labels[summonerName]["name"].grid(row=row, column=0, padx=10, pady=5)
            self.info_labels[summonerName]["kills"] = tk.Label(self.infoFrame, text="")
            self.info_labels[summonerName]["kills"].grid(row=row, column=1, padx=10, pady=5)
            self.info_labels[summonerName]["deaths"] = tk.Label(self.infoFrame, text="")
            self.info_labels[summonerName]["deaths"].grid(row=row, column=2, padx=10, pady=5)
            self.info_labels[summonerName]["assists"] = tk.Label(self.infoFrame, text="")
            self.info_labels[summonerName]["assists"].grid(row=row, column=3, padx=10, pady=5)
            self.info_labels[summonerName]["vision"] = tk.Label(self.infoFrame, text="")
            self.info_labels[summonerName]["vision"].grid(row=row, column=4, padx=10, pady=5)
            self.info_labels[summonerName]["support"] = tk.Label(self.infoFrame, text="")
            self.info_labels[summonerName]["support"].grid(row=row, column=5, padx=10, pady=5)

    def update_data(self, playerData):
        """Updates existing labels with new data from playerData."""
        for row, (gameName, stats) in enumerate(playerData.items(), start=1):
            # Retrieve stats
            kills = stats["kills"]
            deaths = stats["deaths"]
            assists = stats["assists"]
            vision = stats["vision"]
            is_supp = stats["position"] == "SUPPORT"
            
            summonerName = globals.get_summoner_name_by_game_name(gameName)
            
            # Update label text using config
            self.info_labels[summonerName]["name"].config(text=summonerName)
            self.info_labels[summonerName]["kills"].config(text=kills)
            self.info_labels[summonerName]["deaths"].config(text=deaths)
            self.info_labels[summonerName]["assists"].config(text=assists)
            self.info_labels[summonerName]["vision"].config(text=vision)
            self.info_labels[summonerName]["support"].config(text="Yes" if is_supp else "No")
    
    # assume webbot always works lol
    def updateEarnings(self):
        # webtools.updateOPGG() # api does not rely on op gg
        playerData = points.scoreAdjust() # don't write to file until accepted by next button (homepage)
        self.update_data(playerData) 
        
    def hide(self):
        super().hide()
        self.infoFrame.pack_forget()
        self.frame.place_forget()
    
    def show(self):
        super().show()
        self.infoFrame.pack(padx=10, pady=10)
        self.updateEarnings()

def createPostgamePage(root):
    homepage = PostgamePage(root)
    return homepage