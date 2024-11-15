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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ITS MARBLIN TIME")
        self.setGeometry(100, 100, 1500, 800)  # Width and height

        # Main layout for the window
        self.main_layout = QVBoxLayout()

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

    def show_page(self, page_num):
        """Show a specific page and hide others."""
        for i, page in enumerate(self.pages):
            if i != page_num:
                page.hide_page()

        print("animating!")
        self.pages[page_num].show_page()
        # pages[page_num].animate_message(pages[page_num].message_label)

def main():
    app = QApplication(sys.argv)
    
    # Create the main window and start the event loop
    window = MainWindow()
    window.show()

    parseChampStats.constructWinrates()

    # Start the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
