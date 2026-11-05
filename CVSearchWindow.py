from tkinter import *
from tkinter import ttk, messagebox
from GUITools import *
from CVTools import *
from DBTools import IsValueValid
from main import sessionStateVars

def CVSearchWindow(refreshListLambda):
    CVSearchWindow = Toplevel()
    CVSearchWindow.focus_set()
    CVSearchWindow.state('zoomed')
    CVSearchWindow.columnconfigure(0, weight=1)
    CVSearchWindow.rowconfigure(0, weight=1)
    CVSearchWindow.title('Search for CVs:')

    mainframe = ttk.Frame(CVSearchWindow)
    mainframe.grid(column=0, row=0, sticky='N W E S')
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(2, weight=1)

    ttk.Label(mainframe,
              text='Search for CVs with: ',
              justify='left',
              style='Headings.TLabel').grid(row=0, column=0, sticky='W', padx=8)

    categories = {
        'candidateName': {
            'label': 'Name'
        },
        'address': {
            'label': 'Address'
        },
        'nationality': {
            'label': 'Nationality'
        },
        'eduMagnitude': {
            'label': 'No. of educational qualifications'
        },
        'totalWorkExperience': {
            'label': 'Total years worked'
        },
        'degrees': {
            'label': 'Degrees',
            'type': 'list'
        },
        'organizations': {
            'label': 'Organizations worked',
            'type': 'list'
        },
        'skills': {
            'label': 'Skills',
            'type': 'list'
        },
        'languages': {
            'label': 'Languages',
            'type': 'list'
        },
        'achievements': {
            'label': 'Achievements',
            'type': 'list'
        }
    }

    def Search(criteria):
        if 'eduMagnitude' in criteria.keys():
            criteria['eduMagnitude'] = int(criteria['eduMagnitude'])
        if 'totalWorkExperience' in criteria.keys():
            criteria['totalWorkExperience'] = int(criteria['totalWorkExperience'])

        CVs = SearchForCVs(criteria)
        refreshListLambda(CVs)
        CVSearchWindow.destroy()

    listFrame = ttk.Frame(mainframe)
    listFrame.grid(column=0, row=2, sticky='NSEW')
    scrollableFrame = ScrollableFrameMaker(listFrame)
    getter = CheckboxListMaker(scrollableFrame, categories)

    ttk.Button(scrollableFrame,
               text='Submit',
               command=lambda: Search(getter()),
               style='Buttons.TButton').grid(row=1, column=0, sticky='W', pady=(3, 0))

    WindowSizingTask(CVSearchWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(CVSearchWindow,
               '<Button-1>',
               lambda e: CVSearchWindow.focus_set(),
               bindInteractives=False,
               bindParent=False)