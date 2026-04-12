from tkinter import *
from tkinter import ttk
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
usernameField = Entry(mainframe, textvariable=username)
passwordField = Entry(mainframe, textvariable=password, show='*')
usernameField.grid(row=2, column=2, sticky='N W E S')
passwordField.grid(row=4, column=2, sticky='N W E S')

# Creating labels.
Label(mainframe, text='Login:', font=('Segoe UI', 25)).grid(row=0, column=2, sticky='N W E S')
Label(mainframe, text='Username:', font=('Segoe UI', 13)).grid(row=1, column=2, sticky='N W E S')
Label(mainframe, text='Password:', font=('Segoe UI', 13)).grid(row=3, column=2, sticky='N W E S')
root.mainloop()