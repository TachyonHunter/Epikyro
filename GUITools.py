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
               bindInteractives: bool = True,
               bindParent: bool = True):

    interactives = (
        ttk.Button,
        ttk.Entry,
        ttk.Scrollbar,
        ttk.Scale,
        ttk.Combobox,
        ttk.Checkbutton,
        ttk.Radiobutton
    )

    if bindParent and (bindInteractives or not isinstance(parent, interactives)):
        parent.bind(event, operation)

    for child in parent.winfo_children():
        BindFamily(
            child,
            event,
            operation,
            bindInteractives,
            True
        )

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


def LabelledListMaker(container,
                      fields,
                      mode,
                      valueHandler=None):
    """
    Makes a Labelled List that can convert into a form if needed.

    Fields has the following format::
        {
            <key>: {
                'label': <label>,
                'value': <value>,
                ['tipCreator': <tipCreationLambda>],
                ['elementType': <elementType>]
            }
        }

    `elementType` can be:
        - 'single-line'
        - 'multi-line'
        - 'dropdown-single-line'
        - 'dropdown-multi-line'

    During creation of the list, the key 'inputHub' is added. Its value is
    an object that contains the inputted data.

    The colon (:), etc. must be provided for the label.
    """

    if mode not in ('view', 'edit', 'create'):
        raise ValueError("Mode must be 'view', 'edit' or 'create'.")

    if mode == 'edit' and valueHandler is None:
        raise TypeError('LabelledListMaker() is missing required argument valueHandler while in edit mode.')

    if not all('label' in fieldDef and 'value' in fieldDef for fieldDef in fields.values()):
        raise ValueError('Both labels and values are mandatory for every field.')

    labelledListFrame = ttk.Frame(container, padding=8)
    labelledListFrame.grid(row=0, column=0, sticky="NSEW")

    viewElementsFrame = ttk.Frame(labelledListFrame)
    viewElementsFrame.grid(row=0, column=0, sticky="NSEW")

    if mode != 'create':
        for key, fieldDef in fields.items():
            label = fieldDef['label']
            value = fieldDef['value']
            ttk.Label(viewElementsFrame, text=f'{label}{value}', style='Body.TLabel').pack(anchor='w', pady=5)

    if mode in ('edit', 'create'):
        editElementsFrame = ttk.Frame(labelledListFrame)
        editElementsFrame.grid(row=0, column=0, sticky="NSEW")
        editElementsFrame.grid_remove()

        inputVars = {}

        def TipCreator(elementFrame, tipDeclaration):
            tipObject = tipDeclaration(elementFrame)
            tipObject.pack(side='bottom', anchor='nw')
            tipObject.pack_forget()

            BindFamily(elementFrame,
                       '<FocusIn>',
                       lambda e: tipObject.pack(side='bottom', anchor='w'))
            BindFamily(elementFrame,
                       "<FocusOut>",
                       lambda e: tipObject.pack_forget())

        for key, fieldDef in fields.items():
            label = fieldDef['label']
            value = fieldDef['value']
            tipCreator = fieldDef.get('tipCreator')
            elementType = fieldDef.get('elementType')

            elementFrame = ttk.Frame(editElementsFrame)
            if elementType == 'single-line' or elementType is None:
                ttk.Label(elementFrame,
                          text=f'{label}',
                          style='Body.TLabel',
                          justify='left').pack(side='left', anchor='w')

                entryVar = StringVar()
                inputVars[key] = entryVar

                fields[key]['inputGetter'] = lambda var=entryVar: var.get()

                entry = ttk.Entry(
                    elementFrame,
                    textvariable=entryVar,
                    font=('Aptos', 16)
                )
                entry.pack(side='top', anchor='nw')

                entryVar.set(value)

                if tipCreator is not None:
                    TipCreator(elementFrame, tipCreator)

                elementFrame.pack(anchor='w', pady=5)

            elif elementType == 'multi-line':
                ttk.Label(elementFrame,
                          text=f'{label}',
                          style='Body.TLabel',
                          justify='left').pack(side='left', anchor='nw')

                textBoxFrame = ttk.Frame(elementFrame)
                textBoxFrame.pack(side='left', anchor='nw')

                textBox = ThemedText(textBoxFrame, width=70, height=20)
                scrollbar = ttk.Scrollbar(textBoxFrame, orient="vertical", command=textBox.yview)

                textBox.configure(yscrollcommand=scrollbar.set)

                textBox.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")

                fields[key]['inputGetter'] = lambda: textBox.get("1.0", "end-1c")
                textBox.insert('1.0', f'{value}')

                if tipCreator is not None:
                    TipCreator(elementFrame, tipCreator)

                elementFrame.pack(anchor='w', pady=5)

        buttonText = StringVar()
        buttonText.set('Edit')

        currentMode = 'view'
        if mode == 'edit':
            def ToggleListMode(*args):
                nonlocal currentMode

                if currentMode == 'view':
                    buttonText.set('Submit')
                    editElementsFrame.grid(row=0, column=0, sticky="NSEW")
                    viewElementsFrame.grid_remove()
                    container.update_idletasks()
                    currentMode = 'edit'
                else:
                    buttonText.set('Edit')
                    viewElementsFrame.grid(row=0, column=0, sticky="NSEW")
                    editElementsFrame.grid_remove()
                    details = {}
                    for key, fieldDef in fields.items():
                        inputGetter = fieldDef.get('inputGetter')
                        details[key] = fields[key]['value'] = inputGetter()

                    valueHandler(details)

                    labelledListFrame.destroy()
                    LabelledListMaker(container, fields, 'edit', valueHandler)

            ttk.Button(labelledListFrame,
                       textvariable=buttonText,
                       command=ToggleListMode,
                       style='Buttons.TButton').grid(row=1, column=0, sticky='W', pady=(3, 0))

        elif mode == 'create':
            editElementsFrame.grid(row=0, column=0, sticky="NSEW")
            def SubmitData():
                details = {}
                for key, fieldDef in fields.items():
                    inputGetter = fieldDef.get('inputGetter')
                    details[key] = fields[key]['value'] = inputGetter()

                valueHandler(details)

            ttk.Button(labelledListFrame,
                       textvariable=buttonText,
                       command=SubmitData,
                       style='Buttons.TButton').grid(row=1, column=0, sticky='W', pady=(3, 0))