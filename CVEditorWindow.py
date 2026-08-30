from tkinter import *
from tkinter import ttk, messagebox
from GUITools import WindowSizingTask, BindAllChildren
from CVTools import *
from DBTools import IsValueValid

def CVEditorWindow(mode, ID: int | None = None):
    CVEditorWindow = Toplevel()
    CVEditorWindow.grab_set()
    CVEditorWindow.focus_set()
    CVEditorWindow.columnconfigure(0, weight=1)
    CVEditorWindow.rowconfigure(0, weight=1)
    if ID is None:
        if mode == 'create':
            CVEditorWindow.title(f'Create CV')
    elif mode == 'view':
        CVEditorWindow.title(f'View CV {ID}')
    elif mode == 'edit':
        CVEditorWindow.title(f'Edit CV {ID}')
    else:
        raise ValueError('Some mode error?')

    mainframe = ttk.Frame(CVEditorWindow, padding=8)
    mainframe.grid(column=0, row=0, sticky='N W E S')

    # Retrieve CV.
    details = GetExistingCV(ID) if mode != 'create' else {}
    ttk.Label(mainframe,
              text=f"CV {ID}" if ID is not None else "Create CV:",
              justify='left',
              style='Sub-headings.TLabel').grid(column=0, row=0, sticky='W')

    texts = ('Name: ',
             'Address: ',
             'Phone no.: ',
             'Nationality: ',
             'Gender: ',
             'Educational Qualifications: ',
             'Work Experience: ',
             'Miscellaneous Achievements: ',
             'Skills: ',
             'Languages: ',
             'References: ')

    print(details)

    displayableDetails = {k:v for k, v in details.items() if k not in ('ID', 'owner')}
    labelTexts = dict(zip(displayableDetails.keys(), texts))

    viewFrame = ttk.Frame(mainframe)
    viewFrame.grid(row=1, column=0, sticky='W')
    labelDisplayTexts = {k: f"{labelTexts[k]}{v}" for k, v in displayableDetails.items()}
    for i, (k, v) in enumerate(displayableDetails.items()):
        ttk.Label(viewFrame,
                  text=labelDisplayTexts[k],
                  style='Body.TLabel',
                  justify='left').grid(column=0, row=i, sticky='W', pady=4)

    WindowSizingTask(CVEditorWindow)

    # Code to prevent permanent focus steal by widgets.
    BindAllChildren(CVEditorWindow, '<Button-1>', lambda e: CVEditorWindow.focus_set(), bindInteractives=False)