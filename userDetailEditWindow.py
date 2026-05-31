from tkinter import *
from tkinter import ttk, messagebox
from GUITools import WindowSizer, BindAllChildren
from DBTools import *

def UserDetailsWindow(username):
    userDetailsWindow = Toplevel()
    userDetailsWindow.grab_set()
    userDetailsWindow.focus_set()
    userDetailsWindow.columnconfigure(0, weight=1)
    userDetailsWindow.rowconfigure(0, weight=1)
    userDetailsWindow.title('User Details')
    desiredWidth, desiredHeight = 570, 345
    userDetailsWindow.geometry(WindowSizer(userDetailsWindow, desiredWidth, desiredHeight))

    mainframe = ttk.Frame(userDetailsWindow, padding=8)
    mainframe.grid(column=0, row=0, sticky='N W E S')

    # Retrieve user details.
    keys = ('firstName', 'lastName', 'email', 'designation', 'DOB', 'DOJoining')
    details = {k: StringVar(value=v) for k, v in RetrieveUserDetails(username).items()}

    texts = ("First Name: ", "Last Name: ", "Email: ", "Designation: ", "Date of Birth: ", "Date of Joining: ")
    labelTexts = dict(zip(keys, texts))
    ttk.Label(mainframe, text=f"{username}'s Details:", justify='left', style='Sub-headings.TLabel').grid(column=0, row=0, sticky='W')

    # Functions to switch between viewing and editing details.
    def ActivateEditMode():
        detailFrame.grid_remove()
        editFrame.grid(row=1, column=0, sticky='W')

    def DeactivateEditMode():
        editFrame.grid_remove()
        detailFrame.grid(row=1, column=0, sticky='W')

        operationResult = UpdateUserDetails(username, {k: v.get() for k, v in details.items()})
        if operationResult == 'success':
            messagebox.showinfo('Success!', 'User details updated successfully!')
        else:
            messagebox.showerror('Error', operationResult)

        # For loop updating all the labels for the details.
        for k, v in RetrieveUserDetails(username).items():
            labelTextVars[k].set(f"{labelTexts[k]}{v}")

    # Frame for view mode.
    detailFrame = ttk.Frame(mainframe)
    detailFrame.grid(row=1, column=0, sticky='W')
    labelTextVars = {k: StringVar(value=f"{labelTexts[k]}{v.get()}") for k, v in details.items()}
    for i, (k, v) in enumerate(details.items()):
        ttk.Label(detailFrame, textvariable=labelTextVars[k], style='Body.TLabel', justify='left').grid(column=0, row=i, sticky='W')

    ttk.Button(detailFrame, text='Edit details', style='Buttons.TButton', command=ActivateEditMode).grid(column=0, row=6, sticky='W')

    # Frame for edit mode.
    editFrame = ttk.Frame(mainframe)
    editFrame.grid(row=1, column=0, sticky='W')
    for i, (k, v) in enumerate(details.items()):
        element = ttk.Frame(editFrame)
        element.grid(row=i, column=0, sticky='W', pady=8)
        ttk.Label(element, text=labelTexts[k], style='Body.TLabel', justify='left').grid(column=0, row=0, sticky='W', padx=(0, 4))
        ttk.Entry(element, textvariable=v, font=('Aptos', 16)).grid(column=1, row=0, sticky='W')

    ttk.Button(editFrame, text='Save Details', style='Buttons.TButton', command=DeactivateEditMode).grid(column=0, row=6, sticky='W')
    editFrame.grid_remove()

    # Code to prevent permanent focus steal by widgets.
    BindAllChildren(userDetailsWindow, '<Button-1>', lambda e: userDetailsWindow.focus_set(), bindInteractives=False)