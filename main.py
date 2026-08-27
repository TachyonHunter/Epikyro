from tkinter import ttk
from pathlib import Path

iterations=100000
size=16

sessionStateVars = {
    'account':None
}

projectRootFolder = Path(__file__).resolve().parent

def CreateEventHub(root):
    eventHub = ttk.Frame(root)
    return eventHub