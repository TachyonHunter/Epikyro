from tkinter import *
from tkinter import ttk
import sv_ttk

def SetupStyles(theme: str):
    styleEngine = ttk.Style()
    if theme == "light":
        sv_ttk.set_theme("light")
        styleEngine.configure("Header/Border.TFrame",
                              background="#f0f0f0")
    elif theme == "dark":
        sv_ttk.set_theme("dark")
        styleEngine.configure("Header/Border.TFrame",
                              background="#252525")

    styleEngine.configure("Buttons.TButton",
                          font=("Aptos", 16))

    styleEngine.configure("Headings.TLabel",
                          font=("Aptos", 56))

    styleEngine.configure("Sub-headings.TLabel",
                          font=("Aptos", 32))

    styleEngine.configure("Sub-sub-headings.TLabel",
                          font=("Aptos", 22))

    styleEngine.configure("Body Titles.TLabel",
                          font=("Aptos", 18))

    styleEngine.configure("Body.TLabel",
                          font=("Aptos", 16))

    styleEngine.configure("HeaderText.TLabel",
                          font=("Aptos", 18))