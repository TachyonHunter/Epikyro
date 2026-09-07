from tkinter import *
from tkinter import ttk, messagebox
from GUITools import WindowSizingTask, BindFamily, LabelledListMaker
from DBTools import *

def UserDetailsWindow(username: str):
    userDetailsWindow = Toplevel()
    userDetailsWindow.focus_set()
    userDetailsWindow.columnconfigure(0, weight=1)
    userDetailsWindow.rowconfigure(0, weight=1)
    userDetailsWindow.title('User Details')

    mainframe = ttk.Frame(userDetailsWindow)
    mainframe.grid(column=0, row=0, sticky='N W E S')

    # Retrieve user details.
    details = RetrieveUserDetails(username)

    ttk.Label(mainframe,
              text=f"{username}'s Details:",
              justify='left',
              style='Sub-headings.TLabel').grid(column=0, row=0, sticky='W', padx=8)

    listFrame = ttk.Frame(mainframe)
    listFrame.grid(row=1, column=0, sticky='NWES')

    def SubmitData(details: dict):
        operationResult = UpdateUserDetails(username, {k: v for k, v in details.items()})
        if operationResult == 'success':
            messagebox.showinfo('Success!', 'User details updated successfully!', parent=mainframe)
        else:
            messagebox.showerror('Error', operationResult, parent=mainframe)

    fields = {
        'firstName': {
            'label': 'First Name: ',
            'value': details['firstName']
        },
        'lastName': {
            'label': 'Last Name: ',
            'value': details['lastName']
        },
        'email': {
            'label': 'Email: ',
            'value': details['email']
        },
        'designation': {
            'label': 'Designation: ',
            'value': details['designation']
        },
        'DOB': {
            'label': 'Date of Birth: ',
            'value': details['DOB']
        },
        'DOJoining': {
            'label': 'Date of Joining: ',
            'value': details['DOJoining']
        }
    }

    LabelledListMaker(listFrame, fields, mode='edit', valueHandler=lambda details: SubmitData(details))

    WindowSizingTask(userDetailsWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(userDetailsWindow,
               '<Button-1>',
               lambda e: userDetailsWindow.focus_set(),
               bindInteractives=False,
               bindParent=False)