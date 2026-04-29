from tkinter import *
from tkinter import ttk

def SetupStyles():
    projectStyling = ttk.Style()
    projectStyling.configure("Buttons.TButton",
                             font=("Aptos", 16))
    projectStyling.configure("HeaderButtons.TButton",
                             font=("Aptos", 16),
                             background="#e5e5e5")
    projectStyling.configure("HeaderText.TLabel",
                             font=("Aptos", 16),
                             background="#e5e5e5",
                             foreground="black")