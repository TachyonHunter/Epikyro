from tkinter import *
from tkinter import ttk, messagebox
from DBTools import *
from GUITools import *

def DeleteConfirmationWindow(user):
    deleteConfirmationWindow = Toplevel()
    deleteConfirmationWindow.grab_set()
    deleteConfirmationWindow.focus_set()
    deleteConfirmationWindow.columnconfigure(0, weight=1)
    deleteConfirmationWindow.rowconfigure(0, weight=1)
    deleteConfirmationWindow.title('Confirm Delete?')

    mainframe = ttk.Frame(deleteConfirmationWindow)
    mainframe.grid(column=0, row=0, sticky='N W E S')
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    mainframe.rowconfigure(6, weight=1)
    desiredWidth, desiredHeight = 600, 180
    deleteConfirmationWindow.geometry(WindowSizer(deleteConfirmationWindow, desiredWidth, desiredHeight))

    def LastBarrier(*args):
        confirmButton.grid_remove()
        userConfirmInput = StringVar()

        def DeleteUserCaller(*args):
            if userConfirmInput.get() == user:
                DeleteUser(userConfirmInput.get())
                # Need to store user as some recently deleted thing too...
                messagebox.showinfo('Success!', f'{user} has been deleted.', parent=mainframe)
                deleteConfirmationWindow.destroy()
            else:
                messagebox.showerror("Error", "Mismatched Username...", parent=mainframe)
                deleteConfirmationWindow.destroy()

        ttk.Label(mainframe, text='Re-enter the username:', font=('Aptos', 16)).grid(row=2, column=0)
        ttk.Entry(mainframe, textvariable=userConfirmInput, font=('Aptos', 13)).grid(row=3, column=0)
        ttk.Button(mainframe, text='Confirm', command=DeleteUserCaller, style='Buttons.TButton').grid(row=4, column=0)

        deleteConfirmationWindow.bind('<Return>', DeleteUserCaller)

    ttk.Label(mainframe, text=f'Are you sure you want to delete "{user}"?', font=('Aptos', 18)).grid(row=1, column=0)
    confirmButton = ttk.Button(mainframe, text='Yes', command=LastBarrier, style='Buttons.TButton')
    confirmButton.grid(row=2, column=0)

    deleteConfirmationWindow.bind('<Return>', LastBarrier)
    deleteConfirmationWindow.mainloop()