from tkinter import *
from tkinter import ttk
from login import *
from DBTools import *

def UserEditorWindow():
    userEditWindow = Toplevel()
    userEditWindow.title('Edit Users')

    users = ListUsers()

    # Modifiable widget that supports scrolling, etc.
    canvas = Canvas(userEditWindow)
    scrollbar = ttk.Scrollbar(userEditWindow, orient="vertical", command=canvas.yview)
    scrollableFrame = ttk.Frame(canvas) # The frame to scroll through.
    scrollableFrame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")) # Reconfigures the window when needed.
    )
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Defining actions to perform on hovers, etc.
    def IsInside(event, frame):
        x, y = event.x_root, event.y_root # Coordinates of mouse.
        withinXWidth = frame.winfo_rootx() <= x <= (frame.winfo_rootx() + frame.winfo_width())
        withinYWidth = frame.winfo_rooty() <= y <= (frame.winfo_rooty() + frame.winfo_height())
        return withinXWidth and withinYWidth

    def MakeEnterLambda(frame):
        return lambda e: OnEnter(frame)

    def MakeLeaveLambda(frame):
        return lambda e: OnLeave(frame)

    def OnEnter(frame):
        print('inside')
        for child in frame.winfo_children():
            if isinstance(child, ttk.Frame):
                child.grid(column=1, row=0)

    def OnLeave(frame):
        for child in frame.winfo_children():
            if isinstance(child, ttk.Frame):
                child.grid_remove()

    # Creating a sub-frame for every user.
    for i in users:
        elementFrame = Frame(scrollableFrame, padx=10, pady=10, bd=1, relief="solid")
        ttk.Label(elementFrame, text=i).grid(column=0, row=0, sticky="W")
        interactiveElementsFrame = ttk.Frame(elementFrame)
        interactiveElementsFrame.grid(column=1, row=0, sticky="E")
        interactiveElementsFrame.grid_remove()
        ttk.Button(interactiveElementsFrame, text="Open").grid(row=0, column=0)
        elementFrame.pack(fill="x", pady=5)

        # Binding mouse enter and leave events.
        elementFrame.bind("<Enter>", MakeEnterLambda(elementFrame))
        elementFrame.bind("<Leave>", MakeLeaveLambda(elementFrame))
        for child in elementFrame.winfo_children():
            child.bind("<Enter>", MakeEnterLambda(elementFrame))
            child.bind("<Leave>", MakeLeaveLambda(elementFrame))

    def OnClose():
        userEditWindow.destroy()

    userEditWindow.protocol("WM_DELETE_WINDOW", OnClose)
    userEditWindow.mainloop()

UserEditorWindow()