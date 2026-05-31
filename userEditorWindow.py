from tkinter import *
from tkinter import ttk
from GUITools import HoverableListMaker
from login import *
from DBTools import *
from GUITools import BindAllChildren
from userDeleteConfirmationWindow import DeleteConfirmationWindow
from userAddWindow import AddUserWindow
from userDetailEditWindow import UserDetailsWindow

def UserEditorWindow():
    userEditWindow = Toplevel()
    userEditWindow.title('Edit Users')
    userEditWindow.state('zoomed')
    userEditWindow.columnconfigure(0, weight=1)
    userEditWindow.rowconfigure(1, weight=1)

    canvasFrame = None

    refreshLambda = lambda: CreateOrRefreshUserList(userEditWindow)

    def CreateOrRefreshUserList(userEditWindow):
        nonlocal canvasFrame

        if canvasFrame is not None:
            canvasFrame.destroy()

        users = ListUsers()

        canvasFrame = ttk.Frame(userEditWindow)
        canvasFrame.grid(row=1, column=0, sticky='NSEW')

        # Function to edit the interactive frame that appears on hover.
        def EditInteractiveFrame(interactiveElementsFrame, username):
            # Functions used by buttons.
            def MakeDeleteLambda(username):
                return lambda: DeleteConfirmationWindow(username, refreshLambda)  # Getting the text in the username label.

            def MakeEditLambda(username):
                return lambda: UserDetailsWindow(username)

            # Making the interactive elements.
            ttk.Button(interactiveElementsFrame, text="Edit User Details", style='Buttons.TButton',
                       command=MakeEditLambda(username)).grid(row=0, column=0, sticky='E', padx=4)
            ttk.Button(interactiveElementsFrame, text="Delete User", style='Buttons.TButton',
                       command=MakeDeleteLambda(username)).grid(row=0, column=1, sticky='E')

        interactiveFrameOperations = lambda frame, name: EditInteractiveFrame(frame, name)

        # Makes the interactive, hoverable list.
        HoverableListMaker(canvasFrame, users, interactiveFrameOperations)

    headFrame = ttk.Frame(userEditWindow)
    headFrame.grid(row=0, column=0, sticky='NSEW')
    headFrame.columnconfigure(0, weight=1)

    ttk.Label(headFrame, text='User Details:', justify='left', style='Headings.TLabel').grid(row=0, column=0, sticky='W', padx=10)
    ttk.Button(headFrame,
               text="Add New User",
               style='Buttons.TButton',
               command=lambda: AddUserWindow(refreshLambda)).grid(row=0, column=1, sticky='E', padx=10)

    CreateOrRefreshUserList(userEditWindow)

    # Code to prevent permanent focus steal by widgets.
    BindAllChildren(userEditWindow, '<Button-1>', lambda e: userEditWindow.focus_set(), bindInteractives=False)