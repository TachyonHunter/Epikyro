from tkinter import *
from tkinter import ttk
from GUITools import *
from DBTools import *

def UserDetailsWindow(username):
    userDetailsWindow = Toplevel()
    userDetailsWindow.grab_set()
    userDetailsWindow.focus_set()
    userDetailsWindow.columnconfigure(0, weight=1)
    userDetailsWindow.rowconfigure(0, weight=1)
    userDetailsWindow.title('User Details')
    desiredWidth, desiredHeight = 570, 200
    userDetailsWindow.geometry(WindowSizer(userDetailsWindow, desiredWidth, desiredHeight))

    mainframe = ttk.Frame(userDetailsWindow, padding=8)
    mainframe.grid(column=0, row=0, sticky='N W E S')

    firstName, lastName, designation, DOB, DOJoining = RetrieveUserDetails(username)

    ttk.Label(mainframe, text=f"{username}'s Details:", justify='left', style='Sub-headings.TLabel').grid(column=0, row=0)
    ttk.Label(mainframe, text=f"First Name: {firstName}", justify='left', style='Body.TLabel').grid(column=0, row=1, sticky='W')
    ttk.Label(mainframe, text=f"Last Name: {lastName}", justify='left', style='Body.TLabel').grid(column=0, row=2, sticky='W')
    ttk.Label(mainframe, text=f"Designation: {designation}", justify='left', style='Body.TLabel').grid(column=0, row=3, sticky='W')
    ttk.Label(mainframe, text=f"Date of Birth: {DOB}", justify='left', style='Body.TLabel').grid(column=0, row=4, sticky='W')
    ttk.Label(mainframe, text=f"Date of Joining: {DOJoining}", justify='left', style='Body.TLabel').grid(column=0, row=5, sticky='W')

    # Code to prevent permanent focus steal by widgets.
    BindAllChildren(userDetailsWindow, '<Button-1>', lambda e: userDetailsWindow.focus_set(), bindInteractives=False)

    userDetailsWindow.mainloop()