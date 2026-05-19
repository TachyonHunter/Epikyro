from tkinter import *
from tkinter import ttk
from login import *

def UserEditorWindow(welcomeNotification, loginOrSwitchButtonText, logOutButton, adminFrame, headerFrame, generalFrame):
    userEditWindow = Toplevel()
    userEditWindow.title('Edit Users')
    # SQL code goes here. In the end, I want a list of usernames, called users.
    users = []


    def OnClose():
        userEditWindow.destroy()

    userEditWindow.protocol("WM_DELETE_WINDOW", OnClose)

    userEditWindow.mainloop()