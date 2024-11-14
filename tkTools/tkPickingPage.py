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
        self.state_queue = []
        self.state = "done"
        self.pickState = "pickInit"
        
        self.curAssignments = tk.Label(self.frame, text="Current assignments:", font=("Arial", 12))
        self.curAssignments.place(x=0, y=90.0, anchor="w")
        
        self.entry = tk.Entry(self.frame, width=30)
        self.entry.place(x=300, y=540.0, anchor="w")
        
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.submit)
        self.submit_button.place(x=500, y=540.0, anchor="w")
        # self.button_clicked = False
        self.button_pressed = tk.BooleanVar()
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
        

    # state starts off as "show"
    def updateSummonerMarbles(self):
        state_info = self.state_queue[0]
        self.state = state_info[0]

        if self.state != "done":
            self.frame.after(100, self.updateSummonerMarbles)
        
        # let pick and done be "stuck" states
        if self.state != "pick" and self.state != "done":
            self.state_queue.pop(0)
        
        if self.state == "show":
            # initial visualization of data
            self.updateAssignments()
            
            if rules.godScenario:
                self.setMessageLabel("Someone is God, further picking actions disallowed.")
                self.state_queue.append(["done"])
                return
            
            self.unpickedSummoners = list(globals.summoners.keys())
            self.unpickedRoles = list(globals.ROLES)
            
            self.entered_text = ""
            self.button_clicked = False
            self.setMessageLabel("Enter a number 0-9")
            
            self.state_queue.append(["top10swap"])
        elif self.state == "top10swap":
            if self.checkSubmitted() and self.getNum09():
                rules.top1Swaper(int(self.entered_text))
                self.state_queue.append(["paralyzedFirstCheck"])
            else: 
                self.state_queue.append(["top10swap"])
        elif self.state == "paralyzedFirstCheck": # maybe set state for each picker?
            # # assign marbles via marble level and picking
            # # note: top 1 doesn't pick first ONLY if paralyzed
            if(not rules.marbles[0].level == "0"):
                self.state_queue.append(["pick", rules.marbles[0].name, False])
                self.pickState = "pickInit"
            self.state_queue.append(["mainPicking"])
        elif self.state == "mainPicking":
            if (len(self.unpickedSummoners)>0):
                nextPickers, isParalyzed = rules.getNextPicker(self.unpickedSummoners)
                for picker in nextPickers:
                    self.state_queue.append(["pick", picker, isParalyzed]) # note, this appends multiple pick main calls, need a way to pick picker and paralyzed in queue
                    self.pickState = "pickInit"
                # recheck number of unpicked summoners after going through a nextpickers round
                self.state_queue.append(["mainPicking"])
            else:
                # no more pickers, finish
                self.state_queue.append(["done"])
        elif self.state == "done":
            self.setMessageLabel("All positions are assigned!")
            self.done = True
            self.next_button.config(state="active")
            self.clearPrompts()
        
        # run once for each pick
        elif self.state == "pick":
            # Todo error check
            picker = state_info[1]
            isParalyzed = state_info[2]
            
            # initial check for if it is paralyzed
            if self.pickState == "pickInit":
                rules.updateBestMarble(self.unpickedSummoners, self.unpickedRoles)
                
                if isParalyzed:
                    self.pickState = "paralyzedInit"
                else:
                    self.pickState = "pickRoleInit"
            # start picking once paralysis is no longer a factor
            elif self.pickState == "pickRoleInit":
                # input is valid 
                self.pickedRole = ""
                if(len(self.unpickedRoles)==1):
                    print("One role remaining. Forcibly assigning "+picker+" to "+self.unpickedRoles[0])
                    rules.setRole(globals.summoners[picker].curMarble, self.unpickedRoles[0])
                    self.pickedRole = self.unpickedRoles[0]
                
                if(rules.marbles[globals.summoners[picker].curMarble].position==""):
                    # no role assigned yet, can pick own role, input role
                    self.prompt.config(text="Remaining roles:")
                    for i in range(10):
                        if i < len(self.unpickedRoles):
                            self.top10Labels[i].config(text=self.unpickedRoles[i])
                        else:
                            self.top10Labels[i].config(text="")
                    self.pickState = "pickRoleUpdate"
                else:
                    self.pickedRole = rules.marbles[globals.summoners[picker].curMarble].position
                    self.pickState = "pickRoleFin"
            # wait for role input
            elif self.pickState == "pickRoleUpdate":
                if self.checkSubmitted() and self.entered_text.lower() in self.unpickedRoles:
                    self.pickedRole = self.entered_text.lower()
                    rules.setRole(globals.summoners[picker].curMarble, self.pickedRole)
                    self.pickState = "pickRoleFin"
            # finished picking, exit the picking substate machine
            elif self.pickState == "pickRoleFin":
                    print("picked role: "+self.pickedRole)
                    rules.updatePickList(self.unpickedSummoners, picker, self.unpickedRoles, self.pickedRole)
                    self.updateAssignments(self.unpickedSummoners)
                    self.pickState = "pickInit" # reset in case another pick call afterwards
                    self.state_queue.pop(0) # exit the picking substate machine
    
            # paralyzed, show top 5 marbles prompt
            elif self.pickState == "paralyzedInit":
                self.top5 = rules.getTop5Marbles(picker, globals.summoners[picker].curMarble, self.unpickedRoles)
                self.prompt.config(text="Paralyzed! Pick a marble 0-4")
                self.setMessageLabel(picker+" is paralyzed.")
                for i in range(10):
                    if i < 5:
                        self.top10Labels[i].config(text=str(i)+":"+rules.marbles[self.top5[i]].marbleDesc)
                    else:
                        self.top10Labels[i].config(text="")
                self.pickState = "paralyzedUpdate"
            # paralyzed, wait for 0-4 input
            elif self.pickState == "paralyzedUpdate":
                if self.checkSubmitted() and self.entered_text.isdigit() and int(self.entered_text) >= 0 and int(self.entered_text) < 5:
                    rules.setCurMarble(picker, self.top5[int(self.entered_text)])
                    self.pickState = "pickRoleInit"
    
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
        self.button_pressed.set(True)
        self.entered_text = self.entry.get()  # Get the text from the entry box
        # print("Read input:", self.entered_text)
        self.entry.delete(0, tk.END)
    
    def checkSubmitted(self):
        val = self.button_pressed.get()
        self.button_pressed.set(False)
        return val
        
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
        self.state_queue = [["done"]]
        self.frame.place_forget()
        self.top10gridframe.place_forget()
        self.hide_stat_frames()
        
        
    
    def show(self):
        self.state_queue = [["show"]]
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