from tkinter import *
from tkinter import ttk
from typing import Callable
from ttk_text import ThemedText

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

# Function to bind an event to all members of a widget tree with a given lambda.
def BindFamily(parent: Widget | Toplevel | Tk,
               event: str,
               operation: Callable[[Event], None],
               bindInteractives: bool = True):
    if bindInteractives:
        parent.bind(event, operation)
        for child in parent.winfo_children():
            child.bind(event, operation)
            BindFamily(child, event, operation)
    else:
        interactives = (ttk.Button, ttk.Entry, ttk.Scrollbar, ttk.Scale, ttk.Combobox, ttk.Checkbutton, ttk.Radiobutton)
        parent.bind(event, operation)
        for child in parent.winfo_children():
            if not isinstance(child, interactives):
                child.bind(event, operation)
            BindFamily(child, event, operation, False)

# Function to make hoverable, interactive lists.
def HoverableListMaker(container: Toplevel | Tk | Frame | ttk.Frame,
                       names: list | tuple,
                       interactiveFrameOperations: Callable[[Frame | ttk.Frame, str], None]):
    # Modifiable widget that supports scrolling, etc.
    canvas = Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
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
        def BindHover(elementFrame):
            hovered = False

            def OnEnter(event):
                nonlocal hovered
                hovered = True

                for child in elementFrame.winfo_children():
                    if isinstance(child, ttk.Frame):
                        child.grid(column=1, row=0, sticky="NSE")

            def OnLeave(event):
                nonlocal hovered
                hovered = False

                def Check():
                    if not hovered:
                        for child in elementFrame.winfo_children():
                            if isinstance(child, ttk.Frame):
                                child.grid_remove()

                elementFrame.after(50, Check)

            BindFamily(elementFrame, "<Enter>", OnEnter)
            BindFamily(elementFrame, "<Leave>", OnLeave)

        BindHover(elementFrame)


def DropdownListMaker(container, listTitle, elements, mode='edit'):
    dropdownListFrame = ttk.Frame(container, padding=8)
    dropdownListFrame.grid(row=0, column=0, sticky="NSEW")
    dropdownListFrame.columnconfigure(0, weight=1)

    listElementsFrame = ttk.Frame(dropdownListFrame)
    listElementsFrame.grid(row=1, column=0, sticky="NSEW")
    listElementsFrame.grid_remove()

    listIsHidden = True
    buttonText = StringVar()
    buttonText.set('▶')

    def ToggleList():
        if listIsHidden:
            listElementsFrame.grid(row=1, column=0, sticky="NSEW")
            buttonText.set('▼')
        else:
            listElementsFrame.grid_remove()
            buttonText.set('▶')

    ttk.Label(dropdownListFrame, text=listTitle).grid(column=0, row=0, sticky="W")
    visibilityButton = ttk.Button(dropdownListFrame, textvariable=buttonText, command=ToggleList)
    visibilityButton.grid(column=1, row=0, sticky="W")

    if mode == 'view':
        for i in elements:
            ttk.Label(listElementsFrame, text=i).grid(column=0, row=i, sticky="W")
    elif mode == 'edit':
        for i in elements:
            pass


def LabelledListMaker(container, fields, mode='edit', valueHandler=None): # Labels need to have the colon and space.
    if mode == 'edit' and valueHandler is None:
        raise TypeError('LabelledListMaker() is missing required argument valueHandler while in edit mode.')

    if not all(field.get('label') and field.get('value') for field in fields):
        raise ValueError('Both labels and values are mandatory for every field.')

    labelledListFrame = ttk.Frame(container, padding=8)
    labelledListFrame.grid(row=0, column=0, sticky="NSEW")

    viewElementsFrame = ttk.Frame(labelledListFrame)
    viewElementsFrame.grid(row=0, column=0, sticky="NSEW")

    labelVars = []

    for key, fieldDefinition in fields:
        label = fieldDefinition['label']
        value = fieldDefinition['value']

        labelVar = StringVar()
        labelVar.set(f'{label}{value}')
        labelVars.append(labelVar)
        ttk.Label(viewElementsFrame, textvariable=labelVar, style='Body.TLabel').pack(anchor='w', pady=5)

    if mode == 'edit':
        editElementsFrame = ttk.Frame(labelledListFrame)
        editElementsFrame.grid(row=0, column=0, sticky="NSEW")
        editElementsFrame.grid_remove()

        entryVars = []

        for key, fieldDefinition in fields:
            label = fieldDefinition['label']
            value = fieldDefinition['value']

            elementFrame = ttk.Frame(editElementsFrame)
            ttk.Label(elementFrame,
                      text=f'{label}',
                      style='Body.TLabel').grid(row=0, column=0, sticky="W")

            entryVar = StringVar()
            entryVars.append(entryVar)
            entryVar.set(f'{value}')

            ttk.Entry(elementFrame,
                      textvariable=entryVar,
                      font=('Aptos', 16)).grid(column=1, row=0, sticky='W')

            elementFrame.pack(anchor='w', pady=5)

        buttonText = StringVar()
        buttonText.set('Edit')

        currentMode = 'view'

        def ToggleListMode():
            nonlocal currentMode

            if currentMode == 'view':
                buttonText.set('Submit')
                editElementsFrame.grid(row=0, column=0, sticky="NSEW")
                viewElementsFrame.grid_remove()
                currentMode = 'edit'
            else:
                buttonText.set('Edit')
                viewElementsFrame.grid(row=0, column=0, sticky="NSEW")
                editElementsFrame.grid_remove()
                for labelVar, label, entryVar in zip(labelVars, labels, entryVars):
                    labelVar.set(f'{label}{entryVar.get()}')
                valueHandler(i.get() for i in entryVars)
                currentMode = 'view'

        ttk.Button(labelledListFrame,
                   textvariable=buttonText,
                   command=ToggleListMode,
                   style='Buttons.TButton').grid(row=1, column=0, sticky='W', pady=(3,0))

        BindFamily(container, '<Return>', lambda e: ToggleListMode())