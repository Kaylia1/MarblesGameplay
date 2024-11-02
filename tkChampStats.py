import tkinter as tk
from tkinter import ttk

import globals
import parseChampStats
import threading

# TODO:
# - sort by winrate and only include data with > 100 matches, statistic analysis for highlighting

dataApp = None

# Tkinter App
class DataApp(tk.Tk):
    def __init__(self, data, headers): # assume same number of headers as data
        super().__init__()
        self.title("Data Table")
        self.geometry("1400x400")
        self.headers = headers
        self.frames = []
        self.elements = []
        
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        self.create_table_grids(data)

    def create_table_grids(self, data_sets):
        for index, data in enumerate(data_sets):
            # Create a frame for each grid
            frame = tk.Frame(self, borderwidth=2, relief="solid")
            frame.grid(row=0, column=index, padx=5, pady=5, sticky="nsew")
            self.frames.append(frame)
            
            # Add a header label to the top of the frame
            header = tk.Label(frame, text=self.headers[index], font=("Arial", 12, "bold"))
            header.grid(row=0, column=0, columnspan=4, pady=10)  # Adjust columnspan based on the number of columns

            
            self.create_table(frame, data)

        # Make each frame expandable
        for col in range(len(data_sets)):
            self.grid_columnconfigure(col, weight=1)

    def create_table(self, frame, data):
        
        for element in self.elements:
            if not element == None:
                element.destroy()
        self.elements = []
        
        # Create header
        headers = ["Champion", "Role", "Winrate", "Matches"]
        for col, header in enumerate(headers):
            lbl = tk.Label(frame, text=header, font=('Arial', 10, 'bold'), borderwidth=1, relief="solid")
            lbl.grid(row=1, column=col, sticky="nsew")
            # self.elements.append(lbl)

        # Insert data into grid
        for row, (champ, role) in enumerate(data, start=2):
            
            # can display incomplete data in best-effort
            key = (champ, role)
            if(not key in parseChampStats.winrates):
                continue
            
            obj = parseChampStats.winrates[key]
            lbl1 = tk.Label(frame, text=champ, borderwidth=1, relief="solid")
            lbl1.grid(row=row, column=0, sticky="nsew")
            # self.elements.append(lbl1)
            
            lbl2 = tk.Label(frame, text=role, borderwidth=1, relief="solid")
            lbl2.grid(row=row, column=1, sticky="nsew")
            # self.elements.append(lbl2)
            
            lbl3 = tk.Label(frame, text=obj["winrate"], borderwidth=1, relief="solid")
            lbl3.grid(row=row, column=2, sticky="nsew")
            # self.elements.append(lbl3)
            
            lbl4 = tk.Label(frame, text=obj["matches"], borderwidth=1, relief="solid")
            lbl4.grid(row=row, column=3, sticky="nsew")
            # self.elements.append(lbl4)

        # Make the grid cells expand with the window
        for col in range(4):
            self.grid_columnconfigure(col, weight=1)
        for row in range(len(data) + 1):
            self.grid_rowconfigure(row, weight=1)
    
    def update_data(self, new_data_list):
        # don't need to update headers
        """Update frames with new data without recreating the window."""
        for i, frame in enumerate(self.frames):
            self.create_table(frame, new_data_list[i])  # Update data in each frame

    def hide_window(self):
        """Hide the window instead of closing it."""
        self.withdraw()

    def show_window(self, new_data):
        """Show window again and update data."""
        self.after(0, self.update_data, new_data)
        self.deiconify()

def init_app():
    parseChampStats.constructWinrates()

def run_app(search_list, summonerNames):
    global dataApp
    dataApp = DataApp(search_list, summonerNames)
    dataApp.mainloop()


# threading to be non-blocking
def start_app(marbleData):
    appData = []
    for data in marbleData:
        keys = parseChampStats.getChamps(data[0], data[1])
        appData.append(keys)
        
    # Start the Tkinter app in a new thread
    app_thread = threading.Thread(target=run_app, args=(appData,globals.allSummoners,))
    app_thread.start()

def update_app(marbleData):
    if(dataApp == None):
        start_app(marbleData)
    
    # import time
    # time.sleep(0.1)
    else:
        appData = []
        for data in marbleData:
            keys = parseChampStats.getChamps(data[0], data[1])
            appData.append(keys)
        dataApp.show_window(appData)
        
    