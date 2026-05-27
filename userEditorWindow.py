from tkinter import *
from tkinter import ttk
from GUITools import HoverableListMaker
from login import *
from DBTools import *
from DeleteConfirmationWindow import DeleteConfirmationWindow
from UserDetailEditWindow import UserDetailEditWindow

def UserEditorWindow():
    userEditWindow = Toplevel()
    userEditWindow.title('Edit Users')
    userEditWindow.state('zoomed')

    users = ListUsers()

    def EditInteractiveFrame(interactiveElementsFrame, username):
        # Functions used by buttons.
        def MakeDeleteLambda(username):
            return lambda: DeleteConfirmationWindow(username.cget("text"))  # Getting the text in the username label.

        def MakeEditLambda(username):
            return lambda: UserDetailEditWindow(username.cget("text"))

        # Making the interactive elements.
        ttk.Button(interactiveElementsFrame, text="Edit User Details", style='Buttons.TButton',
                   command=MakeEditLambda(username)).grid(row=0, column=0, sticky='E')
        ttk.Button(interactiveElementsFrame, text="Delete User", style='Buttons.TButton',
                   command=MakeDeleteLambda(username)).grid(row=0, column=1, sticky='E')
    interactiveFrameOperations = lambda frame, name: EditInteractiveFrame(frame, name)

    # Makes the interactive, hoverable list.
    HoverableListMaker(userEditWindow, users, interactiveFrameOperations)

    userEditWindow.mainloop()