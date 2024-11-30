import tkinter as tk
import uiTools.uiPage as uiPage
import backendTools.rules as rules
import backendTools.globals as globals
import backendTools.wheelMap as wheelMap
import uiTools.uiWheelPage as uiWheelPage # import wheel_result
import uiTools.uiMoney as uiMoney
import uiTools.uiAssignments as uiAssignments

class WheelResultPage(uiPage.Page):
    def __init__(self, root):
        super().__init__(root, "Wheel Result Page", "")
        
        self.submit_button = None
        self.label_names = ['a', 'b']
        self.inputs = {} # contains entry, label, poss
        
        # labels for widgets
        for label_name in self.label_names:
            self.inputs[label_name] = {}
            self.inputs[label_name]["label"] = tk.Label(self.frame, text="Input "+label_name+":")
            # self.inputs[label_name]["label"].pack()
            self.inputs[label_name]["entry"] = tk.Entry(self.frame)  # Store entry widget for 'a'
            # self.inputs[label_name]["entry"].pack()
            
            self.inputs[label_name]["poss"] = []
            self.inputs[label_name]["val"] = ""
        self.init_submit_button()
        
        self.moneyDisplay = uiMoney.Money(self.frame)
        self.assignmentsDisplay = uiAssignments.Assignments(self.frame)

    def show(self):
        super().show()
        self.gen_from_inputs()
        self.setMessageLabel(uiWheelPage.wheel_result)
        self.setNextButtonState(False)
        
        self.moneyDisplay.updateMoneyLabels()
        self.moneyDisplay.show()
        self.assignmentsDisplay.updateAssignmentLabels()
        self.assignmentsDisplay.show()
    
    # don't need to implement this since we are using the parent's frame
    def hide(self):
        super().hide()
        self.moneyDisplay.hide()
        self.assignmentsDisplay.hide()
    
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
        # get possibilities and auto select if only one option
        # NOTE: assume wheel_map_inputs always returns a tuple with exact same number of values as label_names
        for i, label_name in enumerate(self.label_names):
            key_str = wheelMap.wheel_map_inputs[uiWheelPage.wheel_result][i]
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
        for i, label_name in enumerate(self.label_names):
            options = self.inputs[label_name]["poss"]
            if options and len(options) > 1:
                self.inputs[label_name]["label"].place(x=550, y=250+100*i)
                self.inputs[label_name]["entry"].place(x=550, y=280+100*i)
            else:
                self.inputs[label_name]["label"].place_forget()
                self.inputs[label_name]["entry"].place_forget()
                self.inputs[label_name]["entry"].delete(0, tk.END)
                self.on_submit()
        self.submit_button.config(state="active")

    def init_submit_button(self):
        # Submit button
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.on_submit)
        self.submit_button.place(x=550, y=500)
        
    # internal function to handle submit button click
    def on_submit(self):
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
            self.setNextButtonState(True)
            # TODO wheel map call
            # construct params
            if not rules.godScenario:
                wheel_params = []
                for label_name in self.label_names:
                    wheel_params.append(self.inputs[label_name]["val"])
                wheelMap.wheel_map[uiWheelPage.wheel_result](wheel_params)
            
            # once valid input, go next immediately
            self.handleNext()
        
    def handleNext(self):
        uiPage.show_page(2)


def createWheelResultPage(root):
    wheelpage = WheelResultPage(root)
    return wheelpage