from tkinter import *
from tkinter import ttk
from login import *
from GUITools import *
from DBTools import GetValueFromUser
from main import sessionStateVars

def LoginWindow(eventHub):
    loginWindow = Toplevel()
    loginWindow.title('Login')
    loginWindow.columnconfigure(0, weight=1)
    loginWindow.rowconfigure(0, weight=1)
    loginWindow.update_idletasks()
    loginWindow.lift()
    loginWindow.focus_force()

    # Creates mainframe.
    mainframe = ttk.Frame(loginWindow)
    mainframe.grid(column=0, row=0, sticky='N W E S', padx=50, pady=10)
    mainframe.columnconfigure(0, weight=1)

    # Creates the username and password entries (user-input textboxes).
    username = StringVar()
    password = StringVar()
    usernameField = ttk.Entry(mainframe, textvariable=username, font=('Aptos', 14))
    usernameField.focus_set()
    passwordField = ttk.Entry(mainframe, textvariable=password, show='*', font=("Aptos", 14))
    usernameField.grid(row=2, column=0)
    passwordField.grid(row=4, column=0)

    # Creating labels.
    ttk.Label(mainframe, text='Login:', style='Headings.TLabel').grid(row=0, column=0)
    ttk.Label(mainframe, text='Username:', style='Sub-sub-headings.TLabel').grid(row=1, column=0)
    ttk.Label(mainframe, text='Password:', style='Sub-sub-headings.TLabel').grid(row=3, column=0)

    # Function to call our function.
    def LoginCaller(*args):
        Login(username.get(), password.get(), lambda success: OnClose(success))

    # Login Button.
    ttk.Button(mainframe, text="Login", command=LoginCaller, style='Buttons.TButton').grid(row=5, column=0, pady=(10,0))

    loginWindow.bind("<Return>", LoginCaller)

    def OnClose(success: bool):
        sessionStateVars['account'] = username.get()
        if success:
            if GetValueFromUser(username.get(), 'designation') == 'admin':
                eventHub.event_generate("<<adminLogin>>")
            else:
                eventHub.event_generate("<<normalLogin>>")
        loginWindow.destroy()

    WindowSizingTask(loginWindow, allowUserResizing=False)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(loginWindow,
               '<Button-1>',
               lambda e: loginWindow.focus_set(),
               bindInteractives=False,
               bindParent=False)