from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont

class Banner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # Set the initial position and width
        self.setFixedWidth(600)  # Set a fixed width for the banner
        self.setFixedHeight(0)   # Set initial height to 0 (rolled up)
        
        # self.move(0, 100)  # Position it at the top of the parent widget or window
        
        # Set the background color and label inside the banner
        self.setStyleSheet("background-color: #3498db;")
        
        self.banner_label = QLabel("Welcome to the App!", self)
        font = QFont("Arial", 16)
        self.banner_label.setFont(font)
        self.banner_label.setStyleSheet("color: white;")
        # self.banner_label.move(50, 20)  # Position the label inside the banner
        self.layout.addWidget(self.banner_label)
        self.setLayout(self.layout)

    def showEvent(self, event):
        """Override the show event to trigger the banner animation"""
        super().showEvent(event)  # Ensure the standard show event is called
        self.unroll_banner()

    def unroll_banner(self):
        """Animate the banner's height from 0 to its full height"""
        
        print("unrolling banner")
        
        # self.animation = QPropertyAnimation(self, b"maximumHeight")
        # self.animation.setDuration(800)  # Duration of the animation in milliseconds
        # self.animation.setStartValue(0)  # Start height at 0
        # self.animation.setEndValue(100)  # End height at full size
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(2000)  # Duration of the animation (2 seconds)
        self.animation.setStartValue(QRect(self.x(), self.y(), self.width(), 0))  # Start with height = 0
        self.animation.setEndValue(QRect(self.x(), self.y(), self.width(), 100))  # End with height = 100
        self.animation.start()