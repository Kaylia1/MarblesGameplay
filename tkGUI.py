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
    tkUtil.root.geometry(str(tkUtil.WIDTH)+"x"+str(tkUtil.HEIGHT))
    
    # img = tk.PhotoImage(file="kay.png") # image code is too complicated bro
    # button = tk.Button(
    #     tkUtil.root, 
    #     image=img,
    #     text="WAHOO",
    #     font=("Helvetica", 12, "bold"),
    #     fg="white",
    #     bg="#4CAF50",       # Green background color
    #     activebackground="#45a049",  # Darker green when clicked
    #     activeforeground="white",
    #     relief="raised",      # Removes the default border
    #     bd=3,               # Sets border width for a flat effect
    #     padx=10,            # Adds padding within the button
    #     pady=5,              # Adds padding within the button
    #     width=50,
    #     height=20,
    # )
    # button.image = img
    # button.configure(highlightbackground="#4CAF50", highlightthickness=0)

    # def on_enter(event):
    #     button.config(bg="#45a049")

    # def on_leave(event):
    #     button.config(bg="#4CAF50")

    # # Bind hover effect events
    # button.bind("<Enter>", on_enter)
    # button.bind("<Leave>", on_leave)
    
    # button.pack(pady=20)
    
    homePage = tkHomePage.createHomePage(tkUtil.root)
    pickingPage = tkPickingPage.createPickingPage(tkUtil.root)
    adjustmentsPage = tkAdjustmentsPage.createAdjustmentsPage(tkUtil.root)
    
    tkUtil.wheelPage = tkWheelPage.createWheelPage(tkUtil.root) #tkUtil.Page(tkUtil.root, "Wheel of Fortune", "")
    tkUtil.wheelResPage = tkWheelResultPage.createWheelResultPage(tkUtil.root) #tkUtil.Page(tkUtil.root, "Wheel of Fortune", "")
    
    midGamePage = tkMidgamePage.createMidgamePage(tkUtil.root)
    postGamePage = tkPostgamePage.createPostgamePage(tkUtil.root)
    tkUtil.pages = [homePage, pickingPage, adjustmentsPage, midGamePage, postGamePage]
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