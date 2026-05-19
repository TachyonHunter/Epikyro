from tkinter import *
from tkinter import ttk
from functools import partial
from loginWindow import LoginWindow
from styling import SetupStyles
from fonts import LoadFont

# Creates root.
LoadFont()
root = Tk()
root.title('Start-up')
root.state('zoomed')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
styles = SetupStyles()

# Creates mainframe.
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky='N W E S')

# Makes the column and rows+titleFrame+headerFrame take up max. possible space.
mainframe.columnconfigure(0, weight=1, minsize=0)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=1)
mainframe.rowconfigure(3, weight=1)

#Makes the stuff in titleFrame take up max. possible space.
titleFrame = ttk.Frame(mainframe)
titleFrame.grid(column=0, row=1, sticky='N W E S')
titleFrame.columnconfigure(0, weight=1)

# The text.
ttk.Label(titleFrame, text='Epikyro', font=('Aptos', 56)).grid(row=0, column=0)
ttk.Label(titleFrame, text='επικυρώ', font=('Aptos', 32)).grid(row=1, column=0)
ttk.Label(titleFrame, text='(ep-ee-kee-ROH)', font=('Aptos', 22)).grid(row=2, column=0)
ttk.Label(mainframe, text="""Epikyro is an HR Employee Management System, built to streamline the application and review process for position candidates.
It takes in details from formatted CVs, and stores them in a company-wide database to reference easily.
Epikyro supports a criteria search and grading system, management of a CV database and even interview scheduling.""",
          font=('Aptos', 18)).grid(row=2, column=0)
ttk.Label(mainframe, text="""Team members:
- Nathan Nibu John
- Hussain Sameer Ulde
- Adwaiy Chidanandan Ajay""", font=('Aptos', 18), justify='left').grid(row=3, column=0, sticky='WS')

# The header.
headerFrame = Frame(mainframe, bg='#e5e5e5')
headerFrame.grid(column=0, row=0, sticky='N W E S')
headerFrame.columnconfigure(0, weight=1)
headerFrame.columnconfigure(2, weight=1)

def LoginWindowOpener():
    LoginWindow(welcomeNotification, loginOrSwitchButtonText, logOutButton, adminFrame, headerFrame, generalFrame)

def LogOut():
    logOutButton.grid_remove()
    loginOrSwitchButtonText.set('Log in')
    welcomeNotification.set('No user logged in...')
    generalFrame.grid_remove()
    adminFrame.grid_remove()

loginOrSwitchButtonText = StringVar()
loginOrSwitchButtonText.set('Log in')
ttk.Button(headerFrame, textvariable=loginOrSwitchButtonText,  style="HeaderButtons.TButton", command=LoginWindowOpener).grid(row=0, column=3, sticky='E', padx=(0,5))

welcomeNotification = StringVar()
welcomeNotification.set('No user logged in...')
ttk.Label(headerFrame, textvariable=welcomeNotification, style="HeaderText.TLabel").grid(row=0, column=0, sticky='W')

logOutButton = ttk.Button(headerFrame, text='Sign out', style="HeaderButtons.TButton", command=LogOut)
logOutButton.grid_remove()

# Frame specifically for admins.
def UserEditWindowOpener():
    pass # Temporary

def UserInspectWindowOpener():
    pass # Temporary

adminFrame = Frame(headerFrame, bg='#e5e5e5')
adminFrame.grid(column=1, row=0, sticky='N W E S')
adminFrame.grid_remove()
ttk.Button(adminFrame, text='Edit users', style="HeaderButtons.TButton", command=UserEditWindowOpener).grid(row=0, column=0, sticky='E')
ttk.Button(adminFrame, text='Inspect users', style="HeaderButtons.TButton", command=UserInspectWindowOpener).grid(row=0, column=1, sticky='E')

# Frame for general users.
def CVManagerWindowOpener():
    pass # Temporary

def InterviewManagerWindowOpener():
    pass # Temporary

generalFrame = Frame(headerFrame, bg='#e5e5e5')
generalFrame.grid(column=1, row=0, sticky='N W E S')
generalFrame.grid_remove()
ttk.Button(generalFrame, text='Manage CVs and Candidates', style="HeaderButtons.TButton", command=CVManagerWindowOpener).grid(row=0, column=0, sticky='E')
ttk.Button(generalFrame, text='Manage Interviews', style="HeaderButtons.TButton", command=InterviewManagerWindowOpener).grid(row=0, column=1, sticky='E')

root.mainloop()