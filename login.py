import sqlite3
from tkinter import *
import os
import hashlib
import main

def DataBaseConnect(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # get username
    cursor.execute("SELECT name FROM users WHERE name = ?", (username,))
    usernameFromDB = cursor.fetchone();

    # get the corresponding password
    cursor.execute("SELECT password FROM users WHERE name = ?", (username,))
    passwordFromDB = cursor.fetchone();

    cursor.execute("SELECT salt FROM users WHERE name = ?", (username,))
    salt = cursor.fetchone();

    # close the connection
    cursor.close()
    conn.close()
    return usernameFromDB, passwordFromDB[0], salt[0]



def Login(username, password, statusText, ): # username, password, and the .
    usernameFromDB, passwordFromDB, salt = DataBaseConnect(username, password)
    passwordHash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, main.iterations).hex()

    print(f'Username: {username}\nPassword: {password}\nStatusText: {statusText.get()}')

    print("passwordHash: ", passwordHash, "\npasswordFromDB: ", passwordFromDB)
    # Check the inputted values against the DB.
    if usernameFromDB==None:
        statusText.set('Username not found...')
    elif passwordHash != passwordFromDB:
        statusText.set('Password incorrect...')
    else:
        statusText.set('Login successful...')