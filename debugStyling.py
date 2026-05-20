from tkinter import *
from tkinter import ttk

def SetupStyles():
    debugStyling = ttk.Style()
    debugStyling.configure("TFrame",
                    background="#ffcccc",
                    borderwidth=2,
                    relief="solid")

    debugStyling.configure("TLabel",
                    background="#ccffcc")

    debugStyling.configure("TButton",
                    background="#ccccff")