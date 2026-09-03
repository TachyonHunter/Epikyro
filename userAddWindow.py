from tkinter import *
from tkinter import ttk, messagebox
from GUITools import WindowSizingTask, BindFamily, LabelledListMaker
from DBTools import *
from datetime import datetime

def AddUserWindow(eventHub: ttk.Frame | Frame) -> None:
    addUserWindow = Toplevel()
    addUserWindow.focus_set()
    addUserWindow.columnconfigure(0, weight=1)
    addUserWindow.rowconfigure(0, weight=1)
    addUserWindow.title('Add User')

    mainframe = ttk.Frame(addUserWindow, padding=8)
    mainframe.grid(column=0, row=0, sticky='N W E S')
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(1, weight=1)

    ttk.Label(mainframe, text='Add User:', style='Headings.TLabel', justify='left').grid(column=0, row=0, sticky='W')

    def SubmitData(details: dict):
        elementValidities = tuple(IsValueValid(k, v) for k, v in details.items())
        if all(i == 'success' for i in elementValidities):
            operationResult = AddUser({k:v for k, v in details.items()})
            if operationResult == 'success':
                messagebox.showinfo('Success!', 'User added successfully!', parent=mainframe)
                eventHub.event_generate("<<UserAdded>>")
            else:
                messagebox.showerror('Error', operationResult, parent=mainframe)
            addUserWindow.destroy()
        else:
            messagebox.showerror('Error', '\n'.join(i for i in elementValidities if i != 'success'), parent=mainframe)

    def CreatePasswordRuleTip(container):
        passwordRulesFrame = ttk.Frame(container)
        ttk.Label(passwordRulesFrame,
                  text='Password must be greater than 8 characters.',
                  style='Body.TLabel', justify='left').grid(column=0, row=0, sticky='W', padx=(0, 4))
        ttk.Label(passwordRulesFrame,
                  text='Password must contain at least 1 uppercase and 1 lowercase letter.',
                  style='Body.TLabel', justify='left').grid(column=0, row=1, sticky='W', padx=(0, 4))
        ttk.Label(passwordRulesFrame,
                  text='Password must contain at least 1 digit.',
                  style='Body.TLabel', justify='left').grid(column=0, row=2, sticky='W', padx=(0, 4))
        ttk.Label(passwordRulesFrame,
                  text='Password must contain at least 1 special character.',
                  style='Body.TLabel', justify='left').grid(column=0, row=3, sticky='W', padx=(0, 4))

        return passwordRulesFrame

    fields = {
        'username': {
            'label': 'Username: ',
            'value': ''
        },
        'password': {
            'label': 'Password: ',
            'value': '',
            'tipCreator': lambda container: CreatePasswordRuleTip(container),
        },
        'firstName': {
            'label': 'First Name: ',
            'value': ''
        },
        'lastName': {
            'label': 'Last Name: ',
            'value': ''
        },
        'email': {
            'label': 'Email: ',
            'value': ''
        },
        'designation': {
            'label': 'Designation: ',
            'value': '',
        },
        'DOB': {
            'label': 'Date of Birth: ',
            'value': ''
        },
        'DOJoining': {
            'label': 'Date of Joining: ',
            'value': datetime.now().strftime("%d-%m-%Y")
        }
    }

    listFrame = ttk.Frame(mainframe)
    listFrame.grid(column=0, row=1, sticky='NSEW')
    LabelledListMaker(listFrame, fields, mode='create', valueHandler=lambda details: SubmitData(details))

    WindowSizingTask(addUserWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(addUserWindow,
               '<Button-1>',
               lambda e: addUserWindow.focus_set(),
               bindInteractives=False,
               bindParent=False)