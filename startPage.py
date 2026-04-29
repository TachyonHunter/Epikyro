from tkinter import *
from tkinter import ttk
from functools import partial
from loginPage import LoginWindow
from styling import SetupStyles

# Creates root.
root = Tk()
root.title('Start-up')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
styles = SetupStyles()

# Creates mainframe (window, basically).
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky='N W E S')

# Makes the column and rows+titleFrame+headerFrame take up max. possible space.
mainframe.columnconfigure(0, weight=1, minsize=0)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=1)
mainframe.rowconfigure(3, weight=1)

#Makes the stuff in titleFrame take up max. possible space.
titleFrame = ttk.Frame(mainframe, padding="3 3 12 12")
titleFrame.grid(column=0, row=1, sticky='N W E S')
titleFrame.columnconfigure(0, weight=1)

# The text.
ttk.Label(titleFrame, text='Epikyro', font=('Segoe UI', 56)).grid(row=0, column=0)
ttk.Label(titleFrame, text='επικυρώ', font=('Segoe UI', 32)).grid(row=1, column=0)
ttk.Label(titleFrame, text='(ep-ee-kee-ROH)', font=('Segoe UI', 22)).grid(row=2, column=0)
ttk.Label(mainframe, text="""Epikyro is an HR Employee Management System, built to streamline the application and review process for position candidates.
It takes in details from formatted CVs, and stores them in a company-wide database to reference easily.
Epikyro supports a criteria search and grading system, management of a CV database and even interview scheduling.""",
          font=('Segoe UI', 18), wraplength=800).grid(row=2, column=0)
ttk.Label(mainframe, text="""Team members:
- Nathan Nibu John
- Hussain Sameer Ulde
- Adwaiy Chidanandan Ajay""", font=('Segoe UI', 18), justify='left').grid(row=3, column=0, sticky='WS')

# The header.
headerFrame = Frame(mainframe)
headerFrame.grid(column=0, row=0, sticky='N W E S')

def LoginWindowOpener():
    LoginWindow(welcomeNotification, loginButtonText)

welcomeNotification = StringVar()
loginButtonText = StringVar()
loginButtonText.set('Login')
welcomeNotification.set('No user logged in...')
headerFrame.columnconfigure(0, weight=1)
headerFrame.columnconfigure(1, weight=1)
ttk.Label(headerFrame, textvariable=welcomeNotification, font=('Segoe UI', 16)).grid(row=0, column=0, sticky='W')
ttk.Button(headerFrame, textvariable=loginButtonText,  style="Buttons.TButton", command=LoginWindowOpener).grid(row=0, column=1, sticky='E')

root.mainloop()