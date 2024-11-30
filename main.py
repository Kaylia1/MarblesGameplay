import tkinter as tk
import uiTools.uiPage as uiPage
import uiTools.uiHomePage as uiHomePage, uiTools.uiPostgamePage as uiPostgamePage
import uiTools.uiPickingPage as uiPickingPage, uiTools.uiAdjustmentsPage as uiAdjustmentsPage
import backendTools.parseChampStats as parseChampStats
import uiTools.uiWheelPage as uiWheelPage
import uiTools.uiWheelResultPage as uiWheelResultPage
import uiTools.uiMidgamePage as uiMidgamePage
import argparse
import firebase.firebaseTools as firebaseTools
import json
import backendTools.globals as globals
import discordBot # runs in background

def init_tk():
    uiPage.root = tk.Tk()
    uiPage.root.title("ITS MARBLIN TIME")
    uiPage.root.protocol("WM_DELETE_WINDOW", on_close)
    uiPage.root.geometry(str(uiPage.WIDTH)+"x"+str(uiPage.HEIGHT))
    
    homePage = uiHomePage.createHomePage(uiPage.root)
    pickingPage = uiPickingPage.createPickingPage(uiPage.root)
    adjustmentsPage = uiAdjustmentsPage.createAdjustmentsPage(uiPage.root)
    
    uiPage.wheelPage = uiWheelPage.createWheelPage(uiPage.root)
    uiPage.wheelResPage = uiWheelResultPage.createWheelResultPage(uiPage.root)
    
    midGamePage = uiMidgamePage.createMidgamePage(uiPage.root)
    postGamePage = uiPostgamePage.createPostgamePage(uiPage.root)
    uiPage.pages = [homePage, pickingPage, adjustmentsPage, midGamePage, postGamePage]
    uiPage.curPage = 0


def on_close():
    uiPage.root.quit()
    uiPage.root.destroy()

def main():
    parser = argparse.ArgumentParser(description="Script that accepts an optional argument.")
    
    # Add an optional argument
    parser.add_argument(
        "--mode",  # Argument flag
        type=str,  # Expected type
        help="Y (optional)",  # Description
        default="Guest"  # Default value if not provided
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Access the optional argument
    globals.mode = args.mode
    print(f"Hello, {globals.mode}!")
    
    init_tk()
    parseChampStats.constructWinrates()
    
    # Start with the first page
    uiPage.show_page(uiPage.curPage)

    # Run the application
    uiPage.root.mainloop()
    
    print("mainloop exited")
    

if __name__ == "__main__":
    main()