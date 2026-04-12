from tkinter import *
from tkinter import ttk
from login import *

root = Tk()
root.title('Login')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky='N W E S')
username = StringVar()
password = StringVar()
usernameField = Entry(mainframe, textvariable=username)
#tempt