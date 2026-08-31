from tkinter import *
from tkinter import ttk, messagebox
from GUITools import WindowSizingTask, BindFamily, LabelledListMaker
from DBTools import *

def UserDetailsWindow(username: str):
    userDetailsWindow = Toplevel()
    userDetailsWindow.grab_set()
    userDetailsWindow.focus_set()
    userDetailsWindow.columnconfigure(0, weight=1)
    userDetailsWindow.rowconfigure(0, weight=1)
    userDetailsWindow.title('User Details')

    mainframe = ttk.Frame(userDetailsWindow)
    mainframe.grid(column=0, row=0, sticky='N W E S')

    # Retrieve user details.
    keys = ('firstName', 'lastName', 'email', 'designation', 'DOB', 'DOJoining')
    details = RetrieveUserDetails(username)
    values = tuple(details.values())

    labels = ("First Name: ", "Last Name: ", "Email: ", "Designation: ", "Date of Birth: ", "Date of Joining: ")
    ttk.Label(mainframe,
              text=f"{username}'s Details:",
              justify='left',
              style='Sub-headings.TLabel').grid(column=0, row=0, sticky='W', padx=8)

    listFrame = ttk.Frame(mainframe)
    listFrame.grid(row=1, column=0, sticky='NWES')

    def SubmitData(values: tuple):
        details = {k:v for k, v in zip(keys, values)}
        print(details)
        elementValidities = tuple(IsValueValid(k, v) for k, v in details.items())
        if all(i == 'success' for i in elementValidities):
            operationResult = UpdateUserDetails(username, {k: v for k, v in details.items()})
            if operationResult == 'success':
                messagebox.showinfo('Success!', 'User details updated successfully!', parent=mainframe)
            else:
                messagebox.showerror('Error', operationResult, parent=mainframe)
        else:
            messagebox.showerror('Error', '\n'.join(i for i in elementValidities if i != 'success'), parent=mainframe)

    LabelledListMaker(listFrame, labels, values, mode='edit', valueHandler=lambda values: SubmitData(values))

    WindowSizingTask(userDetailsWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(userDetailsWindow, '<Button-1>', lambda e: userDetailsWindow.focus_set(), bindInteractives=False)