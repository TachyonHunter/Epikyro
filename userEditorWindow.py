from tkinter import *
from tkinter import ttk
from login import *
from DBTools import *

def UserEditorWindow():
    userEditWindow = Toplevel()
    userEditWindow.title('Edit Users')
    users = ListUsers()

    canvas = Canvas(userEditWindow)
    scrollbar = ttk.Scrollbar(userEditWindow, orient="vertical", command=canvas.yview)

    scrollableFrame = ttk.Frame(canvas)

    scrollableFrame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")) # Reconfigure the window.
    )

    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for i in range(len(users)):
        item = ttk.Frame(scrollableFrame, padding=10)

        ttk.Label(item, text=users[i]).pack(side="left")
        ttk.Button(item, text="Open").pack(side="right")

        item.pack(fill="x", pady=5)

    def OnClose():
        userEditWindow.destroy()

    userEditWindow.protocol("WM_DELETE_WINDOW", OnClose)
    userEditWindow.mainloop()
UserEditorWindow()