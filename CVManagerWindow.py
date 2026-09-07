from tkinter import *
from tkinter import ttk
from deleteConfirmationWindow import DeleteConfirmationWindow
from CVTools import ListOwnedCVs
from GUITools import HoverableListMaker, BindFamily, WindowSizingTask
from CVEditorWindow import CVEditorWindow

def CVManagerWindow(user: str, eventHub, mode: str = 'edit'):
    if mode not in ('edit', 'view'):
        raise ValueError("Mode parameter must be 'edit' or 'view'.")

    CVManagerWindow = Toplevel()
    CVManagerWindow.title(f'Your owned CVs' if mode == 'edit' else f'{user}\'s owned CVs')
    CVManagerWindow.state('zoomed')
    CVManagerWindow.rowconfigure(1, weight=1)
    CVManagerWindow.columnconfigure(0, weight=1)

    def CreateCVList(eventHub):
        OwnedCVs = ListOwnedCVs(user)

        listFrame = ttk.Frame(CVManagerWindow)
        listFrame.grid(row=1, column=0, sticky='NSEW')

        if OwnedCVs == 'not found':
            ttk.Label(listFrame, text='No CVs associated with you...' if mode == 'edit' else f'No CVs associated with {user}...',
                      style='Sub-headings.TLabel',
                      justify='left').grid(row=1, column=0, sticky='NW', padx=8)

            return listFrame

        else:
            def EditInteractiveFrame(interactiveElementsFrame: Frame | ttk.Frame,
                                     candidateName: str):
                ID = candidateName.split(' - ')[0]
                ttk.Button(interactiveElementsFrame,
                           text=f'Open CV {candidateName}' if mode == 'view' else f'Open CV {candidateName}',
                           style='Buttons.TButton',
                           command=lambda: CVEditorWindow(mode, eventHub, int(ID))).grid(row=0, column=0)
                if mode == 'edit':
                    ttk.Button(interactiveElementsFrame,
                               text=f'Delete CV {candidateName}',
                               style='Buttons.TButton',
                               command=lambda: DeleteConfirmationWindow(candidateName,
                                                                        'CV',
                                                                        eventHub)).grid(row=0, column=1)

            interactiveFrameOperations = lambda frame, name: EditInteractiveFrame(frame, name)

            # Makes the interactive, hoverable list.
            HoverableListMaker(listFrame, [f'{k} - {v}' for k, v in OwnedCVs.items()], interactiveFrameOperations)

            return listFrame

    def RefreshCVList(eventHub, *args):
        nonlocal listFrame
        listFrame.destroy()
        listFrame = CreateCVList(eventHub)

    listFrame = CreateCVList(eventHub)

    headFrame = ttk.Frame(CVManagerWindow)
    headFrame.grid(row=0, column=0, sticky='NSEW')
    headFrame.columnconfigure(0, weight=1)

    ttk.Label(headFrame, text=f'Your owned CVs' if mode == 'edit' else f'{user}\'s owned CVs',
              justify='left',
              style='Headings.TLabel').grid(row=0, column=0, sticky='W', padx=8)
    ttk.Button(headFrame,
               text="Add New CV",
               style='Buttons.TButton',
               command=lambda: CVEditorWindow('create', eventHub)).grid(row=0, column=1, sticky='E', padx=10)
    ttk.Button(headFrame,
               text="Search CVs",
               style='Buttons.TButton',
               )

    WindowSizingTask(CVManagerWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(CVManagerWindow, '<Button-1>', lambda e: CVManagerWindow.focus_set(), bindInteractives=False)

    eventHub.bind('<<CVDeleted>>', lambda e: RefreshCVList(eventHub))
    eventHub.bind('<<CVCreated>>', lambda e: RefreshCVList(eventHub))