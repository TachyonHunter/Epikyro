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
    scrollableFrame = ttk.Frame(canvas, padding=5) # The frame to scroll through.
    scrollableFrame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")) # Reconfigures the window when needed.
    )
    canvasWindow = canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

    def resizeScrollableFrame(event):
        canvas.itemconfig(canvasWindow, width=event.width)

    canvas.bind("<Configure>", resizeScrollableFrame)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    scrollbar.pack(side="right", fill="y", padx=5, pady=5)

    # Defining actions to perform on hovers, etc.
    def MakeEnterLambda(frame):
        return lambda e: OnEnter(frame)

    def MakeLeaveLambda(frame):
        return lambda e: OnLeave(frame)

    def OnEnter(frame):
        frame.hovered = True
        for child in frame.winfo_children():
            if isinstance(child, ttk.Frame):
                child.grid(column=1, row=0, sticky="NSE")

    def OnLeave(frame):
        frame.hovered = False

        def check():
            if not frame.hovered:
                for child in frame.winfo_children():
                    if isinstance(child, ttk.Frame):
                        child.grid_remove()

        frame.after(50, check)

    # Function to bind an event to all children of a widget with a given lambda.
    def BindAllChildren(widget, command, lambdaCallable):
        for child in widget.winfo_children():
            child.bind(command, lambdaCallable)
            BindAllChildren(child, command, lambdaCallable)

    # Creating a sub-frame for every user.
    for i in users:
        borderFrame = Frame(scrollableFrame, bg="#e5e5e5", height=60, padx=1, pady=1)
        borderFrame.pack_propagate(False)

        elementFrame = Frame(borderFrame, padx=5, pady=5)
        elementFrame.columnconfigure(0, weight=1)
        elementFrame.rowconfigure(0, weight=1)

        # Username.
        ttk.Label(elementFrame, text=i, font=('Aptos', 16)).grid(column=0, row=0, sticky="W")

        # Frame with all buttons that perform actions.
        interactiveElementsFrame = ttk.Frame(elementFrame)
        interactiveElementsFrame.grid(column=1, row=0, sticky="E")
        interactiveElementsFrame.grid_remove()

        interactiveElementsFrame.rowconfigure(0, weight=1)
        ttk.Button(interactiveElementsFrame, text="Edit User Details", style='Buttons.TButton').grid(row=0, column=0, sticky='E')
        ttk.Button(interactiveElementsFrame, text="Delete User", style='Buttons.TButton').grid(row=0, column=1, sticky='E')
        elementFrame.pack(fill="both", expand=True, padx=1, pady=1)
        borderFrame.pack(fill="x", pady=5)

        # Binding mouse enter and leave events.
        BindAllChildren(borderFrame, "<Enter>", MakeEnterLambda(elementFrame))
        BindAllChildren(borderFrame, "<Leave>", MakeLeaveLambda(elementFrame))

    userEditWindow.mainloop()