import tkinter as tk
import random
import time
import math

WHEEL_OPTIONS_PATH = "./data/Wheel.txt"
wheelResult = "Top lane trades marble with Kay"

class WheelOfFortune:
    def __init__(self, root, options):
        self.root = root
        self.options = options
        self.num_options = len(options)
        self.angle_per_option = 360 / self.num_options
        self.selected_option = tk.StringVar()
        self.selected_option.set("Click to Spin")
        
        # Canvas for the wheel
        self.canvas = tk.Canvas(root, width=700, height=700, bg="white")
        self.canvas.pack(pady=20)
        
        # Label to display the selected option
        self.label = tk.Label(root, textvariable=self.selected_option, font=("Times", 12))
        self.label.pack(pady=10)
        
        # Button to spin the wheel
        self.spin_button = tk.Button(root, text="Spin the Wheel", command=self.spin_wheel, font=("Times", 16))
        self.spin_button.pack(pady=20)
        
        self.draw_wheel()  # Initial drawing of the wheel
        self.draw_pointer()  # Draw the fixed pointer

    def draw_wheel(self, offset_angle=0, highlight_index=None):
        """Draws the wheel with each option displayed in a sector."""
        self.canvas.delete("wheel")  # Clear only the wheel, not the pointer
        center_x, center_y = 350, 350  # Center of the canvas
        radius = 300
        
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
        center_x, center_y = 350, 350  # Center of the canvas
        pointer_x = center_x + 300
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
        total_spins = random.uniform(2.0, 4.5)  # Total spins
        delay = 0.005  # Initial delay
        offset_angle = 0
        total_offset_angle = total_spins * 360
        angle_change = 23
        while total_offset_angle > 0:
            total_offset_angle -= angle_change
            offset_angle = (offset_angle + angle_change) % 360
            # Determine which sector is currently selected by the pointer
            selected_index = int((-offset_angle % 360) / self.angle_per_option) % self.num_options
            
            # Redraw the wheel with the highlighted sector
            self.draw_wheel(offset_angle, highlight_index=selected_index)
            self.root.update()
            time.sleep(delay)
            
            angle_change *= 0.99
            if(angle_change < 1):
                angle_change = 1.0
        
        # Final selection
        final_choice = self.options[selected_index]
        self.selected_option.set(f"Result: {final_choice}")
        
        global wheelResult
        wheelResult = final_choice
        
        # Enable the button again after spinning
        # for now remove this since we don't have a comprehensive UI
        # self.spin_button.config(state="normal")

def readWheelOptions():
    # Open the file in read mode
    with open(WHEEL_OPTIONS_PATH, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines
    return []


def startApp():
    root = tk.Tk()
    root.title("Wheel of Fortune Spinner")
    options = readWheelOptions()#["Option A", "Option B", "Option C", "Option D", "Option E", "Option F"]
    app = WheelOfFortune(root, options)
    root.mainloop()
    
    print("Finished Wheel spin!")

# Main code to run the application
# if __name__ == "__main__":
#     startApp()
