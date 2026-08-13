from tkinter import *
from tkinter import ttk
from CVTools import GetExistingCV, ListOwnedCVs
from GUITools import HoverableListMaker, BindAllChildren

def InspectOwnedCVsWindow(user: str):
    inspectOwnedCVsWindow = Toplevel()
    inspectOwnedCVsWindow.title(f'Inspect {user}\'s owned CVs')
    inspectOwnedCVsWindow.state('zoomed')
    inspectOwnedCVsWindow.rowconfigure(0, weight=1)
    inspectOwnedCVsWindow.columnconfigure(0, weight=1)

    OwnedCVs = ListOwnedCVs(user)
    mainframe = ttk.Frame(inspectOwnedCVsWindow)
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

        # Code to prevent permanent focus steal by widgets.
        BindAllChildren(inspectOwnedCVsWindow, '<Button-1>', lambda e: inspectOwnedCVsWindow.focus_set(), bindInteractives=False)