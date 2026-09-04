from tkinter import *
from tkinter import ttk
from loginWindow import LoginWindow
from userEditorWindow import UserEditorWindow
from inspectEmployeeWindow import InspectEmployeeWindow
from CVManagerWindow import CVManagerWindow
from styling import SetupStyles
# from debugStyling import SetupStyles
from fonts import LoadFont
from GUITools import BindFamily, WindowSizingTask
from main import sessionStateVars, CreateEventHub

# Creates root.
LoadFont()
root = Tk()
eventHub = CreateEventHub(root)
root.title('Start-up')
root.state('zoomed')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mode = 'light'
SetupStyles(mode)

# Creates mainframe.
mainframe = ttk.Frame(root, style='Default.TFrame')
mainframe.grid(column=0, row=0, sticky='N W E S')

# Makes the column and rows+titleFrame+headerFrame take up max. possible space.
mainframe.columnconfigure(0, weight=1, minsize=0)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=1)
mainframe.rowconfigure(3, weight=1)

#Makes the stuff in titleFrame take up max. possible space.
titleFrame = ttk.Frame(mainframe, style='Default.TFrame')
titleFrame.grid(column=0, row=1, sticky='N W E S')
titleFrame.columnconfigure(0, weight=1)

# The text.
ttk.Label(titleFrame, text='Epikyro', style="Headings.TLabel").grid(row=0, column=0)
ttk.Label(titleFrame, text='επικυρώ', style="Sub-headings.TLabel").grid(row=1, column=0)
ttk.Label(titleFrame, text='(ep-ee-kee-ROH)', style="Sub-sub-headings.TLabel").grid(row=2, column=0)
ttk.Label(mainframe, text="""Epikyro is an HR Employee Management System, built to streamline the application and review process for position candidates.
It takes in details from formatted CVs, and stores them in a company-wide database to reference easily.
Epikyro supports a criteria search and grading system, management of a CV database and even interview scheduling."""
          , style="Body Titles.TLabel").grid(row=2, column=0)
ttk.Label(mainframe, text="""Team members:
- Nathan Nibu John
- Hussain Sameer Ulde
- Adwaiy Chidanandan Ajay""", style="Body.TLabel", justify='left').grid(row=3, column=0, sticky='WS')

account = None

# The header.
headerFrame = ttk.Frame(mainframe, style='Header/Border.TFrame', padding=5)
headerFrame.grid(column=0, row=0, sticky='N W E S')
headerFrame.columnconfigure(0, weight=1)

# Frame with all account-related buttons.
accountFrame = ttk.Frame(headerFrame, style='Header/Border.TFrame')
accountFrame.grid(row=0, column=2)

loginButton = ttk.Button(accountFrame, text='Log in',  style="Buttons.TButton", command=lambda: LoginWindow(eventHub))
loginButton.grid(row=0, column=0, sticky='E')

switchAccountButton = ttk.Button(accountFrame, text='Switch account',  style="Buttons.TButton", command=lambda: LoginWindow(eventHub))
switchAccountButton.grid(row=0, column=0, sticky='E', padx=(0,4))
switchAccountButton.grid_remove()

def LogOut():
    logOutButton.grid_remove()
    switchAccountButton.grid_remove()
    loginButton.grid(row=0, column=0, sticky='E')
    welcomeNotification.set('No user logged in...')
    generalFrame.grid_remove()
    adminFrame.grid_remove()

logOutButton = ttk.Button(accountFrame, text='Log out', style="Buttons.TButton", command=LogOut)
logOutButton.grid(row=0, column=1)
logOutButton.grid_remove()

# Welcome notification label.
welcomeNotification = StringVar()
welcomeNotification.set('No user logged in...')
welcomeLabel = ttk.Label(headerFrame, textvariable=welcomeNotification, style="HeaderText.TLabel")
welcomeLabel.grid(row=0, column=0, sticky='W')
welcomeLabel.config(background = ("#f0f0f0" if mode == 'light' else "252525"))

# Frame specifically for admins.
adminFrame = ttk.Frame(headerFrame, style='Header/Border.TFrame')
adminFrame.grid(column=1, row=0, sticky='E')
adminFrame.grid_remove()
ttk.Button(adminFrame, text='Edit users', style="Buttons.TButton", command=lambda: UserEditorWindow(eventHub)).pack(side='left', padx=(0,4))
ttk.Button(adminFrame, text='Inspect users', style="Buttons.TButton", command=lambda: InspectEmployeeWindow(eventHub)).pack(side='right', padx=(0,4))

# Frame for general users.
def CVManagerWindowOpener():
    CVManagerWindow(sessionStateVars['account'], eventHub)

def InterviewManagerWindowOpener():
    pass # Temporary

generalFrame = ttk.Frame(headerFrame, style='Header/Border.TFrame')
generalFrame.grid(column=1, row=0, sticky='N W E S')
generalFrame.grid_remove()
ttk.Button(generalFrame, text='Manage CVs and Candidates', style="Buttons.TButton", command=CVManagerWindowOpener).pack(side='left', padx=(0,4))
ttk.Button(generalFrame, text='Manage Interviews', style="Buttons.TButton", command=InterviewManagerWindowOpener).pack(side='right', padx=(0,4))

# Functions for the account system.
def UpdateOnLogin(accountType):
    welcomeNotification.set(f'Welcome {sessionStateVars['account']}!')
    loginButton.grid_remove()
    switchAccountButton.grid(row=0, column=0, sticky='E', padx=(0, 4))
    logOutButton.grid(row=0, column=1, sticky='E')
    if accountType == 'admin':
        adminFrame.grid(row=0, column=1, sticky='E', padx=(0, 4))
        headerFrame.columnconfigure(1, weight=1)
        generalFrame.grid_remove()
    else:
        generalFrame.grid(row=0, column=1, sticky='E', padx=(0, 4))
        headerFrame.columnconfigure(1, weight=1)
        adminFrame.grid_remove()

eventHub.bind('<<adminLogin>>', lambda e: UpdateOnLogin('admin'))
eventHub.bind('<<normalLogin>>', lambda e: UpdateOnLogin('normal'))

# Light/Dark Mode switcher.
def SwitchMode():
    global mode
    if mode == 'light':
        SetupStyles('dark')
        mode = 'dark'
    elif mode == 'dark':
        SetupStyles('light')
        mode = 'light'
    welcomeLabel.config(background=("#f0f0f0" if mode == 'light' else "#252525"))

ttk.Button(headerFrame, text='Light/Dark Mode', style="Buttons.TButton", command=SwitchMode).grid(row=0, column=3, sticky='E', padx=8)

WindowSizingTask(root)

# Code to prevent permanent focus steal by widgets.
BindFamily(root, '<Button-1>', lambda e: root.focus_set(), bindInteractives=False)

root.mainloop()