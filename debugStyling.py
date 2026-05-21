from tkinter import *
from tkinter import ttk

def SetupStyles():
    projectStyling = ttk.Style()
    projectStyling.configure("TFrame",
                    background="#ffcccc",
                    borderwidth=2,
                    relief="solid")

    projectStyling.configure("TLabel",
                    background="#ccffcc")

    projectStyling.configure("TButton",
                    background="#ccccff")