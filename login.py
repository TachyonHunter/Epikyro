import sqlite3
from tkinter import *
# Error codes:
# incorrectUN - Incorrect Username passed
# incorrectPW - Incorrect Password passed
# correct - Success

def Login(username, password, statusText, ): # username, password, and the .
    print(f'Username: {username}\nPassword: {password}\nStatusText: {statusText.get()}')
    #connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    #get the username
    cursor.execute("SELECT name FROM users WHERE name = ?", (username,))
    usernameFromDB = cursor.fetchone();

    #get the corresponding password
    cursor.execute("SELECT password FROM users WHERE name = ?", (username,))
    passwordFromDB = cursor.fetchone();

    #close the connection
    cursor.close()
    conn.close()

    # Check the inputted values against the DB.
    if usernameFromDB==None:
        statusText.set('Username not found...')
    elif password != passwordFromDB[0]:
        statusText.set('Password incorrect...')
    else:
        statusText.set('Login successful...')