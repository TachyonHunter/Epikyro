from tkinter import *
from tkinter import ttk
import sv_ttk

root = Tk()
root.configure(background="#000000")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sv_ttk.set_theme('dark')

style = ttk.Style()
style.configure('TButton', font=("Arial", 56), background="#252525")
style.configure('TFrame', background="#222222")

mainframe = ttk.Frame(root, style='TFrame')
mainframe.grid(row=0, column=0, sticky="NSEW")
ttk.Button(mainframe, text="Click me!", style='TButton').pack()
root.mainloop()