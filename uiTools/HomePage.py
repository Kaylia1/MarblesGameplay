import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import Qt
import backendTools.points as points
import backendTools.globals as globals
import uiTools.tkUtil as Page

class HomePage(Page.Page):
    def __init__(self, parent=None):
        super().__init__(parent, "Home Page", "Hello World")  # Pass the parent widget to QWidget
        self.setGeometry(0, 0, 1500, 800)
        
        # Layout for the entire page
        self.main_layout = QVBoxLayout(self)
        
        # Historic data label
        self.historicData = QLabel("Historic Data:", self)
        self.historicData.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.historicData)
        
        # Reminder message label
        self.reminderMsg = QLabel("Did you finish copying marbles output to data/marbles_output.txt?", self)
        self.reminderMsg.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.reminderMsg)
        
        # Stats labels will be placed in a grid layout
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)
        
        # Initialize and populate stats labels
        self.statsLabels = {}
        self.init_labels()
        
        # Load points data
        points.load_state()

    def init_labels(self):
        """Initializes and sets up the header and summoner stat labels."""
        headers = ["Name", "Money", "Kills", "Deaths", "Assists"]
        
        # Add headers to the grid layout
        for col, header in enumerate(headers):
            label = QLabel(header, self)
            label.setAlignment(Qt.AlignLeft)
            self.grid_layout.addWidget(label, 0, col)
        
        # Initialize and add summoner stat labels to the grid layout
        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            self.statsLabels[key] = {
                "name": QLabel(key, self),
                "money": QLabel(f"${summoner.money}", self),
                "kills": QLabel(str(summoner.kills), self),
                "deaths": QLabel(str(summoner.deaths), self),
                "assists": QLabel(str(summoner.assists), self),
            }

            # Add each label to the grid at the appropriate row and column
            self.grid_layout.addWidget(self.statsLabels[key]["name"], row, 0)
            self.grid_layout.addWidget(self.statsLabels[key]["money"], row, 1)
            self.grid_layout.addWidget(self.statsLabels[key]["kills"], row, 2)
            self.grid_layout.addWidget(self.statsLabels[key]["deaths"], row, 3)
            self.grid_layout.addWidget(self.statsLabels[key]["assists"], row, 4)

    def update_labels(self):
        """Updates the displayed data for each summoner."""
        for key, summoner in globals.summoners.items():
            self.statsLabels[key]["money"].setText(f"${summoner.money}")
            self.statsLabels[key]["kills"].setText(str(summoner.kills))
            self.statsLabels[key]["deaths"].setText(str(summoner.deaths))
            self.statsLabels[key]["assists"].setText(str(summoner.assists))

    def show_page(self):
        """Show the page, updating labels and saving the state."""
        self.update_labels()
        
        # Write the updated game state to file
        output = points.map_to_json(globals.summoners)
        points.save_state(output)

        self.show()  # Make sure the page is visible

    def hide_page(self):
        """Hide the page."""
        self.hide()  # Hide the page

def createHomePage(root):
    return HomePage(root)