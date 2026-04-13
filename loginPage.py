from tkinter import *
from tkinter import ttk
from functools import partial
from login import *

# Creates root.
root = Tk()
root.title('Login')

# Creates mainframe (window, basically).
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky='N W E S')

# Creates the username and password entries (user-input textboxes).
username = StringVar()
password = StringVar()
userNotification = StringVar()
usernameField = Entry(mainframe, textvariable=username)
passwordField = Entry(mainframe, textvariable=password, show='*')
usernameField.grid(row=2, column=0, sticky='N W E S')
passwordField.grid(row=4, column=0, sticky='N W E S')

# Creating labels.
Label(mainframe, text='Login:', font=('Segoe UI', 25)).grid(row=0, column=0, sticky='N W E S')
Label(mainframe, text='Username:', font=('Segoe UI', 13)).grid(row=1, column=0, sticky='N W E S')
Label(mainframe, text='Password:', font=('Segoe UI', 13)).grid(row=3, column=0, sticky='N W E S')

#Function to call our function... Tkinter runs all isolated functions on startup...
def LoginCaller(*args):
    Login(username.get(), password.get(), userNotification)

# Button.
Button(mainframe, text="Login", command=LoginCaller).grid(row=5, column=0, sticky='W')

# The status for the users.
Label(mainframe, textvariable=userNotification).grid(row=6, column=0, sticky='W')
root.bind("<Return>", LoginCaller)

root.mainloop()