import tkTools.tkUtil as tkUtil
import tkTools.tkAssignments as tkAssignments
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals
import backendTools.rules as rules
import backendTools.parseChampStats as parseChampStats

# CUR_ASSIGNMENT_X_OFFSET = 300
DEFAULT_MSG = "Homies, it's marblin time x2"


class PickingPage(tkAssignments.AssignmentsPage):
    def __init__(self, root):
        super().__init__(root, "Picking Page", DEFAULT_MSG)
        
        self.curAssignments = tk.Label(self.frame, text="Current assignments:", font=("Arial", 12))
        self.curAssignments.place(x=0, y=90.0, anchor="w")
        
        self.entry = tk.Entry(self.frame, width=30)
        self.entry.place(x=300, y=540.0, anchor="w")
        
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.submit)
        self.submit_button.place(x=500, y=540.0, anchor="w")
        # self.button_clicked = False
        self.button_pressed = tk.StringVar()
        self.entered_text = ""
        
        # self.reminderMsg = tk.Label(self.frame, text="Did you finish copying marbles output to data/marbles_output.txt?", font=("Arial", 12))
        # self.reminderMsg.place(x=tkUtil.WIDTH/2, y=400.0, anchor="center")
        
        self.top10gridframe = None
        
        self.top10Labels = []
        self.initTop10Marbles()
        self.prompt = tk.Label(self.top10gridframe, text="", font=("Arial", 12))
        self.prompt.grid(row=0, column=0, padx=5, pady=5, sticky="w") #.place(x=0, y=340.0, anchor="w")
        
        # Champ stats
        self.stat_frames = []
        self.stats_data_labels = {}
        self.stats_title_labels = []
        self.stats_col_title_labels = []
        self.create_table_grids()

    def initTop10Marbles(self):
        self.top10gridframe = tk.Frame(self.root)
        for i in range(1, 11):
            self.top10Labels.append(tk.Label(self.top10gridframe, text=str(i)+": "))
            self.top10Labels[-1].grid(row=i, column=0, padx=5, pady=5, sticky="w")

    def updateTop10Marbles(self):
        self.prompt.config(text="Pick a top 10 marble to swap with:")
        for i in range(10):
            self.top10Labels[i].config(text=str(i)+": "+rules.marbles[i].marbleDesc)
    
    def clearPrompts(self):
        # self.prompt.
        self.top10gridframe.place_forget()

    def updateAssignments(self, unpickedSummoners=globals.allSummoners):
        super().updateAssignments(unpickedSummoners)
        
        # champion winrate statistics
        keys = rules.marbleChampStats()
        appData = []
        for key in keys:
            keys = parseChampStats.getChamps(key[0], key[1])
            appData.append(keys)
        for i, frame in enumerate(self.stat_frames):
            self.create_table(frame, appData[i])
        

    def updateSummonerMarbles(self):
        # initial visualization of data
        self.updateAssignments()
        
        if rules.godScenario:
            self.setMessageLabel("Someone is God, further picking actions disallowed.")
            return
        
        self.unpickedSummoners = list(globals.summoners.keys())
        self.unpickedRoles = list(globals.ROLES)
        
        self.entered_text = ""
        self.button_clicked = False
        self.setMessageLabel("Enter a number 0-9")
        
        
        
        while True:
            self.submit_button.wait_variable(self.button_pressed)
            if(self.getNum09()):
                break
    
        rules.top1Swaper(int(self.entered_text))
        self.updateAssignments()
        
        # # assign marbles via marble level and picking
        # # note: top 1 doesn't pick first ONLY if paralyzed
        if(not rules.marbles[0].level == "0"):
            self.pick(rules.marbles[0].name, False)
        while(len(self.unpickedSummoners)>0):
            nextPickers, isParalyzed = rules.getNextPicker(self.unpickedSummoners)
            for picker in nextPickers:
                self.pick(picker, isParalyzed)
        
        self.setMessageLabel("All positions are assigned!")
        self.done = True
        self.next_button.config(state="active")
        self.clearPrompts()
        
    def pick(self, picker, isParalyzed):
        # check if current role assignment is ok, else get new marble
        rules.updateBestMarble(self.unpickedSummoners, self.unpickedRoles)
        
        # print("picker:"+picker) # TODO UI THIS
        # if paralyzed, print next 5 lvl1 marbles of that person with avail roles
        top5 = []
        if isParalyzed:
            top5 = rules.getTop5Marbles(picker, globals.summoners[picker].curMarble, self.unpickedRoles)
            
            # show top 5 marbles as prompt
            self.prompt.config(text="Paralyzed! Pick a marble 0-4")
            self.setMessageLabel(picker+" is paralyzed.")
            for i in range(10):
                if i < 5:
                    self.top10Labels[i].config(text=str(i)+":"+rules.marbles[top5[i]].marbleDesc)
                else:
                    self.top10Labels[i].config(text="")

            # input 0-4
            while True:
                self.submit_button.wait_variable(self.button_pressed)
                if(self.entered_text.isdigit() and int(self.entered_text) >= 0 and int(self.entered_text) < 5):
                    rules.setCurMarble(picker, top5[int(self.entered_text)])
                    break
        
        # input valid 
        pickedRole = ""
        if(len(self.unpickedRoles)==1):
            print("One role remaining. Forcibly assigning "+picker+" to "+self.unpickedRoles[0])
            rules.setRole(globals.summoners[picker].curMarble, self.unpickedRoles[0])
            pickedRole = self.unpickedRoles[0]
        
        if(rules.marbles[globals.summoners[picker].curMarble].position==""):
            # no role assigned yet, can pick own role, input role
            self.prompt.config(text="Remaining roles:")
            for i in range(10):
                if i < len(self.unpickedRoles):
                    self.top10Labels[i].config(text=self.unpickedRoles[i])
                else:
                    self.top10Labels[i].config(text="")
            pickedRole = self.getRole(picker)
            rules.setRole(globals.summoners[picker].curMarble, pickedRole)
        else:
            pickedRole = rules.marbles[globals.summoners[picker].curMarble].position
        
        print("picked role: "+pickedRole)
        rules.updatePickList(self.unpickedSummoners, picker, self.unpickedRoles, pickedRole)
        # print("REMAINING ROLES:")
        # print(self.unpickedRoles)
        
        # update display with new assignments
        self.updateAssignments(self.unpickedSummoners)
        # rules.currentMarbleAssignments(self.unpickedSummoners)
    
    def getRole(self, picker):
        self.setMessageLabel("Pick a role "+picker)
        while True:
            self.submit_button.wait_variable(self.button_pressed)
            if(self.entered_text.lower() in self.unpickedRoles):
                return self.entered_text
    
    def getNum09(self): # TODO rename this to validate
        self.button_clicked = False
        if self.entered_text.isdigit() and int(self.entered_text) >= 0 and int(self.entered_text) <= 9:
            if rules.marbles[int(self.entered_text)].level != "MARBLE GOD":
                self.setMessageLabel(DEFAULT_MSG)
                return True
            self.setMessageLabel("Cannot swap with God!")
        self.setMessageLabel("Enter a number 0-9")
        self.animate_message(self.message_label)
        return False
    
    def submit(self):
        self.button_pressed.set("button pressed")
        self.entered_text = self.entry.get()  # Get the text from the entry box
        # print("Read input:", self.entered_text)
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
    
    # =================== CONTROL ==========================
    
    def hide(self):
        super().hide()
        self.frame.place_forget()
        self.top10gridframe.place_forget()
        self.hide_stat_frames()
        
        
    
    def show(self):
        self.top10gridframe.place(x=0, y=350.0)
        # self.prompt.place(x=0, y=340.0, anchor="w")
        self.done = False
        self.next_button.config(state="disabled")
        
        # run main assignments program
        rules.readMarbles()
        rules.initGetBestMarbles()
        super().show() # need to initialize marble data before showing assignments
        
        self.updateTop10Marbles()
        self.show_stat_frames()
        self.updateSummonerMarbles() # main picking
        

def createPickingPage(root):
    return PickingPage(root)