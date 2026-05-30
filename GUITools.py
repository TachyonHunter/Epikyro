from tkinter import *
from tkinter import ttk

# Function to give .geometry() formatted window instructions.
def WindowSizer(window, windowWidth, windowHeight):
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = (screenWidth // 2) - (windowWidth // 2)
    y = (screenHeight // 2) - (windowHeight // 2)
    return f"{windowWidth}x{windowHeight}+{x}+{y}"

# Function to bind an event to all children of a widget with a given lambda.
def BindAllChildren(widget, command, operationLambda, bindInteractives=True):
    if bindInteractives:
        for child in widget.winfo_children():
            child.bind(command, operationLambda)
            BindAllChildren(child, command, operationLambda)
    else:
        interactives = (ttk.Button, ttk.Entry, ttk.Scrollbar, ttk.Scale, ttk.Combobox, ttk.Checkbutton, ttk.Radiobutton)
        for child in widget.winfo_children():
            if not isinstance(child, interactives):
                child.bind(command, operationLambda)
                BindAllChildren(child, command, operationLambda, False)

# Function to make hoverable, interactive lists.
def HoverableListMaker(window, names, interactiveFrameLambda):
    # Modifiable widget that supports scrolling, etc.
    canvas = Canvas(window)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollableFrame = ttk.Frame(canvas, padding=5)  # The frame to scroll through.
    scrollableFrame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))  # Reconfigures the window when needed.
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

        def Check():
            if not frame.hovered:
                for child in frame.winfo_children():
                    if isinstance(child, ttk.Frame):
                        child.grid_remove()

        frame.after(50, Check)

    # Creating a sub-frame for every user.
    for name in names:
        borderFrame = ttk.Frame(scrollableFrame, style='Header/Border.TFrame', height=60, padding=1)
        borderFrame.pack_propagate(False)
        elementFrame = Frame(borderFrame, padx=5, pady=5)
        elementFrame.columnconfigure(0, weight=1)
        elementFrame.rowconfigure(0, weight=1)

        nameLabel = ttk.Label(elementFrame, text=name, style='Body.TLabel')
        nameLabel.grid(column=0, row=0, sticky="W")

        # Frame with all buttons that perform actions.
        interactiveElementsFrame = ttk.Frame(elementFrame)
        interactiveElementsFrame.grid(column=1, row=0, sticky="E")
        interactiveElementsFrame.rowconfigure(0, weight=1)
        interactiveElementsFrame.grid_remove()

        # Lambda editing the interactive frame to add the required elements, etc.
        interactiveFrameLambda(interactiveElementsFrame, name)

        # Packing elements.
        elementFrame.pack(fill="both", expand=True, padx=1, pady=1)
        borderFrame.pack(fill="x", pady=5)

        # Binding mouse enter and leave events.
        BindAllChildren(borderFrame, "<Enter>", MakeEnterLambda(elementFrame))
        BindAllChildren(borderFrame, "<Leave>", MakeLeaveLambda(elementFrame))