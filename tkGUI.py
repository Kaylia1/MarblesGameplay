import tkinter as tk
import tkUtil
import tkHomePage, tkPostgamePage


def init_tk():
    tkUtil.root = tk.Tk()
    tkUtil.root.title("ITS MARBLIN TIME")
    tkUtil.root.geometry(str(tkUtil.WIDTH)+"x"+str(tkUtil.HEIGHT))
    
    
    homePage = tkHomePage.createHomePage(tkUtil.root)
    # pickingPage = Page(tkUtil.root, "Picking", "", None)
    # wheelPage = Page(tkUtil.root, "Wheel of Fortune", "", None)
    postGamePage = tkPostgamePage.createPostgamePage(tkUtil.root)
    tkUtil.pages = [homePage, postGamePage]
    tkUtil.curPage = 0


def main():
    init_tk()
    
    # Start with the first page
    tkUtil.show_page(tkUtil.curPage)

    # Run the application
    tkUtil.root.mainloop()

if __name__ == "__main__":
    main()