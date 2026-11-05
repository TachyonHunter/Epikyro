from tkinter import *
from tkinter import ttk, font
from typing import Callable
from ttk_text import ThemedText
import tkinter as tk
from copy import deepcopy

# Debugging...
debugRoot = None
debugWidget = None
debugInspectorEnabled = False

def SetDebugRoot(rootWindow):
    global debugRoot

    debugRoot = rootWindow

    # Listen for the shortcut and mouse clicks throughout the application.
    debugRoot.bind_all(
        '<Control-Shift-I>',
        DebugToggleShortcut,
        add='+'
    )

    debugRoot.bind_all(
        '<Button-1>',
        DebugWidgetClick,
        add='+'
    )

    print('Debug tools initialized.')

def DebugToggleShortcut(event):
    ToggleWidgetInspector()
    return 'break'

def ToggleWidgetInspector():
    global debugInspectorEnabled

    if debugRoot is None:
        raise RuntimeError('Debug root has not been set.')

    debugInspectorEnabled = not debugInspectorEnabled

    status = 'enabled' if debugInspectorEnabled else 'disabled'
    print(f'Widget inspector {status}.')

def DebugWidgetClick(event):
    global debugWidget

    if not debugInspectorEnabled:
        return

    debugWidget = event.widget

    print()
    print('--- Widget selected ---')
    print(f'Widget:   {debugWidget}')
    print(f'Class:    {debugWidget.winfo_class()}')
    print(f'Path:     {debugWidget._w}')
    print(f'Geometry: {debugWidget.winfo_geometry()}')
    print(f'Parent:   {debugWidget.master}')
    print('-----------------------')

    if isinstance(debugWidget, ttk.Label):
        print('Text:', debugWidget.cget('text'))
        textVar = debugWidget.cget('textvariable')
        print('Textvar:', textVar)
        print('TextVarVal:', repr(debugWidget.getvar(textVar)))
        print('Reqwidth:', debugWidget.winfo_reqwidth())
        print('Given Width:', debugWidget.master.winfo_width())
        print('Reqheight:', debugWidget.winfo_reqheight())
        print('Given height:', debugWidget.master.winfo_height())

def DebugWidget():
    """Return the widget most recently clicked while inspecting."""
    return debugWidget

def DebugUpdate():
    """Process pending geometry and redraw operations."""
    if debugRoot is None:
        raise RuntimeError('Debug root has not been initialized.')

    debugRoot.update_idletasks()

def DebugWidgetInfo():
    """Print useful information about the selected widget."""
    if debugWidget is None:
        print('No widget has been selected.')
        return

    widget = debugWidget

    try:
        if not widget.winfo_exists():
            print('The selected widget has been destroyed.')
            return

        print()
        print('========== WIDGET ==========')
        print(f'Object:       {widget}')
        print(f'Class:        {widget.winfo_class()}')
        print(f'Path:         {widget._w}')
        print(f'Parent:       {widget.master}')
        print(f'Geometry:     {widget.winfo_geometry()}')
        print(f'Width:        {widget.winfo_width()}')
        print(f'Height:       {widget.winfo_height()}')
        print(
            f'Requested:    {widget.winfo_reqwidth()}'
            f' x {widget.winfo_reqheight()}'
        )
        print(f'X:            {widget.winfo_x()}')
        print(f'Y:            {widget.winfo_y()}')
        print(f'Root X:       {widget.winfo_rootx()}')
        print(f'Root Y:       {widget.winfo_rooty()}')
        print('============================')

    except tk.TclError:
        print('The selected widget no longer exists.')

def DebugFocusIn(operation):
    """Attach an additional FocusIn handler to the selected widget."""
    if debugWidget is None:
        raise RuntimeError('No widget has been selected.')

    debugWidget.bind('<FocusIn>', operation, add='+')
    print(f'FocusIn binding added to {debugWidget}.')

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
                      elementType,
                      tipDeclaration = None):
    if mode not in ('view', 'edit'):
        raise ValueError("Mode must be 'view' or 'edit'.")

    if elementType not in ('single-line', 'multi-line', 'structured'):
        raise ValueError("elementType must be 'single-line' or 'multi-line'.")

    dropdownListFrame = ttk.Frame(container)
    dropdownListFrame.grid(row=0, column=0, pady=5)
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

    emptyFrame = ttk.Frame(elementsFrame)
    emptyFrame.pack(anchor='w', pady=5)
    ttk.Label(emptyFrame,
              text='Currently empty...',
              style='Body.TLabel',
              justify='left').grid(row=0, column=0, sticky='W')
    emptyFrame.pack_forget()

    if mode == 'view':
        for i in range(len(elements)):
            text = elements[i]
            if len(text) > 20:
               text = text[:17]+'...'
            element = ttk.Label(elementsFrame,
                                text=text,
                                style='Body.TLabel',
                                justify='left')
            element.grid(row=i, column=0, sticky="W")

    elif mode == 'edit':
        getters = []
        if tipDeclaration is not None:
            tipFrame = ttk.Frame(elementsFrame)
            tipObject = tipDeclaration(tipFrame)
            tipFrame.pack(side='top', anchor='nw')
            tipObject.grid(row=0, column=0, sticky='NSEW')

        def DeleteElement(element, getter):
            getters.remove(getter)
            element.destroy()
            noOfElements = len(getters)
            if noOfElements == 0:
                emptyFrame.pack(anchor='w', pady=5)

        def AddElement(content, contentMaker):
            noOfElements = len(getters)
            if noOfElements == 0:
                emptyFrame.pack_forget()

            element = ttk.Frame(elementsFrame)

            getter = contentMaker(element, content)
            getters.append(getter)

            ttk.Button(
                element,
                text='Remove',
                style='Buttons.TButton',
                command=lambda frame=element, getter=getter:
                DeleteElement(frame, getter)
            ).grid(column=1, row=0, sticky='E', padx=2)

            element.pack(anchor='w', pady=5)

        if elementType == 'single-line':
            def MakeContent(parent, content):
                entryVar = StringVar(value=content)

                ttk.Entry(
                    parent,
                    textvariable=entryVar,
                    font=('Aptos', 16),
                    justify='left'
                ).grid(column=0, row=0, sticky='W')

                return entryVar.get

            for content in elements:
                AddElement(content, MakeContent)

        elif elementType == 'multi-line':
            def MakeContent(parent, content):
                return CollapsibleTextboxMaker(parent, content)

            for content in elements:
                AddElement(content, MakeContent)

        addElementButton = ttk.Button(dropdownListFrame,
                                      text='Add',
                                      style='Buttons.TButton',
                                      command=lambda: AddElement('', MakeContent))

    isListHidden = True
    def ToggleList(*args):
        nonlocal isListHidden
        if isListHidden:
            elementsFrame.grid(row=1, column=0, sticky="NSEW")
            titleText.set('⏷ ' + title)
            isListHidden = False
            if mode == 'edit':
                addElementButton.grid(column=0, row=2, sticky='W', padx=2)

            if tipDeclaration is not None:
                tipFrame.pack(side='top', anchor='nw')
        else:
            elementsFrame.grid_remove()
            titleText.set('⏵ ' + title)
            isListHidden = True
            if mode == 'edit':
                addElementButton.grid_remove()

            if tipDeclaration is not None:
                tipFrame.pack_forget()

    titleLabel.bind('<Button-1>', ToggleList)

    return None if mode == 'view' else lambda: list(getter() for getter in getters)

def StructuredDropdownMaker(container,
                            title,
                            structureDefinition,
                            mode,
                            tipDeclaration = None):
    if mode not in ('view', 'edit'):
        raise ValueError("Mode must be 'view' or 'edit'.")

    structuredDropdownFrame = ttk.Frame(container)
    structuredDropdownFrame.grid(row=0, column=0, pady=5)
    structuredDropdownFrame.columnconfigure(0, weight=1)

    titleText = StringVar()
    titleText.set('⏵ ' + title)

    titleLabel = ttk.Label(structuredDropdownFrame,
                           textvariable=titleText,
                           style='Body Titles.TLabel',
                           justify='left')
    titleLabel.grid(column=0, row=0, sticky="W")

    elementsFrame = ttk.Frame(structuredDropdownFrame)
    elementsFrame.grid(row=2, column=0, sticky="NSEW", padx=8)
    elementsFrame.grid_remove()

    if tipDeclaration is not None:
        tipFrame = ttk.Frame(elementsFrame)
        tipObject = tipDeclaration(tipFrame)
        tipFrame.pack(side='top', anchor='nw')
        tipObject.grid(row=0, column=0, sticky='NSEW')

    emptyFrame = ttk.Frame(elementsFrame)
    emptyFrame.pack(anchor='w', pady=5)
    ttk.Label(emptyFrame,
              text='Currently empty...',
              style='Body.TLabel',
              justify='left').grid(row=0, column=0, sticky='W')
    emptyFrame.pack_forget()

    def MakeStructuredElement(fields, mode, getters):
        noOfElements = len(getters)
        if noOfElements == 0:
            emptyFrame.pack_forget()

        element = ttk.Frame(elementsFrame)
        element.columnconfigure(0, weight=1)
        element.pack(anchor='w', pady=5)
        expandedFrame = ttk.Frame(element)
        expandedFrame.grid(row=1, column=0, sticky='NSEW')

        getter = LabelledListMaker(expandedFrame,
                                   fields,
                                   'edit-core' if mode == 'edit' else 'view')

        expandedFrame.grid_remove()

        if mode == 'edit':
            getters.append(getter)

        collapsedFrame = ttk.Frame(element)
        collapsedFrame.grid(row=1, column=0, sticky='NSEW')
        collapsedFrame.columnconfigure(0, weight=1)
        titleLabel = ttk.Label(element,
                               text='⏵ ' + ' - '.join(definition['value'] if definition['value'] else 'NULL' for definition in fields.values()),
                               style='Body.TLabel',
                               justify='left')
        titleLabel.grid(row=0, column=0, sticky='W')

        isListHidden = True
        def ToggleList(*args):
            nonlocal isListHidden
            currentText = titleLabel.cget('text')
            if isListHidden:
                expandedFrame.grid(row=1, column=0, sticky='NSEW')
                collapsedFrame.grid_remove()
                titleLabel.configure(text='⏷ ' + currentText[2:])
                isListHidden = False
            else:
                collapsedFrame.grid(row=1, column=0, sticky='NSEW')
                expandedFrame.grid_remove()
                titleLabel.configure(text='⏵ ' + currentText[2:])
                isListHidden = True

        titleLabel.bind('<Button-1>', ToggleList)

        if mode == 'edit':
            destroyed = False

            def DeleteElement(element, getter):
                nonlocal destroyed
                destroyed = True
                element.destroy()
                getters.remove(getter)
                noOfElements = len(getters)
                if noOfElements == 0:
                    emptyFrame.pack(anchor='w', pady=5)

            def UpdateTitleTask():
                nonlocal destroyed
                if destroyed:
                    return

                values = getter()
                if isListHidden:
                    titleLabel.configure(text='⏵ ' + ' - '.join(v if v else 'NULL' for k, v in values.items()))
                else:
                    titleLabel.configure(text='⏷ ' + ' - '.join(v if v else 'NULL' for k, v in values.items()))
                container.after(200, UpdateTitleTask)

            UpdateTitleTask()

            ttk.Button(
                element,
                text='Remove',
                style='Buttons.TButton',
                command=lambda frame=element, getter=getter:
                DeleteElement(frame, getter)
            ).grid(column=1, row=0, sticky='E', padx=2)

    getters = []
    structureMembers = structureDefinition['structure']['structureMembers']
    if structureDefinition['values']:
        for value in structureDefinition['values']:
            fields = {}
            for structureMember in structureMembers:
                fields[structureMember] = {
                    'label': structureDefinition['structure']['labels'][structureMember],
                    'value': value[structureMember],
                    'elementType': structureDefinition['structure']['elementTypes'][structureMember]
                }
            MakeStructuredElement(fields, mode, getters)
    else:
        emptyFrame.pack(anchor='w', pady=5)


    emptyFields = {}
    for structureMember in structureMembers:
        emptyFields[structureMember] = {
                'label': structureDefinition['structure']['labels'][structureMember],
                'value': '',
                'elementType': structureDefinition['structure']['elementTypes'][structureMember]
            }
    addElementButton = ttk.Button(structuredDropdownFrame,
                                  text='Add',
                                  style='Buttons.TButton',
                                  command=lambda: MakeStructuredElement(deepcopy(emptyFields),
                                                                        mode,
                                                                        getters))

    isListHidden = True
    def ToggleList(*args):
        nonlocal isListHidden
        if isListHidden:
            elementsFrame.grid(row=2, column=0, sticky="NSEW")
            titleText.set('⏷ ' + title)
            isListHidden = False

            if mode == 'edit':
                addElementButton.grid(column=0, row=3, sticky='W', padx=2)

            if tipDeclaration is not None:
                tipFrame.pack(side='top', anchor='nw')
        else:
            elementsFrame.grid_remove()
            titleText.set('⏵ ' + title)
            isListHidden = True

            if mode == 'edit':
                addElementButton.grid_remove()

            if tipDeclaration is not None:
                tipFrame.pack_forget()
    titleLabel.bind('<Button-1>', ToggleList)

    return lambda: list(getter() for getter in getters) if mode != 'view' else None

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
        - 'structured-dropdown-single-line'
        - 'stuctured-dropdown-multi-line'

    During creation of the list, the key 'inputGetter' is added. Its value is
    an object that contains the inputted data.

    The colon (:), etc. must be provided for the label.
    """

    if mode not in ('view', 'edit', 'create', 'edit-core'):
        raise ValueError("Mode must be 'view', 'edit', 'core' or 'create'.")

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

    if mode not in ('create', 'edit-core'):
        for key, fieldDef in fields.items():
            label = fieldDef['label']
            value = fieldDef['value']
            elementType = fieldDef.get('elementType')
            if elementType in ('single-line', 'multi-line') or elementType is None:
                ttk.Label(viewElementsFrame,
                          text=f'{label}{value}',
                          style='Body.TLabel').pack(anchor='w', pady=5)
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
            elif elementType == 'structured-dropdown':
                elementFrame = ttk.Frame(viewElementsFrame)
                StructuredDropdownMaker(elementFrame,
                                        label,
                                        value,
                                        mode='view')
                elementFrame.pack(anchor='w', pady=5)

    if mode in ('edit', 'create', 'edit-core'):
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
                element = ttk.Frame(elementFrame)
                element.pack(anchor='w', side='top')
                ttk.Label(element,
                          text=f'{label}',
                          style='Body Titles.TLabel',
                          justify='left').pack(side='left', anchor='nw')

                entryVar = StringVar()
                inputVars[key] = entryVar

                fields[key]['inputGetter'] = lambda var=entryVar: var.get()

                entry = ttk.Entry(
                    element,
                    textvariable=entryVar,
                    font=('Aptos', 16)
                )
                entry.pack(side='right', anchor='ne')

                entryVar.set(value)

                if tipCreator is not None:
                    TipCreator(elementFrame, tipCreator)

                elementFrame.pack(anchor='w', pady=5)

            elif elementType == 'multi-line':
                element = ttk.Frame(elementFrame)
                element.pack(anchor='w', side='top')
                ttk.Label(element,
                          text=f'{label}',
                          style='Body Titles.TLabel',
                          justify='left').pack(side='left', anchor='nw')

                textBoxFrame = ttk.Frame(element)
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
                                                               elementType='single-line',
                                                               tipDeclaration=tipCreator)

                elementFrame.pack(anchor='w', pady=5)

            elif elementType == 'dropdown-multi-line':
                fields[key]['inputGetter'] = DropdownListMaker(elementFrame,
                                                               label,
                                                               value,
                                                               mode='edit',
                                                               elementType='multi-line',
                                                               tipDeclaration=tipCreator)

                elementFrame.pack(anchor='w', pady=5)

            elif elementType == 'structured-dropdown':
                fields[key]['inputGetter'] = StructuredDropdownMaker(elementFrame,
                                                                     label,
                                                                     value,
                                                                     mode='edit',
                                                                     tipDeclaration=tipCreator)

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
                        value = inputGetter()
                        if fieldDef.get('elementType') == 'structured-dropdown':
                            details[key] = fields[key]['value']['values'] = value if value else []
                        elif fieldDef.get('elementType') in ('dropdown-single-line', 'dropdown-multi-line'):
                            details[key] = fields[key]['value'] = value if (value and all(i for i in value)) else ['nil']
                        else:
                            details[key] = fields[key]['value'] = value

                    valueHandler(details)

                    labelledListFrame.destroy()
                    LabelledListMaker(container, fields, 'edit', valueHandler)

            ttk.Button(labelledListFrame,
                       textvariable=buttonText,
                       command=ToggleListMode,
                       style='Buttons.TButton').grid(row=1, column=0, sticky='W', pady=(3, 0))

        elif mode == 'edit-core':
            editElementsFrame.grid(row=0, column=0, sticky="NSEW")

            def Getter():
                details = {}
                for key, fieldDef in fields.items():
                    inputGetter = fieldDef.get('inputGetter')
                    value = inputGetter()
                    if fieldDef.get('elementType') == 'structured-dropdown':
                        details[key] = value if value else []
                    elif fieldDef.get('elementType') in ('dropdown-single-line', 'dropdown-multi-line'):
                        details[key] = value if (value and all(i for i in value)) else ['nil']
                    else:
                        details[key] = value
                return details

            return Getter

        elif mode == 'create':
            editElementsFrame.grid(row=0, column=0, sticky="NSEW")

            def SubmitData():
                details = {}
                for key, fieldDef in fields.items():
                    inputGetter = fieldDef.get('inputGetter')
                    value = inputGetter()
                    if fieldDef.get('elementType') == 'structured-dropdown':
                        details[key] = fields[key]['value']['values'] = value if value else []
                    elif fieldDef.get('elementType') in ('dropdown-single-line', 'dropdown-multi-line'):
                        details[key] = fields[key]['value'] = value if (value and all(i for i in value)) else ['nil']
                    else:
                        details[key] = fields[key]['value'] = value

                valueHandler(details)

            ttk.Button(labelledListFrame,
                       text='Submit',
                       command=SubmitData,
                       style='Buttons.TButton').grid(row=1, column=0, sticky='W', pady=(3, 0))

    return None

def CheckboxListMaker(container,
                      categories):
    checkboxListFrame = ttk.Frame(container, padding=8)
    checkboxListFrame.grid(row=0, column=0, sticky="NSEW")
    checkboxListFrame.columnconfigure(0, weight=1)
    checkboxListFrame.rowconfigure(0, weight=1)
    getters = {}

    for k, definition in categories.items():
        element = ttk.Frame(checkboxListFrame)
        isEnabled = BooleanVar(value=False)
        elementType = definition.get('type')

        if elementType is None or elementType == 'default':
            labelText = StringVar()
            labelText.set(definition['label'])
            ttk.Label(element,
                      textvariable=labelText,
                      justify='left',
                      style='Body Titles.TLabel').grid(row=0, column=1, sticky='W', padx=4)
            entryVar = StringVar()
            entry = ttk.Entry(element, textvariable=entryVar, font=('Aptos', 16))
            entry.grid(row=0, column=2, sticky='W')
            entry.grid_remove()
            getters[k] = lambda e=entryVar, enabled=isEnabled: (
                e.get() if enabled.get() else None
            )

            def ToggleContent(
                    e=entry,
                    text=labelText,
                    d=definition,
                    enabled=isEnabled
            ):
                if not enabled.get():
                    e.grid_remove()
                    text.set(d['label'])
                else:
                    e.grid(row=0, column=2, sticky='W')
                    text.set(d['label'] + ' as:')


        elif elementType == 'list':
            label = ttk.Label(
                element,
                text=definition['label'],
                justify='left',
                style='Body Titles.TLabel'
            )

            label.grid(row=0, column=1, sticky='W', padx=4)
            listFrame = ttk.Frame(element)
            listFrame.grid(row=0, column=1, columnspan=3, sticky='NSEW')
            listFrame.grid_remove()

            getter = DropdownListMaker(
                listFrame,
                definition['label'] + ' in:',
                '',
                mode='edit',
                elementType='single-line'
            )

            getters[k] = lambda g=getter, enabled=isEnabled: (
                g() if enabled.get() else None
            )

            def ToggleContent(
                    frame=listFrame,
                    lbl=label,
                    enabled=isEnabled
            ):
                if enabled.get():
                    frame.grid(row=0, column=1, columnspan=3, sticky='NSEW')
                    lbl.grid_remove()
                else:
                    frame.grid_remove()
                    lbl.grid(row=0, column=1, sticky='W', padx=4)
        else:
            raise ValueError('Unknown element type...')

        ttk.Checkbutton(element, variable=isEnabled, command=ToggleContent).grid(row=0, column=0, sticky='NW')

        element.pack(anchor='w', pady=5)

    return lambda: {k: v() for k, v in getters.items() if v() is not None}