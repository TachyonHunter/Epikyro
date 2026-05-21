from tkinter import *
from tkinter import ttk
from login import *

def LoginWindow(welcomeNotification, loginOrSwitchButtonText, logOutButton, adminFrame, headerFrame, generalFrame):
    loginWindow = Toplevel()
    loginWindow.title('Login')
    loginWindow.columnconfigure(0, weight=1)
    loginWindow.rowconfigure(0, weight=1)
    loginWindow.update_idletasks()
    loginWindow.lift()
    loginWindow.focus_force()

    # Code to center the window.
    screenWidth = loginWindow.winfo_screenwidth()
    screenHeight = loginWindow.winfo_screenheight()
    windowWidth = 500
    windowHeight = 300
    x = (screenWidth // 2) - (windowWidth // 2)
    y = (screenHeight // 2) - (windowHeight // 2)
    loginWindow.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    # Creates mainframe.
    mainframe = ttk.Frame(loginWindow, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky='N W E S')
    mainframe.columnconfigure(0, weight=1)

    # Creates the username and password entries (user-input textboxes).
    username = StringVar()
    password = StringVar()
    userNotification = StringVar()
    usernameField = ttk.Entry(mainframe, textvariable=username, font=("Aptos", 13))
    usernameField.focus_set()
    passwordField = ttk.Entry(mainframe, textvariable=password, show='*', font=("Aptos", 13))
    usernameField.grid(row=2, column=0)
    passwordField.grid(row=4, column=0)

    # Creating labels.
    ttk.Label(mainframe, text='Login:', font=('Aptos', 52)).grid(row=0, column=0)
    ttk.Label(mainframe, text='Username:', font=('Aptos', 22)).grid(row=1, column=0)
    ttk.Label(mainframe, text='Password:', font=('Aptos', 22)).grid(row=3, column=0)

    #Function to call our function.
    def LoginCaller(*args):
        Login(username.get(), password.get(), userNotification, )

    # Button.
    ttk.Button(mainframe, text="Login", command=LoginCaller, style='Buttons.TButton').grid(row=5, column=0, pady=(10,0))

    # The status for the users.
    ttk.Label(mainframe, textvariable=userNotification).grid(row=6, column=0)
    loginWindow.bind("<Return>", LoginCaller)

    def OnClose():
        if userNotification.get() == 'Login successful...':
            welcomeNotification.set(f'Welcome {username.get()}!')
            loginOrSwitchButtonText.set('Switch account')
            logOutButton.grid(row=0, column=2, sticky='E')
            if username.get() == 'admin':
                adminFrame.grid(row=0, column=1, sticky='E', padx=(0, 4))
                headerFrame.columnconfigure(1, weight=1)
                generalFrame.grid_remove()
            else:
                generalFrame.grid(row=0, column=1, sticky='E', padx=(0, 4))
                headerFrame.columnconfigure(1, weight=1)
                adminFrame.grid_remove()
        loginWindow.destroy()

    loginWindow.protocol("WM_DELETE_WINDOW", OnClose)

    loginWindow.mainloop()