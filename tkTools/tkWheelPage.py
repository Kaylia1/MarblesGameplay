import tkTools.tkUtil as tkUtil
import random
import tkinter as tk
import time
import math
import backendTools.wheelMap as wheelMap
import backendTools.soundTools as soundTools

# wheel page is responsible for making marble adjustments due to wheel
wheel_result = ""

class WheelPage(tkUtil.Page):

    def __init__(self, root):
        super().__init__(root, "Wheel of fortune", "")
        self.label1.lower()
        
        self.options = readWheelOptions()
        self.num_options = len(self.options)
        self.angle_per_option = 360 / self.num_options
        self.selected_option = tk.StringVar()
        self.selected_option.set("Click to Spin")
        
        # Canvas for the wheel
        self.canvas = tk.Canvas(self.frame, width=600, height=600)
        
        # Label to display the selected option
        self.label = tk.Label(self.frame, textvariable=self.selected_option, font=("Times", 18))
        
        # Button to spin the wheel
        self.spin_button = tk.Button(self.frame, text="Spin the Wheel", command=self.spin_wheel, font=("Times", 18))

        self.draw_wheel()  # Initial drawing of the wheel
        self.draw_pointer()  # Draw the fixed 
        self.wheelResult = ""
        global wheel_result
        wheel_result = ""
    

    def draw_wheel(self, offset_angle=0, highlight_index=None):
        """Draws the wheel with each option displayed in a sector."""
        self.canvas.delete("wheel")  # Clear only the wheel, not the pointer
        center_x, center_y = 300, 300  # Center of the canvas
        radius = 250
        
        for i, option in enumerate(self.options):
            # Calculate the start and end angles for each sector
            start_angle = i * self.angle_per_option + offset_angle
            end_angle = start_angle + self.angle_per_option
            
            # Convert angles to radians for calculations
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Calculate the points for the sector
            x1, y1 = center_x + radius * math.cos(start_rad), center_y - radius * math.sin(start_rad)
            x2, y2 = center_x + radius * math.cos(end_rad), center_y - radius * math.sin(end_rad)
            
            # Choose fill color, highlight the current sector
            fill_color = "red" if i == highlight_index else self.random_color(i)
            
            # Draw the sector as a polygon with three points: center and two arc points
            self.canvas.create_polygon(
                center_x, center_y, x1, y1, x2, y2, 
                fill=fill_color, outline="black", tags="wheel"
            )
            
            # Calculate text position and angle
            mid_angle = math.radians(start_angle + self.angle_per_option / 2)
            text_x = center_x + (radius - 60) * math.cos(mid_angle)
            text_y = center_y - (radius - 60) * math.sin(mid_angle)
            text_rotation = start_angle + self.angle_per_option / 2  # Aligns text with sector
            
            # Calc truncated text
            text = option
            if(len(option)>33):
                text = option[:30]+"..."
            
            # Add text label for the option
            self.canvas.create_text(
                text_x, text_y, text=text, font=("Times", 10),
                angle=text_rotation, tags="wheel"
            )

    def draw_pointer(self):
        """Draw a fixed pointer on the right side of the wheel."""
        center_x, center_y = 300, 300  # Center of the canvas
        pointer_x = center_x + 250
        pointer_y_top = center_y - 20
        pointer_y_bottom = center_y + 20
        self.canvas.create_polygon(
            pointer_x, center_y, pointer_x + 20, pointer_y_top, pointer_x + 20, pointer_y_bottom,
            fill="red", outline="black", tags="pointer"
        )
    
    def random_color(self, seed):
        """Generate a random color for each sector based on a seed."""
        random.seed(seed)
        return f"#{random.randint(100, 255):02x}{random.randint(100, 255):02x}{random.randint(100, 255):02x}"
    
    def spin_wheel(self):
        self.spin_button.config(state="disabled")
        self.selected_option.set("Spinning...")
        
        # Animation parameters
        random.seed(time.time())
        total_spins = random.uniform(2.5, 6.8)  # Total spins
        delay = 0.005  # Initial delay
        offset_angle = 0
        total_offset_angle = total_spins * 360
        angle_change = 23 # speed: how many degrees to change per iter
        
        # Simulation of total animation time
        precomputed_seconds = 0
        current_angle_change = angle_change
        sim_offset_angle = total_spins * 360
        # Calculate total number of steps and cumulative time
        while sim_offset_angle > 0:
            # Add the delay for this step
            precomputed_seconds += delay
            sim_offset_angle -= current_angle_change
            current_angle_change *= 0.99
            if current_angle_change < 1.0:
                current_angle_change = 1.0
        # Not sure why my calculation is so far off, probably to do with tkinter update delay
        # I'll just scale approximately
        precomputed_seconds *= 7
        print(f"Precomputed total wheel animation time: {precomputed_seconds:.2f} seconds")
        soundTools.wheel_nonblocking(soundTools.arcadeSound, soundTools.fanfareSound, total_time=precomputed_seconds)
        
        
        while total_offset_angle > 0:
            total_offset_angle -= angle_change
            offset_angle = (offset_angle + angle_change) % 360
            # Determine which sector is currently selected by the pointer
            selected_index = int((-offset_angle % 360) / self.angle_per_option) % self.num_options
            
            # Redraw the wheel with the highlighted sector
            self.draw_wheel(offset_angle, highlight_index=selected_index)
            self.frame.update()
            time.sleep(delay)
            
            # Decrease spin speed by 2% each time
            angle_change *= 0.99
            if(angle_change < 1):
                angle_change = 1.0
        
        # Final selection
        final_choice = self.options[selected_index]
        
        self.selected_option.set(f"Result: {final_choice}")
        
        print("Result: "+final_choice)
        
        self.wheelResult = final_choice
        global wheel_result
        wheel_result = final_choice
        
        self.next_button.config(state="active")

    def hide(self):
        super().hide()
        # self.frame.place_forget()
        
        self.canvas.pack_forget()
        self.label.pack_forget()
        self.spin_button.pack_forget()
    
    def show(self):
        super().show()
        self.spin_button.config(state="active")
        self.wheelResult = ""
        global wheel_result
        wheel_result = ""
        self.setMessageLabel("spinner: "+wheelMap.lastSpinner)
        self.next_button.config(state="disabled")
        
        self.canvas.place(x=450, y=100) 
        self.label.place(x=750, y=720, anchor="center")
        self.spin_button.place(x=750, y=760, anchor="center")
    
    def handleNext(self):
        tkUtil.trigger_wheel_res_page()

def createWheelPage(root):
    wheelpage = WheelPage(root)
    return wheelpage


WHEEL_OPTIONS_PATH = "./data/Wheel.txt"

def readWheelOptions():
    # Open the file in read mode
    with open(WHEEL_OPTIONS_PATH, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines
    return []