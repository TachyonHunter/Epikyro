import sqlite3
from tkinter import *
import os
import hashlib
from tkinter import messagebox

import main

def GetUNPWSaltFromDB(username: str, password: str):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        # get username
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        usernameFromDB = cursor.fetchone();

        # get the corresponding password
        cursor.execute("SELECT hashedPassword FROM users WHERE username = ?", (username,))
        passwordFromDB = cursor.fetchone();

        cursor.execute("SELECT salt FROM users WHERE username = ?", (username,))
        salt = cursor.fetchone();

    if usernameFromDB == None:
        return 'UNNotFound'
    else:
        return usernameFromDB, passwordFromDB[0], salt[0]

def Login(username: str,
          password: str,
          closerLambda: Callable[[bool], None]):
    DBGetOperationOutput = GetUNPWSaltFromDB(username, password)
    if DBGetOperationOutput == 'UNNotFound':
        messagebox.showerror('Error', 'Username not found...')
        closerLambda(False)
        return
    else:
        usernameFromDB, passwordFromDB, salt = DBGetOperationOutput

    passwordHash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, main.iterations).hex()

    print(f'Username: {username}\nPassword: {password}')
    print("passwordHash: ", passwordHash, "\npasswordFromDB: ", passwordFromDB)

    # Check the inputted values against the DB.
    if passwordHash != passwordFromDB:
        messagebox.showerror('Error', 'Password incorrect...')
        closerLambda(False)
    else:
        messagebox.showinfo('Success!', 'You have successfully logged in!')
        closerLambda(True)