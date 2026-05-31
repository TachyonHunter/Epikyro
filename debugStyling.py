from tkinter import *
from tkinter import ttk

def SetupStyles(*args):
    styleEngine = ttk.Style()
    styleEngine.configure("TFrame",
                          background="#ffcccc",
                          borderwidth=2,
                          relief="solid")

    styleEngine.configure("Header/Border.TFrame",
                          background="#252525")

    styleEngine.configure("Buttons.TButton",
                          font=("Aptos", 16),
                          background="#ccccff")

    styleEngine.configure("Headings.TLabel",
                          font=("Aptos", 56),
                          background="#ccffcc")

    styleEngine.configure("Sub-headings.TLabel",
                          font=("Aptos", 32),
                          background="#ccffcc")

    styleEngine.configure("Sub-sub-headings.TLabel",
                          font=("Aptos", 22),
                          background="#ccffcc")

    styleEngine.configure("Body Titles.TLabel",
                          font=("Aptos", 18),
                          background="#ccffcc")

    styleEngine.configure("Body.TLabel",
                          font=("Aptos", 16),
                          background="#ccffcc")

    styleEngine.configure("HeaderText.TLabel",
                          font=("Aptos", 18),
                          background="#ccffcc")