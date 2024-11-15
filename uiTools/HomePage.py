from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt
import backendTools.points as points
import backendTools.globals as globals
import uiTools.uiGlobals as uiGlobals
from PyQt5.QtGui import QFont
import uiTools.tkUtil as Page
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy



class HomePage(Page.Page):
    def __init__(self, parent):
        super().__init__(parent, "Home Page", "Hello World")
        
        # Main layout
        self.home_layout = QVBoxLayout(self)
        # self.home_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # self.layout.addLayout(self.home_layout)
        
        # Historic Data label
        self.historicData = QLabel("Historic Data:", self)
        self.historicData.setFont(QFont("Arial", 12))
        self.historicData.setAlignment(Qt.AlignCenter)
        self.home_layout.addWidget(self.historicData)
        
        # Reminder message
        self.reminderMsg = QLabel("Did you finish copying marbles output to data/marbles_output.txt?", self)
        self.reminderMsg.setFont(QFont("Arial", 12))
        self.reminderMsg.setAlignment(Qt.AlignCenter)
        self.home_layout.addWidget(self.reminderMsg)
        
        # Stats Labels grid
        self.gridframe = QFrame(self)
        self.grid_layout = QGridLayout(self.gridframe)
        self.home_layout.addWidget(self.gridframe)
        
        points.load_state()  # Load game state
        self.statsLabels = {}
        self.init_labels()  # Initialize headers and stat labels
        
        # Set up a button for updating or any other actions
        self.update_button = QPushButton("Update Stats", self)
        self.update_button.clicked.connect(self.update_labels)
        self.home_layout.addWidget(self.update_button)
        
        self.setLayout(self.home_layout)

    def init_labels(self):
        """Initializes and packs the header and summoner stat labels."""
        headers = ["Name", "Money", "Kills", "Deaths", "Assists"]
        
        # Add headers to grid layout
        for col, header in enumerate(headers):
            label = QLabel(header, self)
            label.setFont(QFont("Arial", 12))
            self.grid_layout.addWidget(label, 0, col)
        
        # Initialize and place summoner stat labels
        for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
            self.statsLabels[key] = {
                "name": QLabel(key, self),
                "money": QLabel(f"${summoner.money}", self),
                "kills": QLabel(str(summoner.kills), self),
                "deaths": QLabel(str(summoner.deaths), self),
                "assists": QLabel(str(summoner.assists), self),
            }
            
            # Position each label in the grid layout
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
        
        # Write game state to file
        output = points.map_to_json(globals.summoners)
        points.save_state(output)

    def show(self):
        """Show the page."""
        super().show()
        self.update_labels()

    def hide(self):
        """Hide the page."""
        super().hide()

def createHomePage(parent):
    return HomePage(parent)


# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton
# from PyQt5.QtCore import Qt
# import backendTools.points as points
# import backendTools.globals as globals
# import uiTools.tkUtil as Page
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDesktopWidget


# class HomePage(Page.Page):
#     def __init__(self, parent=None):
#         super().__init__(parent, "Home Page", "Hello World")  # Pass the parent widget to QWidget
        
#         # Layout for the entire page
#         container_widget = QWidget()
#         self.center_on_screen(container_widget)
#         self.main_layout = QVBoxLayout(container_widget)
#         self.home_layout.addLayout(self.main_layout)
        
#         # # Historic data label
#         self.historicData = QLabel("Historic Data:", self)
#         self.historicData.setAlignment(Qt.AlignCenter)
#         self.main_layout.addWidget(self.historicData)
        
#         geometry = container_widget.geometry()
#         print("Layout2 Container Position (x, y):", geometry.x(), geometry.y())
#         print("Layout2 Container Dimensions (width, height):", geometry.width(), geometry.height())
        
#         # # Reminder message label
#         # self.reminderMsg = QLabel("Did you finish copying marbles output to data/marbles_output.txt?", self)
#         # self.reminderMsg.setAlignment(Qt.AlignCenter)
#         # # self.main_layout.addWidget(self.reminderMsg)
        
#         # # Stats labels will be placed in a grid layout
#         # self.grid_layout = QGridLayout()
#         # # self.main_layout.addLayout(self.grid_layout)
        
#         # # Initialize and populate stats labels
#         # self.statsLabels = {}
#         # self.init_labels()
        
#         # # Load points data
#         # points.load_state()

#     def center_on_screen(self, widget):
#         # Get the screen geometry
#         screen_geometry = QDesktopWidget().screenGeometry()

#         # Get the widget geometry
#         widget_geometry = widget.geometry()

#         # Calculate the center position
#         x = (screen_geometry.width() - widget_geometry.width()) // 2
#         y = (screen_geometry.height() - widget_geometry.height()) // 2

#         # Move the widget to the center of the screen
#         widget.move(x, y)

#     # def init_labels(self):
#     #     """Initializes and sets up the header and summoner stat labels."""
#     #     headers = ["Name", "Money", "Kills", "Deaths", "Assists"]
        
#     #     # Add headers to the grid layout
#     #     for col, header in enumerate(headers):
#     #         label = QLabel(header, self)
#     #         label.setAlignment(Qt.AlignLeft)
#     #         self.grid_layout.addWidget(label, 0, col)
        
#     #     # Initialize and add summoner stat labels to the grid layout
#     #     for row, (key, summoner) in enumerate(globals.summoners.items(), start=1):
#     #         self.statsLabels[key] = {
#     #             "name": QLabel(key, self),
#     #             "money": QLabel(f"${summoner.money}", self),
#     #             "kills": QLabel(str(summoner.kills), self),
#     #             "deaths": QLabel(str(summoner.deaths), self),
#     #             "assists": QLabel(str(summoner.assists), self),
#     #         }

#     #         # Add each label to the grid at the appropriate row and column
#     #         self.grid_layout.addWidget(self.statsLabels[key]["name"], row, 0)
#     #         self.grid_layout.addWidget(self.statsLabels[key]["money"], row, 1)
#     #         self.grid_layout.addWidget(self.statsLabels[key]["kills"], row, 2)
#     #         self.grid_layout.addWidget(self.statsLabels[key]["deaths"], row, 3)
#     #         self.grid_layout.addWidget(self.statsLabels[key]["assists"], row, 4)

#     # def update_labels(self):
#     #     """Updates the displayed data for each summoner."""
#     #     for key, summoner in globals.summoners.items():
#     #         self.statsLabels[key]["money"].setText(f"${summoner.money}")
#     #         self.statsLabels[key]["kills"].setText(str(summoner.kills))
#     #         self.statsLabels[key]["deaths"].setText(str(summoner.deaths))
#     #         self.statsLabels[key]["assists"].setText(str(summoner.assists))

#     def show_page(self):
#         """Show the page, updating labels and saving the state."""
#         super().show_page()
#         # self.update_labels()
        
#         # Write the updated game state to file
#         output = points.map_to_json(globals.summoners)
#         points.save_state(output)

#         self.show()  # Make sure the page is visible

#     def hide_page(self):
#         """Hide the page."""
#         super().hide_page()
#         self.hide()  # Hide the page

# def createHomePage(root):
#     return HomePage(root)