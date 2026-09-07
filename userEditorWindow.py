from tkinter import *
from tkinter import ttk
from GUITools import HoverableListMaker, WindowSizingTask
from login import *
from DBTools import *
from GUITools import BindFamily
from deleteConfirmationWindow import DeleteConfirmationWindow
from userAddWindow import AddUserWindow
from userDetailEditWindow import UserDetailsWindow

def UserEditorWindow(eventHub):
    userEditWindow = Toplevel()
    userEditWindow.title('Edit Users')
    userEditWindow.state('zoomed')
    userEditWindow.columnconfigure(0, weight=1)
    userEditWindow.rowconfigure(1, weight=1)

    def CreateUserList(eventHub):
        users = ListUsers()

        listFrame = ttk.Frame(userEditWindow)
        listFrame.grid(row=1, column=0, sticky='NSEW')

        # Function to edit the interactive frame that appears on hover.
        def EditInteractiveFrame(interactiveElementsFrame: Frame | ttk.Frame,
                                 username: str):

            # Making the interactive elements.
            ttk.Button(interactiveElementsFrame, text="Edit User Details", style='Buttons.TButton',
                       command=lambda: UserDetailsWindow(username)).grid(row=0, column=0, sticky='E', padx=4)
            ttk.Button(interactiveElementsFrame, text="Delete User", style='Buttons.TButton',
                       command=lambda: DeleteConfirmationWindow(username, 'user', eventHub)).grid(row=0, column=1, sticky='E')

        interactiveFrameOperations = lambda frame, name: EditInteractiveFrame(frame, name)

        # Makes the interactive, hoverable list.
        HoverableListMaker(listFrame, users, interactiveFrameOperations)

        return listFrame

    def RefreshUserList(eventHub, *args):
        nonlocal listFrame
        listFrame.destroy()
        listFrame = CreateUserList(eventHub)

    listFrame = CreateUserList(eventHub)

    headFrame = ttk.Frame(userEditWindow)
    headFrame.grid(row=0, column=0, sticky='NSEW')
    headFrame.columnconfigure(0, weight=1)

    ttk.Label(headFrame, text='User Details:', justify='left', style='Headings.TLabel').grid(row=0, column=0, sticky='W', padx=10)
    ttk.Button(headFrame,
               text="Add New User",
               style='Buttons.TButton',
               command=lambda: AddUserWindow(eventHub)).grid(row=0, column=1, sticky='E', padx=10)

    WindowSizingTask(userEditWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(userEditWindow, '<Button-1>', lambda e: userEditWindow.focus_set(), bindInteractives=False)

    eventHub.bind('<<UserDeleted>>', lambda e: RefreshUserList(eventHub))
    eventHub.bind('<<UserAdded>>', lambda e: RefreshUserList(eventHub))