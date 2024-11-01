import tkinter as tk
from tkinter import ttk

import globals
import parseChampStats
import threading

# TODO:
# - sort by winrate and only include data with > 100 matches, statistic analysis for highlighting

# Tkinter App
class DataApp(tk.Tk):
    def __init__(self, data, headers): # assume same number of headers as data
        super().__init__()
        self.title("Data Table")
        self.geometry("1400x400")
        self.headers = headers
        self.create_table_grids(data)

    def create_table_grids(self, data_sets):
        for index, data in enumerate(data_sets):
            # Create a frame for each grid
            frame = tk.Frame(self, borderwidth=2, relief="solid")
            frame.grid(row=0, column=index, padx=5, pady=5, sticky="nsew")
            
            # Add a header label to the top of the frame
            header = tk.Label(frame, text=self.headers[index], font=("Arial", 12, "bold"))
            header.grid(row=0, column=0, columnspan=4, pady=10)  # Adjust columnspan based on the number of columns

            
            self.create_table(frame, data)

        # Make each frame expandable
        for col in range(len(data_sets)):
            self.grid_columnconfigure(col, weight=1)

    def create_table(self, frame, data):
        # Create header
        headers = ["Champion", "Role", "Winrate", "Matches"]
        for col, header in enumerate(headers):
            lbl = tk.Label(frame, text=header, font=('Arial', 10, 'bold'), borderwidth=1, relief="solid")
            lbl.grid(row=1, column=col, sticky="nsew")

        # Insert data into grid
        for row, (champ, role) in enumerate(data, start=2):
            
            # can display incomplete data in best-effort
            key = (champ, role)
            if(not key in parseChampStats.winrates):
                continue
            
            obj = parseChampStats.winrates[key]
            tk.Label(frame, text=champ, borderwidth=1, relief="solid").grid(row=row, column=0, sticky="nsew")
            tk.Label(frame, text=role, borderwidth=1, relief="solid").grid(row=row, column=1, sticky="nsew")
            tk.Label(frame, text=obj["winrate"], borderwidth=1, relief="solid").grid(row=row, column=2, sticky="nsew")
            tk.Label(frame, text=obj["matches"], borderwidth=1, relief="solid").grid(row=row, column=3, sticky="nsew")

        # Make the grid cells expand with the window
        for col in range(4):
            self.grid_columnconfigure(col, weight=1)
        for row in range(len(data) + 1):
            self.grid_rowconfigure(row, weight=1)

def init_app():
    parseChampStats.constructWinrates()

def run_app(search_list, summonerNames):
    app = DataApp(search_list, summonerNames)
    app.mainloop()


# threading to be non-blocking
def start_app(marbleData):
    appData = []
    for data in marbleData:
        keys = parseChampStats.getChamps(data[0], data[1])
        appData.append(keys)
        
    # Start the Tkinter app in a new thread
    app_thread = threading.Thread(target=run_app, args=(appData,globals.allSummoners,))
    app_thread.start()