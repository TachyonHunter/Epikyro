from tkinter import *
from tkinter import ttk, font
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
        ThemedText,
        ttk.Scrollbar,
        ttk.Scale,
        ttk.Combobox,
        ttk.Checkbutton,
        ttk.Radiobutton
    )

    if bindParent and (bindInteractives or not isinstance(parent, interactives)):
        parent.bind(event, operation, add='+')

    for child in parent.winfo_children():
        BindFamily(
            child,
            event,
            operation,
            bindInteractives,
            True
        )

def ScrollableFrameMaker(container):
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
    return scrollableFrame

def CollapsibleTextboxMaker(container, content):
    inputFrame = ttk.Frame(container, width=350, height=40)
    inputFrame.grid(column=0, row=0, sticky='W')

    textBoxFrame = ttk.Frame(inputFrame, width=350, height=40)
    textBoxFrame.grid(column=0, row=0)
    textBox = ThemedText(
        textBoxFrame,
        width=30,
        height=3,
        wrap='word'
    )
    textBox.configure(font=('Aptos', 16))
    textBox.insert('1.0', content)
    textBox.grid(row=0, column=0, sticky='NSEW')

    scrollbar = ttk.Scrollbar(textBoxFrame, orient="vertical", command=textBox.yview)
    scrollbar.grid(row=0, column=1, sticky='NS')

    textBox.configure(yscrollcommand=scrollbar.set)

    getter = lambda: textBox.get("1.0", "end-1c")

    def TruncateText(entry,
                     textBox) -> str:

        def GetFirstDisplayLine():
            originalView = textBox.yview()

            textBox.yview_moveto(0)
            textBox.update_idletasks()

            start = textBox.index('1.0')
            startY = textBox.dlineinfo(start)[1]

            index = start

            while True:
                nextIndex = textBox.index(f'{index} + 1 char')

                if nextIndex == textBox.index('end'):
                    end = nextIndex
                    break

                if textBox.dlineinfo(nextIndex)[1] != startY:
                    end = nextIndex
                    break

                index = nextIndex

            firstLine = textBox.get(start, end)

            return firstLine, end

        entry.update_idletasks()
        textBox.update_idletasks()

        textFont = font.Font(family='Aptos', size=16)
        experimentallyDeterminedPadding = 10
        maxWidth = entry.winfo_width() - 2*experimentallyDeterminedPadding

        firstLine, firstLineEnd = GetFirstDisplayLine()

        hasMoreLines = bool(textBox.get(firstLineEnd, 'end-1c').strip())
        suffix = '...' if hasMoreLines else ''

        if textFont.measure(firstLine + suffix) <= maxWidth:
            return firstLine + suffix

        candidate = ''

        for char in firstLine:
            if textFont.measure(candidate + char + '...') > maxWidth:
                break
            candidate += char

        return candidate + '...'

    placeholderText = StringVar()
    placeholderEntry = ttk.Entry(inputFrame,
                                 width=30,
                                 justify='left',
                                 textvariable=placeholderText,
                                 font=('Aptos', 16))
    placeholderEntry.grid(row=0, column=0, sticky='NSEW')
    placeholderText.set(TruncateText(placeholderEntry, textBox))
    textBoxFrame.grid_remove()

    def DecompressText(*args):
        placeholderEntry.grid_remove()
        textBoxFrame.grid()
        inputFrame.configure(height=textBox.winfo_reqheight())
        textBox.focus_set()

    def CompressText(*args):
        placeholderText.set(TruncateText(placeholderEntry, textBox))
        placeholderEntry.grid()
        textBoxFrame.grid_remove()
        inputFrame.configure(height=placeholderEntry.winfo_reqheight())

    placeholderEntry.bind('<FocusIn>', DecompressText)
    textBox.bind('<FocusOut>', CompressText)

    return getter

# Function to make hoverable, interactive lists.
def HoverableListMaker(container: Toplevel | Tk | Frame | ttk.Frame,
                       names: list | tuple,
                       interactiveFrameOperations: Callable[[Frame | ttk.Frame, str], None]):
    scrollableFrame = ScrollableFrameMaker(container)

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

def DropdownListMaker(container,
                      title,
                      elements,
                      mode,
                      elementType):
    if mode not in ('view', 'edit'):
        raise ValueError("Mode must be 'view' or 'edit'.")

    if elementType not in ('single-line', 'multi-line'):
        raise ValueError("ElementType must be 'single-line' or 'multi-line'.")

    dropdownListFrame = ttk.Frame(container)
    dropdownListFrame.pack(side='top', pady=5, anchor='w')
    dropdownListFrame.columnconfigure(0, weight=1)

    titleText = StringVar()
    titleText.set('⏵ '+title)

    titleLabel = ttk.Label(dropdownListFrame,
                           textvariable=titleText,
                           style='Body Titles.TLabel',
                           justify='left')
    titleLabel.grid(column=0, row=0, sticky="W")

    elementsFrame = ttk.Frame(dropdownListFrame)
    elementsFrame.grid(row=1, column=0, sticky="NSEW", padx=8)
    elementsFrame.grid_remove()

    if mode == 'view':
        for i in elements:
            ttk.Label(elementsFrame, text=i, style='Body.TLabel', justify='left').pack(anchor='w', pady=5)

    elif mode == 'edit':
        getters = []

        def DeleteElement(element, getter):
            getters.remove(getter)
            element.destroy()

        if elementType == 'single-line':
            def AddElement(content):
                element = ttk.Frame(elementsFrame)
                entryVar = StringVar()
                entryVar.set(content)
                getter = entryVar.get
                getters.append(getter)

                ttk.Entry(element,
                          textvariable=entryVar,
                          font=('Aptos', 16),
                          justify='left').grid(column=0, row=0, sticky='W')

                ttk.Button(
                    element,
                    text='Remove',
                    style='Buttons.TButton',
                    command=lambda frame=element, getter=getter:
                        DeleteElement(frame, getter)
                ).grid(column=1, row=0, sticky='E', padx=2)

                element.pack(anchor='w', pady=5)

            for i in elements:
                AddElement(i)

        elif elementType == 'multi-line':
            def AddElement(content):
                element = ttk.Frame(elementsFrame)
                getter = CollapsibleTextboxMaker(element, content)
                getters.append(getter)

                ttk.Button(
                    element,
                    text='Remove',
                    style='Buttons.TButton',
                    command=lambda frame=element, getter=getter:
                        DeleteElement(frame, getter)
                ).grid(column=1, row=0, sticky='E', padx=2)

                element.pack(anchor='w', pady=5)

            for i in elements:
                AddElement(i)

        addElementButton = ttk.Button(dropdownListFrame,
                                      text='Add',
                                      style='Buttons.TButton',
                                      command=lambda: AddElement(''))

    isListHidden = True
    def ToggleList(*args):
        nonlocal isListHidden
        if isListHidden:
            elementsFrame.grid(row=1, column=0, sticky="NSEW")
            titleText.set('⏷ ' + title)
            isListHidden = False
            if mode == 'edit':
                addElementButton.grid(column=0, row=2, sticky='W', padx=2)
        else:
            elementsFrame.grid_remove()
            titleText.set('⏵ ' + title)
            isListHidden = True
            if mode == 'edit':
                addElementButton.grid_remove()

    titleLabel.bind('<Button-1>', ToggleList)

    return None if mode == 'view' else lambda: tuple(getter() for getter in getters)

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
    labelledListFrame.columnconfigure(0, weight=1)
    labelledListFrame.rowconfigure(0, weight=1)

    viewElementsFrame = ttk.Frame(labelledListFrame)
    viewElementsFrame.grid(row=0, column=0, sticky="NSEW")

    if mode != 'create':
        for key, fieldDef in fields.items():
            label = fieldDef['label']
            value = fieldDef['value']
            elementType = fieldDef.get('elementType')
            if elementType in ('single-line', 'multi-line') or elementType is None:
                ttk.Label(viewElementsFrame,
                          text=f'{label}{value}',
                          style='Body Titles.TLabel').pack(anchor='w', pady=5)
            elif elementType == 'dropdown-single-line':
                elementFrame = ttk.Frame(viewElementsFrame)
                DropdownListMaker(elementFrame,
                                  label,
                                  value,
                                  mode='view',
                                  elementType='single-line')
                elementFrame.pack(anchor='w', pady=5)
            elif elementType == 'dropdown-multi-line':
                elementFrame = ttk.Frame(viewElementsFrame)
                DropdownListMaker(elementFrame,
                                  label,
                                  value,
                                  mode='view',
                                  elementType='multi-line')
                elementFrame.pack(anchor='w', pady=5)

    if mode in ('edit', 'create'):
        editElementsFrame = ttk.Frame(labelledListFrame)

        inputVars = {}

        def TipCreator(elementFrame, tipDeclaration):
            tipObject = tipDeclaration(elementFrame)
            tipObject.pack(side='bottom', anchor='nw')
            tipObject.pack_forget()

            BindFamily(elementFrame,
                       '<FocusIn>',
                       lambda e: tipObject.pack(side='bottom', anchor='sw'))
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
                primaryFrame = ttk.Frame(elementFrame)
                primaryFrame.pack(anchor='w', side='top')
                ttk.Label(primaryFrame,
                          text=f'{label}',
                          style='Body Titles.TLabel',
                          justify='left').pack(side='left', anchor='nw')

                entryVar = StringVar()
                inputVars[key] = entryVar

                fields[key]['inputGetter'] = lambda var=entryVar: var.get()

                entry = ttk.Entry(
                    primaryFrame,
                    textvariable=entryVar,
                    font=('Aptos', 16)
                )
                entry.pack(side='right', anchor='ne')

                entryVar.set(value)

                if tipCreator is not None:
                    TipCreator(elementFrame, tipCreator)

                elementFrame.pack(anchor='w', pady=5)

            elif elementType == 'multi-line':
                primaryFrame = ttk.Frame(elementFrame)
                primaryFrame.pack(anchor='w', side='top')
                ttk.Label(primaryFrame,
                          text=f'{label}',
                          style='Body Titles.TLabel',
                          justify='left').pack(side='left', anchor='nw')

                textBoxFrame = ttk.Frame(primaryFrame)
                textBoxFrame.pack(side='right', anchor='ne')

                fields[key]['inputGetter'] = CollapsibleTextboxMaker(textBoxFrame, value)

                if tipCreator is not None:
                    TipCreator(elementFrame, tipCreator)

                elementFrame.pack(anchor='w', pady=5)

            elif elementType == 'dropdown-single-line':
                fields[key]['inputGetter'] = DropdownListMaker(elementFrame,
                                                               label,
                                                               value,
                                                               mode='edit',
                                                               elementType='single-line')

                if tipCreator is not None:
                    TipCreator(elementFrame, tipCreator)

                elementFrame.pack(anchor='w', pady=5)

            elif elementType == 'dropdown-multi-line':
                fields[key]['inputGetter'] = DropdownListMaker(elementFrame,
                                                               label,
                                                               value,
                                                               mode='edit',
                                                               elementType='multi-line')

                if tipCreator is not None:
                    TipCreator(elementFrame, tipCreator)

                elementFrame.pack(anchor='w', pady=5)

        if mode == 'edit':
            buttonText = StringVar()
            buttonText.set('Edit')
            currentState = 'view'

            def ToggleListMode(*args):
                nonlocal currentState

                if currentState == 'view':
                    buttonText.set('Submit')
                    editElementsFrame.grid(row=0, column=0, sticky="NSEW")
                    viewElementsFrame.grid_remove()
                    currentState = 'edit'
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
                    details[key] = inputGetter()
                valueHandler(details)

            ttk.Button(labelledListFrame,
                       text='Submit',
                       command=SubmitData,
                       style='Buttons.TButton').grid(row=1, column=0, sticky='W', pady=(3, 0))