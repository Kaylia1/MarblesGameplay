import tkinter as tk
import tkTools.tkUtil as tkUtil
import backendTools.rules as rules
import backendTools.globals as globals
import backendTools.wheelMap as wheelMap

import tkTools.tkWheelPage as tkWheelPage # import wheel_result

class WheelResultPage(tkUtil.Page):
    def __init__(self, root):
        super().__init__(root, "Wheel Result Page", "")
        
        self.curAssignments = tk.Label(self.frame, text="Current assignments:", font=("Arial", 12))
        self.curAssignments.place(x=0, y=90.0, anchor="w")
        
        self.gridframe = None # assignments grid
        
        self.headers = []
        self.assignmentHeadLabels = []
        self.assignmentLabels = {}
        
        # points.load_state() # TODO should we be able to dynamically load at runtime?
        self.initSummonerMarbles()
        
        # entries for widgets
        # self.entries = {}
        # self.labels = {}
        # self.poss = {}
        self.submit_button = None
        self.label_names = ['a', 'b']
        self.inputs = {} # contains entry, label, poss
        
        # labels for widgets
        for label_name in self.label_names:
            self.inputs[label_name] = {}
            self.inputs[label_name]["label"] = tk.Label(self.frame, text="Input "+label_name+":")
            self.inputs[label_name]["label"].pack()
            self.inputs[label_name]["entry"] = tk.Entry(self.frame)  # Store entry widget for 'a'
            self.inputs[label_name]["entry"].pack()
            
            self.inputs[label_name]["poss"] = []
            self.inputs[label_name]["val"] = ""
        self.init_submit_button()
        
        
    def initSummonerMarbles(self):
        self.gridframe = tk.Frame(self.root)
        self.headers = ["Name", "Position", "Letter", "Level"]
        for col, header in enumerate(self.headers):
            self.assignmentHeadLabels.append(tk.Label(self.gridframe, text=header, font=("Arial", 10, "bold"), anchor="w").grid(row=0, column=col, padx=5, pady=5, sticky="w"))

        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            # Display each attribute of the Summoner object in a new column
            self.assignmentLabels[key] = {}
            self.assignmentLabels[key][self.headers[0]] = tk.Label(self.gridframe, text=key)
            self.assignmentLabels[key][self.headers[0]].grid(row=row, column=0, padx=5, pady=5)
            
            self.assignmentLabels[key][self.headers[1]] = tk.Label(self.gridframe, text="")
            self.assignmentLabels[key][self.headers[1]].grid(row=row, column=1, padx=5, pady=5)
            
            self.assignmentLabels[key][self.headers[2]] = tk.Label(self.gridframe, text="")
            self.assignmentLabels[key][self.headers[2]].grid(row=row, column=2, padx=5, pady=5)

            self.assignmentLabels[key][self.headers[3]] = tk.Label(self.gridframe, text="")
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

    def show(self):
        super().show()
        self.gridframe.place(x=0, y=200.0, anchor="w")
        self.updateAssignments()
        self.gen_from_inputs()
        self.setMessageLabel(tkWheelPage.wheel_result)
        self.next_button.config(state="disabled")
    
    def hide(self):
        super().hide()
        self.frame.place_forget()
        self.gridframe.place_forget()
    
    
    def get_possible_input(self, code): # TODO this should be a map tbh
        if code == "letter":
            return [
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
                ]
        elif code == "summoner":
            return globals.allSummoners # TODO victim checking
        elif code == "summonerLvl1":
            return rules.getLvl1s() # note these values CAN BE LEN 1
        elif code == "summonerLetter":
            return rules.getHasLetters()
        elif code == "summonerNoLetter":
            return rules.getNoLetters()
        elif code == "role+":
            # role if currently a level 1 marble, otherwise NOTHING # TODO TEST THIS JANK THING
            if(rules.marbles[globals.summoners[wheelMap.lastSpinner].curMarble].level == "1"):
                return globals.ROLES
            return []
        elif code == "role":
            return globals.ROLES
        else:
            return []
    
    def gen_from_inputs(self):
        self.updateAssignments()
        
        # get possibilities and auto select if only one option
        # NOTE: assume wheel_map_inputs always returns a tuple with exact same number of values as label_names
        for i, label_name in enumerate(self.label_names):
            key_str = wheelMap.wheel_map_inputs[tkWheelPage.wheel_result][i]
            self.inputs[label_name]["poss"] = self.get_possible_input(key_str)
            poss_inputs_str = ", ".join(self.inputs[label_name]["poss"])
            print(poss_inputs_str)
            self.inputs[label_name]["label"].config(text=key_str + " Possible inputs: "+ poss_inputs_str)
            self.inputs[label_name]["val"] = ""
            if len(self.inputs[label_name]["poss"]) == 1:
                print("autofilling")
                self.inputs[label_name]["val"] = self.inputs[label_name]["poss"][0]
        self.create_gui()

    def create_gui(self):
        # Show a text box for `a` if `a_options` is not empty
        for label_name in self.label_names:
            options = self.inputs[label_name]["poss"]
            if options and len(options) > 1:
                self.inputs[label_name]["label"].pack()
                self.inputs[label_name]["entry"].pack()
            else:
                self.inputs[label_name]["label"].pack_forget()
                self.inputs[label_name]["entry"].pack_forget()
        self.submit_button.config(state="active")

    def init_submit_button(self):
        # internal function to handle submit button click
        def on_submit():
            # Print the values and validate them
            
            totalOk = True
            for label_name in self.label_names:
                read_input = self.inputs[label_name]["entry"].get()
                print(label_name+":"+read_input)
                
                # only validate inputs with text boxes
                if len(self.inputs[label_name]["poss"]) > 1:
                    self.inputs[label_name]["val"] = read_input
                    ok = False
                    loweredVal = self.inputs[label_name]["val"].lower()
                    for possVal in self.inputs[label_name]["poss"]:
                        if(loweredVal == possVal.lower()):
                            ok = True
                            break
                    if not ok:
                        totalOk = False
                        print("BAD INPUT probably")
                        break
            
            if totalOk:
                self.submit_button.config(state="disabled") # prevent excess submissions for a bit(?)
                self.next_button.config(state="active")
                # TODO wheel map call
                # construct params
                if not rules.godScenario:
                    wheel_params = []
                    for label_name in self.label_names:
                        wheel_params.append(self.inputs[label_name]["val"])
                    wheelMap.wheel_map[tkWheelPage.wheel_result](wheel_params)
                
                # once valid input, go next immediately
                self.handleNext()

            # if inputs not ok then don't do anything
            

        # Submit button
        self.submit_button = tk.Button(self.frame, text="Submit", command=on_submit)
        self.submit_button.pack()
        
    def handleNext(self):
        tkUtil.show_page(2)


def createWheelResultPage(root):
    wheelpage = WheelResultPage(root)
    return wheelpage


# Example arrays of possible strings
# a_options = ["Option 1", "Option 2"]
# b_options = ["a", "b", "c", "d"]  # Empty, so no entry will be created for b

# # Run the GUI with example inputs
# create_gui(a_options, b_options)
