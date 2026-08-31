from tkinter import *
from tkinter import ttk, messagebox
from GUITools import WindowSizingTask, BindFamily
from DBTools import *
from datetime import datetime

def AddUserWindow(eventHub: ttk.Frame | Frame) -> None:
    addUserWindow = Toplevel()
    addUserWindow.grab_set()
    addUserWindow.focus_set()
    addUserWindow.columnconfigure(0, weight=1)
    addUserWindow.rowconfigure(0, weight=1)
    addUserWindow.title('Add User')

    mainframe = ttk.Frame(addUserWindow, padding=8)
    mainframe.grid(column=0, row=0, sticky='N W E S')

    keys = ('username', 'password', 'firstName', 'lastName', 'email', 'designation', 'DOB', 'DOJoining')
    details = {key: StringVar() for key in keys}

    texts = ("Username: ", "Password: ", "First Name: ", "Last Name: ", "Email: ", "Designation: ", "Date of Birth: ", "Date of Joining Organization: ")
    labelTexts = dict(zip(keys, texts))

    details['DOJoining'].set(datetime.now().strftime("%d-%m-%Y"))

    ttk.Label(mainframe, text='Add User:', style='Headings.TLabel', justify='left').grid(column=0, row=0, sticky='W')

    def AddUserCaller():
        elementValidities = tuple(IsValueValid(k, v.get()) for k, v in details.items())
        if all(i == 'success' for i in elementValidities):
            operationResult = AddUser({k:v.get() for k, v in details.items()})
            if operationResult == 'success':
                messagebox.showinfo('Success!', 'User added successfully!', parent=mainframe)
                eventHub.event_generate("<<UserAdded>>")
            else:
                messagebox.showerror('Error', operationResult, parent=mainframe)
            addUserWindow.destroy()
        else:
            messagebox.showerror('Error', '\n'.join(i for i in elementValidities if i != 'success'), parent=mainframe)

    entryFrame = ttk.Frame(mainframe)
    entryFrame.grid(column=0, row=1, sticky='N W E S')
    for k, v in details.items():
        element = ttk.Frame(entryFrame)
        element.pack(anchor='w', pady=4)
        ttk.Label(element, text=labelTexts[k], style='Body.TLabel', justify='left').pack(side='left', padx=(0, 4), anchor='w')
        entry = ttk.Entry(element, textvariable=v, font=('Aptos', 16))
        entry.pack(side='top', anchor='w')
        if k == 'password':
            passwordRulesFrame = ttk.Frame(element)
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

            passwordRulesFrame.pack(anchor='w')
            passwordRulesFrame.pack_forget()

            BindFamily(element, "<FocusIn>", lambda e: passwordRulesFrame.pack(side='bottom', anchor='w'))
            BindFamily(element, "<FocusOut>", lambda e: passwordRulesFrame.pack_forget())

    ttk.Button(mainframe, text='Confirm', style='Buttons.TButton', command=AddUserCaller).grid(column=0, row=9, sticky='W')

    WindowSizingTask(addUserWindow)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(addUserWindow, '<Button-1>', lambda e: addUserWindow.focus_set(), bindInteractives=False)