import tkTools.tkUtil as tkUtil

class PostgamePage(tkUtil.Page):
    def __init__(self, root):
        super().__init__(root, "Post-Game", "ggs")
        
    def hide(self):
        super().hide()
        self.frame.place_forget()

def createPostgamePage(root):
    homepage = PostgamePage(root)
    return homepage