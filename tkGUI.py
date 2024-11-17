import tkinter as tk
import tkTools.tkUtil as tkUtil
import tkTools.tkHomePage as tkHomePage, tkTools.tkPostgamePage as tkPostgamePage
import tkTools.tkPickingPage as tkPickingPage, tkTools.tkAdjustmentsPage as tkAdjustmentsPage
import backendTools.parseChampStats as parseChampStats
import tkTools.tkWheelPage as tkWheelPage
import tkTools.tkWheelResultPage as tkWheelResultPage
import tkTools.tkMidgamePage as tkMidgamePage
import argparse
import dropbox

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


key = "sl.CA5OdXez-buGlvgfIz7ULeXhpP-HBjLZC4pIxBQnGdJxSdjkiSSVeJL3yEwrWXUsvMYAsuPpMuc537bqeAIoS22Qti1pahXcRUOX_Nkz4SHxqehjgcbrWN0Z7z0jkNfxeM6bnR-GNlRf"
dbx = dropbox.Dropbox(key)

def read_file_content(dropbox_file_path):
    """Read content of a file in Dropbox without downloading."""
    try:
        # Get the file content
        metadata, response = dbx.files_download(dropbox_file_path)
        file_content = response.content.decode("utf-8")  # Decode the bytes to string
        print(f"Content of {dropbox_file_path}:\n{file_content}")
        return file_content
    except dropbox.exceptions.ApiError as e:
        print(f"Error reading file: {e}")
        return None

def main():
    # parser = argparse.ArgumentParser(description="Script that accepts an optional argument.")
    
    # # Add an optional argument
    # parser.add_argument(
    #     "--name",  # Argument flag
    #     type=str,  # Expected type
    #     help="Your name (optional)",  # Description
    #     default="Guest"  # Default value if not provided
    # )
    
    # # Parse the arguments
    # args = parser.parse_args()
    
    # # Access the optional argument
    # name = args.name
    # print(f"Hello, {name}!")
    
    # read_file_content("/saved_points.json")

    
    init_tk()
    parseChampStats.constructWinrates()
    
    # Start with the first page
    tkUtil.show_page(tkUtil.curPage)

    # Run the application
    tkUtil.root.mainloop()
    
    print("mainloop exited")
    

if __name__ == "__main__":
    main()