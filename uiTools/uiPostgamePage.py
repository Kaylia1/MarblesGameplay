import uiTools.uiPage as uiPage
import backendTools.webtools as webtools
import backendTools.points as points
import backendTools.globals as globals
import tkinter as tk
import firebase.firebaseTools as firebaseTools

class PostgamePage(uiPage.Page):
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
            label = tk.Label(self.infoFrame, text=header, font=('Arial', 14, 'bold'))
            label.grid(row=0, column=col, padx=10, pady=5)
            self.headers.append(label)

        # Initialize data labels for each summoner
        for row in range(1, 6):  # We know there are always 5 entries
            summonerName = globals.allSummoners[row - 1]
            self.info_labels[summonerName] = {}

            # Create labels for each column in the row
            self.info_labels[summonerName]["name"] = tk.Label(self.infoFrame, text="", font=('Arial', 14))
            self.info_labels[summonerName]["name"].grid(row=row, column=0, padx=10, pady=5)
            self.info_labels[summonerName]["kills"] = tk.Label(self.infoFrame, text="", font=('Arial', 14))
            self.info_labels[summonerName]["kills"].grid(row=row, column=1, padx=10, pady=5)
            self.info_labels[summonerName]["deaths"] = tk.Label(self.infoFrame, text="", font=('Arial', 14))
            self.info_labels[summonerName]["deaths"].grid(row=row, column=2, padx=10, pady=5)
            self.info_labels[summonerName]["assists"] = tk.Label(self.infoFrame, text="", font=('Arial', 14))
            self.info_labels[summonerName]["assists"].grid(row=row, column=3, padx=10, pady=5)
            self.info_labels[summonerName]["vision"] = tk.Label(self.infoFrame, text="", font=('Arial', 14))
            self.info_labels[summonerName]["vision"].grid(row=row, column=4, padx=10, pady=5)
            self.info_labels[summonerName]["support"] = tk.Label(self.infoFrame, text="", font=('Arial', 14))
            self.info_labels[summonerName]["support"].grid(row=row, column=5, padx=10, pady=5)

    def update_data(self, playerData, support):
        """Updates existing labels with new data from playerData."""
        for row, (name, stats) in enumerate(playerData.items(), start=1):
            # Retrieve stats
            kills = stats["kills"]
            deaths = stats["deaths"]
            assists = stats["assists"]
            vision = stats["vision"]
            is_supp = support == name
            
            # Update label text using config
            self.info_labels[name]["name"].config(text=name)
            self.info_labels[name]["kills"].config(text=kills)
            self.info_labels[name]["deaths"].config(text=deaths)
            self.info_labels[name]["assists"].config(text=assists)
            self.info_labels[name]["adjusted-vision"].config(text=vision)
            self.info_labels[name]["support"].config(text="Yes" if is_supp else "No")
    
    # Read data from riot and update db and display
    def updateEarnings(self):
        playerData, support = points.scoreAdjust()
        
        # Assume Riot API works, write to firebase immediately
        output = points.map_to_json(globals.summoners)
        firebaseTools.fb.storeData(output)
        self.update_data(playerData, support) 
        
    def hide(self):
        super().hide()
        self.infoFrame.pack_forget()
        self.frame.place_forget()
    
    def show(self):
        super().show()
        self.infoFrame.place(x=350, y=250.0, anchor="w")
        self.updateEarnings()
        globals.totalGames += 1
        print("Showing earnings")

def createPostgamePage(root):
    homepage = PostgamePage(root)
    return homepage