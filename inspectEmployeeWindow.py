from tkinter import *
from tkinter import ttk

from CVManagerWindow import CVManagerWindow
from CVTools import GetExistingCV
from DBTools import ListUsers
from GUITools import HoverableListMaker, BindFamily, WindowSizingTask

def InspectEmployeeWindow(eventHub):
    inspectEmployeeWindow = Toplevel()
    inspectEmployeeWindow.title('Inspect employees')
    inspectEmployeeWindow.state('zoomed')
    inspectEmployeeWindow.rowconfigure(0, weight=1)
    inspectEmployeeWindow.columnconfigure(0, weight=1)

    users = ListUsers(skipAdmins=True)

    mainframe = ttk.Frame(inspectEmployeeWindow)
    mainframe.grid(row=0, column=0, sticky='NSEW')
    mainframe.rowconfigure(1, weight=1)
    mainframe.columnconfigure(0, weight=1)

    canvasFrame = ttk.Frame(mainframe)
    canvasFrame.grid(row=1, column=0, sticky='NSEW')

    def EditInteractiveFrame(interactiveElementsFrame: Frame | ttk.Frame,
                             username: str):

        ttk.Button(interactiveElementsFrame, text='Inspect owned CVs',
                   style='Buttons.TButton',
                   command=lambda: CVManagerWindow(username, eventHub, mode='view')).grid(row=0, column=0)

    interactiveFrameOperations = lambda frame, name: EditInteractiveFrame(frame, name)

    # Makes the interactive, hoverable list.
    HoverableListMaker(canvasFrame, users, interactiveFrameOperations)

    ttk.Label(mainframe, text='Inspect Users:', justify='left', style='Headings.TLabel').grid(row=0, column=0, sticky='W', padx=8)

    WindowSizingTask(inspectEmployeeWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(inspectEmployeeWindow, '<Button-1>', lambda e: inspectEmployeeWindow.focus_set(), bindInteractives=False)