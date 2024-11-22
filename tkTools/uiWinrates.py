import tkTools.tkUtil as tkUtil
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals
import backendTools.rules as rules
import backendTools.parseChampStats as parseChampStats

class Winrates():
    def __init__(self, root):
        self.root = root
        
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
    
    def initWinrateGrid(self):
        for index in range(5):
            # Create a frame for each summoner's stat grid
            frame = tk.Frame(self.root, borderwidth=2, relief="solid")
            # frame.grid(row=0, column=index, padx=5, pady=5, sticky="nsew")
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
        # read champ stats
        keys = rules.marbleChampStats()
        appData = []
        for key in keys:
            keys = parseChampStats.getChamps(key[0], key[1])
            appData.append(keys)
        
        # create table per person's assignment data
        for i, frame in enumerate(self.stat_frames):
            data = appData[i]
            for element in self.stats_data_labels[frame]:
                if not element == None:
                    element.destroy()
            self.stats_data_labels[frame] = []

            # Insert data into grid
            for row, (champ, role) in enumerate(data, start=2):
                
                # can display incomplete data in best-effort
                key = (champ, role)
                if(not key in parseChampStats.winrates):
                    continue
                
                obj = parseChampStats.winrates[key]
                lbl1 = tk.Label(frame, text=champ, borderwidth=1, relief="solid", font=('Arial', 14))
                lbl1.grid(row=row, column=0, sticky="nsew")
                self.stats_data_labels[frame].append(lbl1)
                
                # lbl2 = tk.Label(frame, text=role, borderwidth=1, relief="solid")
                # lbl2.grid(row=row, column=1, sticky="nsew")
                # self.stats_data_labels[frame].append(lbl2)
                
                lbl3 = tk.Label(frame, text=obj["winrate"], borderwidth=1, relief="solid", font=('Arial', 14))
                lbl3.grid(row=row, column=1, sticky="nsew")
                self.stats_data_labels[frame].append(lbl3)
                
                lbl4 = tk.Label(frame, text=obj["matches"], borderwidth=1, relief="solid", font=('Arial', 14))
                lbl4.grid(row=row, column=2, sticky="nsew")
                self.stats_data_labels[frame].append(lbl4)