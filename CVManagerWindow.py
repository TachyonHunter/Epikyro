from tkinter import *
from tkinter import ttk
from CVTools import ListOwnedCVs
from GUITools import HoverableListMaker, BindFamily, WindowSizingTask
from CVEditorWindow import CVEditorWindow

def CVManagerWindow(user: str, mode: str = 'edit'):
    CVManagerWindow = Toplevel()
    CVManagerWindow.title(f'Your owned CVs' if mode == 'edit' else f'{user}\'s owned CVs')
    CVManagerWindow.state('zoomed')
    CVManagerWindow.rowconfigure(0, weight=1)
    CVManagerWindow.columnconfigure(0, weight=1)

    OwnedCVs = ListOwnedCVs(user)
    mainframe = ttk.Frame(CVManagerWindow)
    mainframe.grid(row=0, column=0, sticky='NSEW')
    mainframe.rowconfigure(1, weight=1)
    mainframe.columnconfigure(0, weight=1)

    if OwnedCVs == 'not found':
        ttk.Label(mainframe, text='No CVs associated with you...' if mode == 'edit' else f'No CVs associated with {user}...',
                  style='Sub-headings.TLabel',
                  justify='left').grid(row=0, column=0, sticky='W', padx=8)

    else:
        canvasFrame = ttk.Frame(mainframe)
        canvasFrame.grid(row=1, column=0, sticky='NSEW')

        def EditInteractiveFrame(interactiveElementsFrame: Frame | ttk.Frame,
                                 candidateName: str):
            ID = candidateName.split(' - ')[0]
            print(ID)
            ttk.Button(interactiveElementsFrame,
                       text=f'Open CV {candidateName}',
                       style='Buttons.TButton',
                       command=lambda: CVEditorWindow(mode, int(ID))).grid(row=0, column=0)

        interactiveFrameOperations = lambda frame, name: EditInteractiveFrame(frame, name)

        # Makes the interactive, hoverable list.
        HoverableListMaker(canvasFrame, [f'{k} - {v}' for k, v in OwnedCVs.items()], interactiveFrameOperations)

        ttk.Label(mainframe, text=f'Your owned CVs' if mode == 'edit' else f'{user}\'s owned CVs',
                  justify='left',
                  style='Headings.TLabel').grid(row=0, column=0, sticky='W', padx=8)

        WindowSizingTask(CVManagerWindow)

        # Code to prevent permanent focus steal by widgets.
        BindFamily(CVManagerWindow, '<Button-1>', lambda e: CVManagerWindow.focus_set(), bindInteractives=False)
