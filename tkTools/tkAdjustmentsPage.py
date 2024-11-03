import tkTools.tkUtil as tkUtil
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals
import backendTools.rules as rules
import backendTools.parseChampStats as parseChampStats
import tkTools.tkPickingPage as tkPickingPage

# is this actually less efficient since it is creating a whole new class that also has stat data?

import backendTools.wheelMap as wheelMap
import tkTools.tkUtil as tkUtil
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals
import backendTools.rules as rules
import backendTools.parseChampStats as parseChampStats

class AdjustmentsPage(tkUtil.Page):
    def __init__(self, root):
        super().__init__(root, "Wheel / Bribe Page", "huh")
        
        self.curAssignments = tk.Label(self.frame, text="Current assignments:", font=("Arial", 12))
        self.curAssignments.place(x=0, y=90.0, anchor="w")
        
        self.entry = tk.Entry(self.frame, width=30)
        self.entry.place(x=300, y=540.0, anchor="w")
        
        self.submit_button = tk.Button(self.frame, text="Spin!", command=self.submit)
        self.submit_button.place(x=500, y=540.0, anchor="w")
        self.button_pressed = tk.StringVar()
        self.entered_text = ""
        
        self.gridframe = None # assignments grid
        self.moneyFrame = None
        
        self.headers = []
        self.assignmentHeadLabels = []
        self.assignmentLabels = {}
        
        # points.load_state() # TODO should we be able to dynamically load at runtime?
        self.initSummonerMarbles()
        
        # Champ stats
        self.stat_frames = []
        self.stats_data_labels = {}
        self.stats_title_labels = []
        self.stats_col_title_labels = []
        self.create_table_grids()
        
        # Money
        self.moneyLabels = []
        self.initSummonerMoney()
        
        # bribery
        self.initBribery()
    
    def initSummonerMarbles(self):
        self.gridframe = tk.Frame(self.root)
        # self.gridframe.place(x=0, y=200.0, anchor="w")
        
        self.headers = ["Name", "Position", "Letter", "Level"]
        for col, header in enumerate(self.headers):
            self.assignmentHeadLabels.append(tk.Label(self.gridframe, text=header, font=("Arial", 10, "bold"), anchor="w").grid(row=0, column=col, padx=5, pady=5, sticky="w"))

        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            # Display each attribute of the Summoner object in a new column
            self.assignmentLabels[key] = {}
            self.assignmentLabels[key][self.headers[0]] = tk.Label(self.gridframe, text=key)
            self.assignmentLabels[key][self.headers[0]].grid(row=row, column=0, padx=5, pady=5)
            
            self.assignmentLabels[key][self.headers[1]] = tk.Label(self.gridframe, text=rules.marbles[summoner.curMarble].position)
            self.assignmentLabels[key][self.headers[1]].grid(row=row, column=1, padx=5, pady=5)
            
            self.assignmentLabels[key][self.headers[2]] = tk.Label(self.gridframe, text=rules.marbles[summoner.curMarble].letter)
            self.assignmentLabels[key][self.headers[2]].grid(row=row, column=2, padx=5, pady=5)

            self.assignmentLabels[key][self.headers[3]] = tk.Label(self.gridframe, text=rules.marbles[summoner.curMarble].level)
            self.assignmentLabels[key][self.headers[3]].grid(row=row, column=3, padx=5, pady=5)

    def updateAssignments(self, unpickedSummoners=globals.allSummoners):
        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            # Update each attribute of the Summoner object
            bgd = "SystemButtonFace"
            if not key in unpickedSummoners:
                bgd = "#90EE90"
            self.assignmentLabels[key][self.headers[0]].config(bg=bgd)
            self.assignmentLabels[key][self.headers[1]].config(text=rules.marbles[summoner.curMarble].position, bg=bgd)
            self.assignmentLabels[key][self.headers[2]].config(text=rules.marbles[summoner.curMarble].letter, bg=bgd)
            self.assignmentLabels[key][self.headers[3]].config(text=rules.marbles[summoner.curMarble].level, bg=bgd)
        
        keys = rules.marbleChampStats()
        appData = []
        for key in keys:
            keys = parseChampStats.getChamps(key[0], key[1])
            appData.append(keys)
        for i, frame in enumerate(self.stat_frames):
            self.create_table(frame, appData[i])
    
    def submit(self):
        self.button_pressed.set("button pressed")
        # print("SPINNING WHEEL???")
        self.entered_text = self.entry.get()  # Get the text from the entry box
        # print("Read input:", self.entered_text)
        for summonerName in globals.allSummoners:
            if(self.entered_text.lower() == summonerName.lower() and globals.summoners[(self.entered_text[0].upper() + self.entered_text[1:].lower())].money >= 100):
                wheelMap.lastSpinner = self.entered_text[0].upper() + self.entered_text[1:].lower() # TODO bad coding practice to manually make first letter uppercase
                globals.summoners[wheelMap.lastSpinner].money -= 100
                tkUtil.trigger_wheel_page()
                break
        self.entry.delete(0, tk.END)
        
        
        
    # =================== STATISTICS ==========================
    
    def show_stat_frames(self):
        for i, frame in enumerate(self.stat_frames):
            frame.place(x=320+210*i, y=100)
            
    def hide_stat_frames(self):
        for frame in self.stat_frames:
            frame.place_forget()
    
    def create_table_grids(self):
        for index in range(5):
            # Create a frame for each summoner's stat grid
            frame = tk.Frame(self.root, borderwidth=2, relief="solid")
            # frame.grid(row=0, column=index, padx=5, pady=5, sticky="nsew")
            self.stat_frames.append(frame)
            self.stats_data_labels[frame] = []
            
            # Add a header label to the top of the frame
            self.stats_title_labels.append(tk.Label(frame, text=globals.allSummoners[index], font=("Arial", 12, "bold")))
            self.stats_title_labels[-1].grid(row=0, column=0, columnspan=4, pady=10)  # Adjust columnspan based on the number of columns
            
            # Create header
            headers = ["Champion", "Role", "Winrate", "Matches"]
            for col, header in enumerate(headers):
                self.stats_col_title_labels.append(tk.Label(frame, text=header, font=('Arial', 10, 'bold'), borderwidth=1, relief="solid"))
                self.stats_col_title_labels[-1].grid(row=1, column=col, sticky="nsew")

    def create_table(self, frame, data):
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
            lbl1 = tk.Label(frame, text=champ, borderwidth=1, relief="solid")
            lbl1.grid(row=row, column=0, sticky="nsew")
            self.stats_data_labels[frame].append(lbl1)
            
            lbl2 = tk.Label(frame, text=role, borderwidth=1, relief="solid")
            lbl2.grid(row=row, column=1, sticky="nsew")
            self.stats_data_labels[frame].append(lbl2)
            
            lbl3 = tk.Label(frame, text=obj["winrate"], borderwidth=1, relief="solid")
            lbl3.grid(row=row, column=2, sticky="nsew")
            self.stats_data_labels[frame].append(lbl3)
            
            lbl4 = tk.Label(frame, text=obj["matches"], borderwidth=1, relief="solid")
            lbl4.grid(row=row, column=3, sticky="nsew")
            self.stats_data_labels[frame].append(lbl4)
    
    # =================== MONEY ============================
    
    def initSummonerMoney(self):
        self.moneyFrame = tk.Frame(self.root)
        
        headers = ["Name", "Money"]
        for col, header in enumerate(headers):
            self.moneyLabels.append(tk.Label(self.moneyFrame, text=header, font=("Arial", 10, "bold"), anchor="w"))
            self.moneyLabels[-1].grid(row=0, column=col, padx=5, pady=5, sticky="w")

        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            # key is summoner name
            # Display each attribute of the Summoner object in a new column
            self.moneyLabels.append(tk.Label(self.moneyFrame, text=key))
            self.moneyLabels[-1].grid(row=row, column=0, padx=5, pady=5)
            self.moneyLabels.append(tk.Label(self.moneyFrame, text="$"+str(summoner.money)))
            self.moneyLabels[-1].grid(row=row, column=1, padx=5, pady=5)
    
    def updateSummonerMoney(self):
        name = ""
        for i in range(2, len(self.moneyLabels)):
            if(i%2==0):
                name = tkUtil.getLabelTxt(self.moneyLabels[i])
            else:
                self.moneyLabels[i].config(text="$"+str(globals.summoners[name].money))
    
    # =================== BRIBE BUTTON ==========================
    def initBribery(self):
        # List of valid inputs
        # valid_inputs = globals.allSummoners  # Replace with your valid inputs
        self.bribeFrame = tk.Frame(self.root)

        self.bribePrompt = tk.Label(self.bribeFrame, text="Bribery\n from, to, amount")
        self.bribePrompt.pack(pady=5)

        # Create text entry boxes
        self.name1 = tk.Entry(self.bribeFrame)
        self.name1.pack(pady=5)

        self.name2 = tk.Entry(self.bribeFrame)
        self.name2.pack(pady=5)

        self.money = tk.Entry(self.bribeFrame)
        self.money.pack(pady=5)
        
        # Create submit button
        self.bribe_button = tk.Button(self.bribeFrame, text="Bribe", command=self.submit_inputs)
        self.bribe_button.pack(pady=20)
    
    # TODO NEED TO RENAME THESE
    def submit_inputs(self):
        lowercase_summoners = [summoner.lower() for summoner in globals.allSummoners]  # Convert all to lowercase

        input1 = self.name1.get().strip().lower()  # Get input and convert to lowercase
        input2 = self.name2.get().strip().lower()  # Get input and convert to lowercase
        input3 = self.money.get().strip()  # Get the third input without changing case for number check

        self.name1.delete(0, tk.END)
        self.name2.delete(0, tk.END)
        self.money.delete(0, tk.END)

        if input1 in lowercase_summoners and input2 in lowercase_summoners:
            if input3.isdigit() and int(input3) >= 0 and globals.summoners[input1[0].upper() + input1[1:].lower()].money>=int(input3):
                print(f"Inputs are valid: {input1}, {input2}, {input3}")
                # self.bribe_button.config(state=tk.DISABLED)  # Disable the submit button
                
                globals.summoners[input1[0].upper() + input1[1:].lower()].money -= int(input3)
                globals.summoners[input2[0].upper() + input2[1:].lower()].money += int(input3)
                self.message_label.config(text="Bribery accepted")
                self.updateSummonerMoney()
            else:
                self.message_label.config(text="The third input must be a non-negative number.")
        else:
            self.message_label.config(text="The first two inputs must summoner names.")
    
    # =================== CONTROL ==========================
    
    def hide(self):
        super().hide()
        self.frame.place_forget()
        self.gridframe.place_forget()
        self.moneyFrame.place_forget()
        self.bribeFrame.place_forget()
        self.hide_stat_frames()
        
    def show(self):
        super().show()
        self.gridframe.place(x=0, y=200.0, anchor="w")
        self.moneyFrame.place(x=0, y=600.0, anchor="w")
        self.bribeFrame.place(x=800, y=600.0, anchor="w")
        
        self.updateSummonerMoney()
        
        # run main assignments program
        self.updateAssignments() # get data that pickingpage set
        self.show_stat_frames()

def createAdjustmentsPage(root):
    return AdjustmentsPage(root)