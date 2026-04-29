from tkinter import *
from tkinter import ttk
from functools import partial
from login import *

# Creates root.
def LoginWindow(welcomeNotification, loginButtonText):
    loginWindow = Toplevel()
    loginWindow.title('Login')
    loginWindow.columnconfigure(0, weight=1)
    loginWindow.rowconfigure(0, weight=1)

    # Creates mainframe (window, basically).
    mainframe = ttk.Frame(loginWindow, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky='N W E S')
    mainframe.columnconfigure(0, weight=1)

    # Creates the username and password entries (user-input textboxes).
    username = StringVar()
    password = StringVar()
    userNotification = StringVar()
    usernameField = Entry(mainframe, textvariable=username, font=("Segoe UI", 13))
    passwordField = Entry(mainframe, textvariable=password, show='*', font=("Segoe UI", 13))
    usernameField.grid(row=2, column=0)
    passwordField.grid(row=4, column=0)

    # Creating labels.
    ttk.Label(mainframe, text='Login:', font=('Segoe UI', 52)).grid(row=0, column=0)
    ttk.Label(mainframe, text='Username:', font=('Segoe UI', 22)).grid(row=1, column=0)
    ttk.Label(mainframe, text='Password:', font=('Segoe UI', 22)).grid(row=3, column=0)

    #Function to call our function... Tkinter runs all isolated functions on startup...
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
            loginButtonText.set('Switch account')
        loginWindow.destroy()

    loginWindow.protocol("WM_DELETE_WINDOW", OnClose)

    loginWindow.mainloop()