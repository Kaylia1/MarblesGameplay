import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtGui import QFont, QFontDatabase
from PIL import Image, ImageEnhance
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
import uiTools.uiGlobals as uiGlobals

curPage = 0
pages = []

wheelPage = None
wheelResPage = None


def popup(title, msg):
    # PyQt5's equivalent of a messagebox
    from PyQt5.QtWidgets import QMessageBox
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(msg)
    msg_box.exec_()


class Page(QWidget):
    IMAGE_PATH = "marblesreviews.png"
    processed_image = None

    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(0, 0, uiGlobals.width, uiGlobals.height)

        # Main layout for the page
        self.layout = QVBoxLayout(self)
        self.banner_layout = QVBoxLayout()

        # Title label
        # Load the custom font (Choii.otf)
        font_id = QFontDatabase.addApplicationFont('uiTools/Fonts/ChokoMilky-gx8gR.otf')
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        # Apply the font to the title_label
        title_font = QFont(font_family)
        title_font.setPointSize(32)

        # Title label with custom font
        self.title_label = QLabel(title, self)
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #FFFFFF;")
        self.title_label.resize(200, 50)
        self.title_label.move(10, 10)

        # Initializing the banner's properties
        self.banner = QWidget(self)
        self.banner.setStyleSheet("background-color: #3498db;")  # Set banner color
        self.banner.setFixedHeight(0)  # Initial height set to zero (rolled up)
        self.banner.setFixedWidth(uiGlobals.width)
        self.banner_layout.addWidget(self.banner)
        
        # title for banner
        self.banner_label = QLabel("Hello World", self)
        self.banner_label.setAlignment(Qt.AlignCenter)
        self.banner_label.setFont(title_font)
        self.banner_label.setStyleSheet("color: #FFFFFF;")
        self.banner_label.resize(200, 50)
        self.banner_label.move(int((uiGlobals.width-self.banner_label.width())/2), uiGlobals.height-990)

        # Message label
        self.message_label = QLabel(message, self)
        self.message_label.setStyleSheet("background-color: lightblue; padding: 12px;")
        self.message_label.setFont(title_font)
        self.message_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.message_label.setFixedWidth(400)
        self.message_label.setFixedHeight(80)
        # don't add to layout so that we can manually position

        # Next button
        self.next_button = QPushButton("Ok", self)
        self.next_button.clicked.connect(self.handle_next)
        self.next_button.move(uiGlobals.width-150, uiGlobals.height-150)

        # this is very jank, I use whitespace to position teh layout
        self.banner_layout.setContentsMargins(0, 0, 0, 850)  # Margin on top (y=100), left and right (50), bottom (50)
        
        self.layout.addLayout(self.banner_layout)
        self.setLayout(self.layout)

    @staticmethod
    def setup_background_image():
        """Load and process the background image once."""
        if Page.processed_image is None:
            image = Image.open(Page.IMAGE_PATH)
            enhancer = ImageEnhance.Brightness(image)
            faded_image = enhancer.enhance(0.5)
            resized_image = faded_image.resize((uiGlobals.width, uiGlobals.height))
            image = resized_image.convert("RGBA")
            Page.processed_image = QPixmap.fromImage(QImage(image.tobytes(), image.width, image.height, image.width * 4, QImage.Format_RGBA8888))

    def init_animations(self):
        """Initialize animations for the message."""
        if self.message_label.text():
            self.animate_message(self.message_label)

    def set_message_label(self, new_txt):
        """Update the message and re-animate."""
        self.message_label.setText(new_txt)
        self.animate_message(self.message_label)

    def animate_message(self, label):
        """Animate the message sliding from right to left."""
        start_x = uiGlobals.width
        target_x = uiGlobals.width-self.message_label.width() # slide all the way to the left
        y_position = 50

        print("started sliding")
        def slide():
            nonlocal start_x
            if start_x > target_x:
                start_x -= 3
                label.move(start_x, y_position)
                QTimer.singleShot(10, slide)
            else:
                label.move(target_x, y_position)

        slide()
    
    def unroll_banner(self):
        # Create the animation for the banner height
        self.animation = QPropertyAnimation(self.banner, b"maximumHeight")
        self.animation.setDuration(800)  # Duration of the animation in milliseconds
        self.animation.setStartValue(0)  # Start height at 0
        self.animation.setEndValue(100)  # End height at full size
        self.animation.start()

    def show_page(self):
        """Show the page and animate the message."""
        self.show()
        self.animate_message(self.message_label)
        self.unroll_banner()
        # self.banner1.show()#unroll_banner()

    def hide_page(self):
        """Hide the page."""
        self.hide()

    def handle_next(self):
        """Handle the Next button press."""
        print("Clicked ok")
        next_page()


def next_page():
    global curPage
    curPage = (curPage + 1) % len(pages)
    show_page(curPage)


def trigger_wheel_page():
    """Show the wheel page."""
    for i, page in enumerate(pages):
        page.hide_page()
    wheelResPage.hide_page()
    wheelPage.show_page()


def trigger_wheel_res_page():
    """Show the wheel result page."""
    for i, page in enumerate(pages):
        page.hide_page()
    wheelPage.hide_page()
    wheelResPage.show_page()