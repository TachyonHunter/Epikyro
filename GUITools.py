from tkinter import *
from tkinter import ttk
from typing import Callable

# Function to handle window sizing.
def WindowSizingTask(window: Toplevel | Tk,
                     allowUserResizing: bool = True):
    window.update_idletasks()

    windowWidth = window.winfo_reqwidth()
    windowHeight = window.winfo_reqheight()

    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = (screenWidth // 2) - (windowWidth // 2)
    y = (screenHeight // 2) - (windowHeight // 2)

    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

    lastRequiredWidth = None
    lastRequiredHeight = None
    if not allowUserResizing:
        window.resizable(False, False)

    def Resize():
        nonlocal lastRequiredWidth, lastRequiredHeight
        window.update_idletasks()

        reqWidth = window.winfo_reqwidth()
        reqHeight = window.winfo_reqheight()

        window.minsize(reqWidth, reqHeight)

        currentWidth = window.winfo_width()
        currentHeight = window.winfo_height()

        if allowUserResizing:
            newWidth = reqWidth if reqWidth != lastRequiredWidth and currentWidth < reqWidth else currentWidth
            newHeight = reqHeight if reqHeight != lastRequiredHeight and currentHeight < reqHeight else currentHeight

        else:
            newWidth = reqWidth if reqWidth != lastRequiredWidth else currentWidth
            newHeight = reqHeight if reqHeight != lastRequiredHeight else currentHeight

        if (newWidth, newHeight) != (currentWidth, currentHeight):
            window.geometry(f"{newWidth}x{newHeight}")

        lastRequiredWidth = reqWidth
        lastRequiredHeight = reqHeight

        window.after(200, Resize)

    Resize()

# Function to bind an event to all children of a widget with a given lambda.
def BindAllChildren(parent: Widget | Toplevel | Tk,
                    event: str,
                    operation: Callable[[Event], None],
                    bindInteractives: bool = True):
    if bindInteractives:
        for child in parent.winfo_children():
            child.bind(event, operation)
            BindAllChildren(child, event, operation)
    else:
        interactives = (ttk.Button, ttk.Entry, ttk.Scrollbar, ttk.Scale, ttk.Combobox, ttk.Checkbutton, ttk.Radiobutton)
        for child in parent.winfo_children():
            if not isinstance(child, interactives):
                child.bind(event, operation)
            BindAllChildren(child, event, operation, False)

# Function to make hoverable, interactive lists.
def HoverableListMaker(window: Toplevel | Tk | Frame | ttk.Frame,
                       names: list | tuple,
                       interactiveFrameOperations: Callable[[Frame | ttk.Frame, str], None]):
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
        interactiveFrameOperations(interactiveElementsFrame, name)

        # Packing elements.
        elementFrame.pack(fill="both", expand=True, padx=1, pady=1)
        borderFrame.pack(fill="x", pady=5)

        # Binding mouse enter and leave events.
        BindAllChildren(borderFrame, "<Enter>", MakeEnterLambda(elementFrame))
        BindAllChildren(borderFrame, "<Leave>", MakeLeaveLambda(elementFrame))