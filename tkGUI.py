import tkinter as tk
import tkTools.tkUtil as tkUtil
import tkTools.tkHomePage as tkHomePage, tkTools.tkPostgamePage as tkPostgamePage
import tkTools.tkPickingPage as tkPickingPage, tkTools.tkAdjustmentsPage as tkAdjustmentsPage
import backendTools.parseChampStats as parseChampStats

def init_tk():
    tkUtil.root = tk.Tk()
    tkUtil.root.title("ITS MARBLIN TIME")
    tkUtil.root.geometry(str(tkUtil.WIDTH)+"x"+str(tkUtil.HEIGHT))
    
    
    homePage = tkHomePage.createHomePage(tkUtil.root)
    pickingPage = tkPickingPage.createPickingPage(tkUtil.root)
    adjustmentsPage = tkAdjustmentsPage.createAdjustmentsPage(tkUtil.root)
    # wheelPage = Page(tkUtil.root, "Wheel of Fortune", "", None)
    postGamePage = tkPostgamePage.createPostgamePage(tkUtil.root)
    tkUtil.pages = [homePage, pickingPage, adjustmentsPage, postGamePage]
    tkUtil.curPage = 0


def main():
    init_tk()
    parseChampStats.constructWinrates()
    
    # Start with the first page
    tkUtil.show_page(tkUtil.curPage)

    # Run the application
    tkUtil.root.mainloop()

if __name__ == "__main__":
    main()