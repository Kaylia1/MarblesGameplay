import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import backendTools.parseChampStats as parseChampStats
import uiTools.tkUtil as Page
import uiTools.HomePage as HomePage
import uiTools.tkPostgamePage as tkPostgamePage
import uiTools.tkPickingPage as tkPickingPage
import uiTools.tkAdjustmentsPage as tkAdjustmentsPage
import uiTools.tkWheelPage as tkWheelPage
import uiTools.tkWheelResultPage as tkWheelResultPage
import uiTools.tkMidgamePage as tkMidgamePage
import uiTools.uiGlobals as uiGlobals
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PIL import Image, ImageEnhance
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtGui import QBrush

def enhance_image(image_path, enhancement_factor=0.5):
    """Enhance the image using PIL and return a QPixmap."""
    # Load image using Pillow
    image = Image.open(image_path)
    
    # Enhance brightness (you can also apply contrast, sharpness, etc.)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(enhancement_factor)  # Adjust the factor as needed
    
    # Convert the enhanced image to QPixmap
    image = image.convert("RGBA")
    data = image.tobytes()
    pixmap = QPixmap.fromImage(QImage(data, image.width, image.height, image.width * 4, QImage.Format_RGBA8888))
    
    return pixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ITS MARBLIN TIME")
        self.showMaximized()
        self.get_screen_size()

        # Main layout for the window
        self.main_layout = QVBoxLayout()
        
        # set background image
        enhanced_pixmap = enhance_image("./marblesreviews.png", enhancement_factor=0.3)  # Adjust factor here
        palette = self.palette()
        palette.setBrush(self.backgroundRole(), QBrush(enhanced_pixmap))
        self.setPalette(palette)

        # Initialize pages here
        self.homePage = Page.Page(self, "HIHI", "hello world")#HomePage.createHomePage(self)
        # self.pickingPage = tkPickingPage.createPickingPage(self)
        # self.adjustmentsPage = tkAdjustmentsPage.createAdjustmentsPage(self)
        # self.wheelPage = tkWheelPage.createWheelPage(self)
        # self.wheelResPage = tkWheelResultPage.createWheelResultPage(self)
        # self.midGamePage = tkMidgamePage.createMidgamePage(self)
        # self.postGamePage = tkPostgamePage.createPostgamePage(self)

        self.pages = [self.homePage] #, self.pickingPage, self.adjustmentsPage, self.midGamePage, self.postGamePage]
        self.curPage = 0
        
        # Set up layout for the first page
        self.show_page(self.curPage)

        # Set central widget and layout
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)
        

    def get_screen_size(self):
        """Get the screen size in pixels after full screen."""
        screen = QApplication.primaryScreen()
        size = screen.size()
        uiGlobals.width = size.width()
        uiGlobals.height = size.height()
        print(f"Screen size: {uiGlobals.width}x{uiGlobals.height} pixels")

    # assumes that it is a numerical page
    def show_next_page(self):
        """Show next page and hide others."""
        self.curPage = (self.curPage+1)%len(self.pages)
        self.show_page(self.curPage)

    def show_page(self, page_num):
        """Show a specific page and hide others."""
        for i, page in enumerate(self.pages):
            if i != page_num:
                page.hide_page()

        print("animating!")
        self.pages[page_num].show_page()

window = None

def main():
    app = QApplication(sys.argv)
    
    # Create the main window and start the event loop
    global window
    window = MainWindow()
    window.show()

    parseChampStats.constructWinrates()

    # Start the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
