from tkinter import *
from tkinter import ttk, messagebox
from GUITools import WindowSizer, BindAllChildren
from DBTools import *
import datetime

def AddUserWindow(userEditWindow, refreshListLambda):
    addUserWindow = Toplevel()
    addUserWindow.grab_set()
    addUserWindow.focus_set()
    addUserWindow.columnconfigure(0, weight=1)
    addUserWindow.rowconfigure(0, weight=1)
    addUserWindow.title('Add User')
    desiredWidth, desiredHeight = 570, 375
    addUserWindow.geometry(WindowSizer(addUserWindow, desiredWidth, desiredHeight))

    mainframe = ttk.Frame(addUserWindow, padding=8)
    mainframe.grid(column=0, row=0, sticky='N W E S')

    keys = ('username', 'password', 'firstName', 'lastName', 'email', 'designation', 'DOB', 'DOJoining')
    details = {key: StringVar() for key in keys}

    texts = ("Username: ", "Password: ", "First Name: ", "Last Name: ", "Email: ", "Designation: ", "Date of Birth: ", "Date of Joining Organization: ")
    labelTexts = dict(zip(keys, texts))

    details['DOJoining'].set(datetime.datetime.now().strftime("%d/%m/%Y"))

    def AddUserCaller():
        operationResult = AddUser({k:v.get() for k, v in details.items()})
        if operationResult == 'success':
            messagebox.showinfo('Success!', 'User added successfully!')
            refreshListLambda()
        else:
            messagebox.showerror('Error', operationResult)
        addUserWindow.destroy()

    for i, (k, v) in enumerate(details.items()):
        element = ttk.Frame(mainframe)
        element.grid(row=i, column=0, sticky='W', pady=8)
        ttk.Label(element, text=labelTexts[k], style='Body.TLabel', justify='left').grid(column=0, row=0, sticky='W', padx=(0, 4))
        ttk.Entry(element, textvariable=v, font=('Aptos', 16)).grid(column=1, row=0, sticky='W')

    ttk.Button(mainframe, text='Confirm', style='Buttons.TButton', command=AddUserCaller).grid(column=0, row=8, sticky='W')

    # Code to prevent permanent focus steal by widgets.
    BindAllChildren(addUserWindow, '<Button-1>', lambda e: addUserWindow.focus_set(), bindInteractives=False)