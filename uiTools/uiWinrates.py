import uiTools.uiPage as uiPage
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals
import backendTools.rules as rules
import backendTools.parseChampStats as parseChampStats

class Winrates():
    _instance = None  # Singleton instance
    appData = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Winrates, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Ensure the instance is initialized only once
        if not hasattr(self, "initialized"):
            # Champ stats
            self.stat_frames = []
            self.stats_data_labels = {}
            self.stats_title_labels = []
            self.stats_col_title_labels = []
            self.initWinrateGrid()
        
    def show(self):
        for i, frame in enumerate(self.stat_frames):
            frame.place(x=460+260*i, y=150)
            
    def hide(self):
        for frame in self.stat_frames:
            frame.place_forget()
    
    # place onto root
    def assignMaster(self, root):
        for i in range(len(globals.allSummoners)):
            self.stat_frames[i].master = root
    
    def initWinrateGrid(self):
        for index in range(len(globals.allSummoners)):
            # Create a frame for each summoner's stat grid
            # no master frame until assigned
            frame = tk.Frame(borderwidth=2, relief="solid")
            
            self.stat_frames.append(frame)
            self.stats_data_labels[frame] = []
            
            # Add a header label to the top of the frame
            self.stats_title_labels.append(tk.Label(frame, text=globals.allSummoners[index], font=("Arial", 14, "bold")))
            self.stats_title_labels[-1].grid(row=0, column=0, columnspan=4, pady=10)  # Adjust columnspan based on the number of columns
            
            # Create header
            headers = ["Champion", "Winrate", "Matches"]
            for col, header in enumerate(headers):
                self.stats_col_title_labels.append(tk.Label(frame, text=header, font=('Arial', 14, 'bold'), borderwidth=1, relief="solid"))
                self.stats_col_title_labels[-1].grid(row=1, column=col, sticky="nsew")

    def updateWinrateGrid(self):
        def colorWinrate(winrate):
            bgd = "SystemButtonFace"
            numeric_value = float(winrate.strip('%'))
            if numeric_value > 48.0:
                bgd = "#90EE90"
            elif numeric_value < 35.0:
                bgd = "#FF9999"
            return bgd
        def colorMatches(matches):
            bgd = "SystemButtonFace"
            numeric_value = int(matches.replace(',',''))
            if numeric_value < 200:
                bgd = "#FF9999"
            return bgd
        
        # read champ stats
        Winrates.appData = rules.marbleChampStats()
        
        # create table per person's assignment data
        for i, frame in enumerate(self.stat_frames):
            data = Winrates.appData[i]
            for element in self.stats_data_labels[frame]:
                if not element == None:
                    element.destroy()
            self.stats_data_labels[frame] = []

            # Insert data into grid starting at row 2, since rows 0 and 1 are headers
            for row, (champ, winrate, matches) in enumerate(data, start=2):
                lbl1 = tk.Label(frame, text=champ, borderwidth=1, relief="solid", font=('Arial', 14))
                lbl1.grid(row=row, column=0, sticky="nsew")
                self.stats_data_labels[frame].append(lbl1)
                
                lbl3 = tk.Label(frame, text=winrate, borderwidth=1, relief="solid", font=('Arial', 14))
                lbl3.config(bg=colorWinrate(winrate))
                lbl3.grid(row=row, column=1, sticky="nsew")
                self.stats_data_labels[frame].append(lbl3)
                
                lbl4 = tk.Label(frame, text=matches, borderwidth=1, relief="solid", font=('Arial', 14))
                lbl4.config(bg=colorMatches(matches))
                lbl4.grid(row=row, column=2, sticky="nsew")
                self.stats_data_labels[frame].append(lbl4)
    
    @classmethod
    def check_constructor_called(cls):
        """Function to check if the constructor (__init__) has been called."""
        return cls.initialized