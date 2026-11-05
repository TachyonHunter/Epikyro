from tkinter import *
from tkinter import ttk, messagebox
from GUITools import *
from CVTools import *
from DBTools import IsValueValid
from main import sessionStateVars

def TagManagerWindow(details):
    newTags = GenerateTags(details)
    try:
        currentTags = GetTags(details['ID'])
    except ValueError:
        currentTags = None
    if newTags == currentTags:
        return

    tagManagerWindow = Toplevel()
    tagManagerWindow.focus_set()
    tagManagerWindow.state('zoomed')
    tagManagerWindow.columnconfigure(0, weight=1)
    tagManagerWindow.rowconfigure(0, weight=1)
    tagManagerWindow.title('Tags')

    mainframe = ttk.Frame(tagManagerWindow)
    mainframe.grid(column=0, row=0, sticky='N W E S')
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(2, weight=1)

    ttk.Label(mainframe,
              text='Manage Tags: ',
              justify='left',
              style='Headings.TLabel').grid(row=0, column=0, sticky='W', padx=8)
    ttk.Label(mainframe,
              text='Kindly check if all these tag values are as per your expectations.',
              justify='left',
              style='Body Titles.TLabel').grid(row=1, column=0, sticky='W', padx=8)

    fields = {
        'name': {
            'label': 'Name: ',
            'value': newTags['name'],
        },
        'address': {
            'label': 'Address: ',
            'value': newTags['address'],
        },
        'nationality': {
            'label': 'Nationality: ',
            'value': newTags['nationality'],
        },
        'eduMagnitude': {
            'label': 'No. of educational qualifications: ',
            'value': newTags['eduMagnitude'],
        },
        'totalWorkExperience': {
            'label': 'Total years worked: ',
            'value': newTags['totalWorkExperience']
        },
        'degrees': {
            'label': 'Degrees: ',
            'value': newTags['degrees'],
            'elementType': 'dropdown-single-line'
        },
        'organizations': {
            'label': 'Organizations worked in: ',
            'value': newTags['organizations'],
            'elementType': 'dropdown-single-line'
        },
        'skills': {
            'label': 'Skills: ',
            'value': newTags['skills'],
            'elementType': 'dropdown-single-line'
        },
        'languages': {
            'label': 'Spoken languages: ',
            'value': newTags['languages'],
            'elementType': 'dropdown-single-line'
        },
        'achievements': {
            'label': 'Achievements: ',
            'value': newTags['achievements'],
            'elementType': 'dropdown-single-line'
        }
    }

    def SubmitData():
        values = getter()
        newTags['name'] = values['name']
        newTags['address'] = values['address']
        newTags['nationality'] = values['nationality']
        newTags['eduMagnitude'] = int(values['eduMagnitude'])
        newTags['degrees'] = values['degrees']
        newTags['totalWorkExperience'] = int(values['totalWorkExperience'])
        newTags['organizations'] = values['organizations']
        newTags['skills'] = values['skills']
        newTags['languages'] = values['languages']
        newTags['achievements'] = values['achievements']

        if currentTags is None:
            operationResult = CreateTags(newTags)
        else:
            operationResult = UpdateTags(newTags)

        if operationResult == 'success':
            messagebox.showinfo('Success!',
                                'Tags updated!' if currentTags is None else 'Changes submitted!',
                                parent=mainframe)
        else:
            messagebox.showerror('Error', operationResult, parent=mainframe)
            return

        tagManagerWindow.destroy()

    listFrame = ttk.Frame(mainframe)
    listFrame.grid(column=0, row=2, sticky='NSEW')
    scrollableFrame = ScrollableFrameMaker(listFrame)

    getter = LabelledListMaker(scrollableFrame,
                               fields,
                         'edit-core')

    ttk.Button(scrollableFrame,
              text='Submit',
              command=SubmitData,
              style='Buttons.TButton').grid(row=1, column=0, sticky='W', pady=(3, 0))

    WindowSizingTask(tagManagerWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(tagManagerWindow,
               '<Button-1>',
               lambda e: tagManagerWindow.focus_set(),
               bindInteractives=False,
               bindParent=False)