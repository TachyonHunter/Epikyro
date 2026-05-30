from tkinter import *
from tkinter import ttk
from GUITools import HoverableListMaker
from login import *
from DBTools import *
from GUITools import BindAllChildren
from deleteConfirmationWindow import DeleteConfirmationWindow
from UserDetailEditWindow import UserDetailsWindow

def UserEditorWindow():
    userEditWindow = Toplevel()
    userEditWindow.title('Edit Users')
    userEditWindow.state('zoomed')

    users = ListUsers()

    # Function to edit the interactive frame that appears on hover.
    def EditInteractiveFrame(interactiveElementsFrame, username):
        # Functions used by buttons.
        def MakeDeleteLambda(username):
            return lambda: DeleteConfirmationWindow(username)  # Getting the text in the username label.

        def MakeEditLambda(username):
            return lambda: UserDetailsWindow(username)

        # Making the interactive elements.
        ttk.Button(interactiveElementsFrame, text="Edit User Details", style='Buttons.TButton',
                   command=MakeEditLambda(username)).grid(row=0, column=0, sticky='E', padx=4)
        ttk.Button(interactiveElementsFrame, text="Delete User", style='Buttons.TButton',
                   command=MakeDeleteLambda(username)).grid(row=0, column=1, sticky='E')

    interactiveFrameOperations = lambda frame, name: EditInteractiveFrame(frame, name)

    # Makes the interactive, hoverable list.
    HoverableListMaker(userEditWindow, users, interactiveFrameOperations)

    # Code to prevent permanent focus steal by widgets.
    BindAllChildren(userEditWindow, '<Button-1>', lambda e: userEditWindow.focus_set(), bindInteractives=False)

    userEditWindow.mainloop()