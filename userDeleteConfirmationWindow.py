from tkinter import *
from tkinter import ttk, messagebox
from DBTools import *
from GUITools import WindowSizingTask, BindFamily

def DeleteConfirmationWindow(user: str, eventHub: ttk.Frame | Frame) -> None:
    deleteConfirmationWindow = Toplevel()
    deleteConfirmationWindow.grab_set()
    deleteConfirmationWindow.focus_set()
    deleteConfirmationWindow.columnconfigure(0, weight=1)
    deleteConfirmationWindow.rowconfigure(0, weight=1)
    deleteConfirmationWindow.title('Confirm Delete?')

    mainframe = ttk.Frame(deleteConfirmationWindow)
    mainframe.grid(column=0, row=0, sticky='N W E S', padx=50, pady=4)
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    mainframe.rowconfigure(6, weight=1)

    def LastBarrier(*args):
        confirmButton.grid_remove()
        userConfirmInput = StringVar()

        def DeleteUserCaller(*args):
            if userConfirmInput.get() == user:
                operationResult = DeleteUser(userConfirmInput.get())
                if operationResult == 'success':
                    messagebox.showinfo('Success!', 'User deleted successfully!', parent=mainframe)
                    eventHub.event_generate("<<UserDeleted>>")
                else:
                    messagebox.showerror('Error', operationResult, parent=mainframe)

                deleteConfirmationWindow.destroy()
            else:
                messagebox.showerror("Error", "Mismatched Username...", parent=mainframe)
                deleteConfirmationWindow.destroy()

        ttk.Label(mainframe, text='Re-enter the username:', style='Body.TLabel').grid(row=2, column=0)
        ttk.Entry(mainframe, textvariable=userConfirmInput, font=('Aptos', 14)).grid(row=3, column=0)
        ttk.Button(mainframe, text='Confirm', command=DeleteUserCaller, style='Buttons.TButton').grid(row=4, column=0, pady=4)

        deleteConfirmationWindow.bind('<Return>', DeleteUserCaller)

    ttk.Label(mainframe, text=f'Are you sure you want to delete "{user}"?', style='Body Titles.TLabel').grid(row=1, column=0)
    confirmButton = ttk.Button(mainframe, text='Yes', command=LastBarrier, style='Buttons.TButton')
    confirmButton.grid(row=2, column=0)

    deleteConfirmationWindow.bind('<Return>', LastBarrier)

    WindowSizingTask(deleteConfirmationWindow, allowUserResizing=False)

    # Code to prevent permanent focus steal by widgets.
    BindFamily(deleteConfirmationWindow, '<Button-1>', lambda e: deleteConfirmationWindow.focus_set(), bindInteractives=False)