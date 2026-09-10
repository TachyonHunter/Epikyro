from tkinter import *
from tkinter import ttk, messagebox
from GUITools import *
from CVTools import *
from DBTools import IsValueValid
from main import sessionStateVars

def TagManagerWindow(details):
    tagManagerWindow = Toplevel()
    tagManagerWindow.focus_set()
    tagManagerWindow.columnconfigure(0, weight=1)
    tagManagerWindow.rowconfigure(0, weight=1)
    tagManagerWindow.title('Tags')

    mainframe = ttk.Frame(tagManagerWindow)
    mainframe.grid(column=0, row=0, sticky='N W E S')

