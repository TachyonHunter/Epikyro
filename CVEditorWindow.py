from tkinter import *
from tkinter import ttk, messagebox
from GUITools import WindowSizingTask, BindFamily, LabelledListMaker, ScrollableFrameMaker
from CVTools import *
from DBTools import IsValueValid
from main import sessionStateVars
from tagManagerWindow import TagManagerWindow


def CVEditorWindow(mode, eventHub, ID: int | None = None):
    CVEditorWindow = Toplevel()
    CVEditorWindow.focus_set()
    CVEditorWindow.state('zoomed')
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
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(1, weight=1)

    # Retrieve CV.
    details = GetExistingCV(ID) if mode != 'create' else {}
    ttk.Label(mainframe,
              text=f"CV {ID}" if ID is not None else "Create CV:",
              justify='left',
              style='Sub-headings.TLabel').grid(column=0, row=0, sticky='W')

    def EducationTipCreator(container):
        educationTipFrame = ttk.Frame(container)
        ttk.Label(educationTipFrame,
                  text='Kindly format educational qualifications as:\nDegree - Institution - Year',
                  style='Body.TLabel', justify='left').grid(column=0, row=0, sticky='W', padx=(0, 4))
        ttk.Label(educationTipFrame,
                  text='eg: Class 12 - CBSE - 2020',
                  style='Body.TLabel', justify='left').grid(column=0, row=1, sticky='W', padx=(0, 4))
        return educationTipFrame

    def WorkExpTipCreator(container):
        workExpTipFrame = ttk.Frame(container)
        ttk.Label(workExpTipFrame,
                  text='Kindly format work experience as:\nPosition - Organization - Tenure (start-end)',
                  style='Body.TLabel', justify='left').grid(column=0, row=0, sticky='W', padx=(0, 4))
        ttk.Label(workExpTipFrame,
                  text='eg: Scientist - Microsoft - 2020-2021',
                  style='Body.TLabel', justify='left').grid(column=0, row=1, sticky='W', padx=(0, 4))
        return workExpTipFrame

    def GenericTipCreator(container):
        genericTipFrame = ttk.Frame(container)
        ttk.Label(genericTipFrame,
                  text='Kindly keep descriptions brief.',
                  style='Body.TLabel', justify='left').grid(column=0, row=0, sticky='W', padx=(0, 4))
        return genericTipFrame

    def ReferenceTipCreator(container):
        referenceTipFrame = ttk.Frame(container)
        ttk.Label(referenceTipFrame,
                  text='Kindly format work experience as:\nPerson\nPosition, Organization\nMode of contact',
                  style='Body.TLabel', justify='left').grid(column=0, row=0, sticky='W', padx=(0, 4))
        ttk.Label(referenceTipFrame,
                  text='eg: Dr. Williamson S. Theodore\nHead of R&D, Microsoft\nwilliamson_synthesis@gmail.com',
                  style='Body.TLabel', justify='left').grid(column=0, row=1, sticky='W', padx=(0, 4))
        return referenceTipFrame

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
            'elementType': 'dropdown-multi-line',
            'tipCreator': lambda container: EducationTipCreator(container)
        },
        'workExperience': {
            'label': 'Work Experience: ',
            'value': details['workExperience'] if mode != 'create' else ('',),
            'elementType': 'dropdown-multi-line',
            'tipCreator': lambda container: WorkExpTipCreator(container)
        },
        'miscAchievements': {
            'label': 'Achievements: ',
            'value': details['miscAchievements'] if mode != 'create' else ('',),
            'elementType': 'dropdown-multi-line',
            'tipCreator': lambda container: GenericTipCreator(container)
        },
        'skills': {
            'label': 'Skills: ',
            'value': details['skills'] if mode != 'create' else ('',),
            'elementType': 'dropdown-multi-line',
            'tipCreator': lambda container: GenericTipCreator(container)
        },
        'languages': {
            'label': 'Languages: ',
            'value': details['languages'] if mode != 'create' else ('',),
            'elementType': 'dropdown-single-line'
        },
        'references': {
            'label': 'References: ',
            'value': details['references'] if mode != 'create' else ('',),
            'elementType': 'dropdown-multi-line',
            'tipCreator': lambda container: ReferenceTipCreator(container)
        }
    }

    account = sessionStateVars['account']

    def SubmitData(details):
        if mode == 'create':
            operationResult = CreateNewCV(account, details)
        elif mode == 'edit':
            details['owner'] = account
            operationResult = UpdateExistingCV(ID, details)
        else:
            raise ValueError(f'Why is submit being called in mode {mode}?')

        if operationResult == 'success':
            messagebox.showinfo('Success!',
                                'CV added successfully!' if mode == 'create' else 'Changes submitted!',
                                parent=mainframe)
            if mode == 'create':
                eventHub.event_generate("<<CVCreated>>")
            TagManagerWindow(details)
        else:
            messagebox.showerror('Error', operationResult, parent=mainframe)

        if mode == 'create':
            CVEditorWindow.destroy()

    listFrame = ttk.Frame(mainframe)
    listFrame.grid(column=0, row=1, sticky='NSEW')
    scrollableFrame = ScrollableFrameMaker(listFrame)

    if mode != 'view':
        LabelledListMaker(scrollableFrame,
                          fields,
                          mode,
                          valueHandler=lambda details: SubmitData(details))
    else:
        LabelledListMaker(scrollableFrame, fields, mode)

    WindowSizingTask(CVEditorWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(CVEditorWindow,
               '<Button-1>',
               lambda e: CVEditorWindow.focus_set(),
               bindInteractives=False,
               bindParent=False)