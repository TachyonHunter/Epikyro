from tkinter import *
from tkinter import ttk, messagebox
from GUITools import WindowSizingTask, BindFamily, LabelledListMaker
from CVTools import *
from DBTools import IsValueValid
from main import sessionStateVars

def CVEditorWindow(mode, eventHub, ID: int | None = None):
    CVEditorWindow = Toplevel()
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



    fields = {
        'name': {
            'label': 'Name: ',
            'value': details['name'] if mode != 'create' else ''
        },
        'address': {
            'label': 'Address: ',
            'value': details['address'] if mode != 'create' else ''
        },
        'phoneNo': {
            'label': 'Phone number: ',
            'value': details['phoneNo'] if mode != 'create' else ''
        },
        'nationality': {
            'label': 'Nationality: ',
            'value': details['nationality'] if mode != 'create' else ''
        },
        'gender': {
            'label': 'Gender: ',
            'value': details['gender'] if mode != 'create' else ''
        },
        'eduQualifications': {
            'label': 'Educational Qualifications: ',
            'value': details['eduQualifications'] if mode != 'create' else ('',),
            'elementType': 'dropdown-multi-line'
        },
        'workExperience': {
            'label': 'Work Experience: ',
            'value': details['workExperience'] if mode != 'create' else ('',),
            'elementType': 'dropdown-multi-line'
        },
        'miscAchievements': {
            'label': 'Achievements: ',
            'value': details['miscAchievements'] if mode != 'create' else ('',),
            'elementType': 'dropdown-multi-line'
        },
        'skills': {
            'label': 'Skills: ',
            'value': details['skills'] if mode != 'create' else ('',),
            'elementType': 'dropdown-multi-line'
        },
        'languages': {
            'label': 'Languages: ',
            'value': details['languages'] if mode != 'create' else ('',),
            'elementType': 'dropdown-single-line'
        },
        'references': {
            'label': 'References: ',
            'value': details['references'] if mode != 'create' else ('',),
            'elementType': 'dropdown-multi-line'
        },
    }

    account = sessionStateVars['account']

    def SubmitData(details):
        elementValidities = tuple(IsValueValid(k, v) for k, v in details.items())
        if all(i == 'success' for i in elementValidities):
            if mode == 'create':
                operationResult = CreateNewCV(account, details)
            elif mode == 'edit':
                operationResult = UpdateExistingCV(details)
            else:
                raise ValueError(f'Why is submit being called in mode {mode}?')

            if operationResult == 'success':
                messagebox.showinfo('Success!', 'User added successfully!', parent=mainframe)
                if mode == 'create':
                    eventHub.event_generate("<<CVCreated>>")
            else:
                messagebox.showerror('Error', operationResult, parent=mainframe)

            if mode == 'create':
                CVEditorWindow.destroy()

        else:
            messagebox.showerror('Error', '\n'.join(i for i in elementValidities if i != 'success'), parent=mainframe)

    listFrame = ttk.Frame(mainframe)
    listFrame.grid(column=0, row=1, sticky='NSEW')
    if mode != 'view':
        LabelledListMaker(listFrame,
                          fields,
                          mode,
                          valueHandler=lambda details: SubmitData(details))
    else:
        LabelledListMaker(listFrame, fields, mode)

    WindowSizingTask(CVEditorWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(CVEditorWindow,
               '<Button-1>',
               lambda e: CVEditorWindow.focus_set(),
               bindInteractives=False,
               bindParent=False)