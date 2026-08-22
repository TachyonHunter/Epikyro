from tkinter import *
from tkinter import ttk
from CVTools import GetExistingCV, ListOwnedCVs
from GUITools import HoverableListMaker, BindAllChildren, WindowSizingTask

def InspectOwnedCVsWindow(user: str):
    ownedCVInspectorWindow = Toplevel()
    ownedCVInspectorWindow.title(f'Inspect {user}\'s owned CVs')
    ownedCVInspectorWindow.state('zoomed')
    ownedCVInspectorWindow.rowconfigure(0, weight=1)
    ownedCVInspectorWindow.columnconfigure(0, weight=1)

    OwnedCVs = ListOwnedCVs(user)
    mainframe = ttk.Frame(ownedCVInspectorWindow)
    mainframe.grid(row=0, column=0, sticky='NSEW')
    mainframe.rowconfigure(1, weight=1)
    mainframe.columnconfigure(0, weight=1)

    if OwnedCVs == 'not found':
        ttk.Label(mainframe, text='No CVs associated with this user',
                  style='Sub-headings.TLabel',
                  justify='left').grid(row=0, column=0, sticky='W', padx=8)

    else:
        canvasFrame = ttk.Frame(mainframe)
        canvasFrame.grid(row=1, column=0, sticky='NSEW')

        def EditInteractiveFrame(interactiveElementsFrame: Frame | ttk.Frame,
                                 candidateName: str):
            ttk.Button(interactiveElementsFrame, text=f'Open {candidateName}\'s CV', style='Buttons.TButton').grid(row=0, column=0)

        interactiveFrameOperations = lambda frame, name: EditInteractiveFrame(frame, name)

        # Makes the interactive, hoverable list.
        HoverableListMaker(canvasFrame, [f'{k} - {v}' for k, v in OwnedCVs.items()], interactiveFrameOperations)

        ttk.Label(mainframe, text=f'{user}\'s owned CVs:',
                  justify='left',
                  style='Headings.TLabel').grid(row=0, column=0, sticky='W', padx=8)

        WindowSizingTask(ownedCVInspectorWindow)

        # Code to prevent permanent focus steal by widgets.
        BindAllChildren(ownedCVInspectorWindow, '<Button-1>', lambda e: ownedCVInspectorWindow.focus_set(), bindInteractives=False)