import tkinter as tk
import tkTools.tkUtil as tkUtil
import tkTools.tkHomePage as tkHomePage, tkTools.tkPostgamePage as tkPostgamePage
import tkTools.tkPickingPage as tkPickingPage, tkTools.tkAdjustmentsPage as tkAdjustmentsPage
import backendTools.parseChampStats as parseChampStats
import tkTools.tkWheelPage as tkWheelPage
import tkTools.tkWheelResultPage as tkWheelResultPage
import tkTools.tkMidgamePage as tkMidgamePage

def init_tk():
    tkUtil.root = tk.Tk()
    tkUtil.root.title("ITS MARBLIN TIME")
    tkUtil.root.protocol("WM_DELETE_WINDOW", on_close)
    tkUtil.root.geometry(str(tkUtil.WIDTH)+"x"+str(tkUtil.HEIGHT))
    
    homePage = tkHomePage.createHomePage(tkUtil.root)
    pickingPage = tkPickingPage.createPickingPage(tkUtil.root)
    adjustmentsPage = tkAdjustmentsPage.createAdjustmentsPage(tkUtil.root)
    
    tkUtil.wheelPage = tkWheelPage.createWheelPage(tkUtil.root)
    tkUtil.wheelResPage = tkWheelResultPage.createWheelResultPage(tkUtil.root)
    
    midGamePage = tkMidgamePage.createMidgamePage(tkUtil.root)
    postGamePage = tkPostgamePage.createPostgamePage(tkUtil.root)
    tkUtil.pages = [homePage, pickingPage, adjustmentsPage, midGamePage, postGamePage]
    tkUtil.curPage = 0


def on_close():
    tkUtil.root.quit()
    tkUtil.root.destroy()

def main():
    init_tk()
    parseChampStats.constructWinrates()
    
    # Start with the first page
    tkUtil.show_page(tkUtil.curPage)

    # Run the application
    tkUtil.root.mainloop()
    
    print("mainloop exited")
    

if __name__ == "__main__":
    main()