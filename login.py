import sqlite3
# Error codes:
# incorrectUN - Incorrect Username passed
# incorrectPW - Incorrect Password passed
# correct - Success

#Hi. We can't return anything from functions being called by buttons. So I've made it set data in a stringVar.
def Login(username, password, statusText):#username, password, and the database with users.
    #connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    #get the username
    cursor.execute(f"SELECT 1 FROM users WHERE name = ?", (username,))
    usernameFromDB = cursor.fetchone();

    #get the corresponding password
    cursor.execute(f"SELECT password FROM users WHERE name = ?", (username,))
    passwordFromDB = cursor.fetchone();

    #close the connection
    cursor.close()
    conn.close()

    #check the inputted values against the DB
    if usernameFromDB==None:
        statusText.set('Username not found...')
    if password != passwordFromDB[0]:
        statusText.set('Password incorrect...')
    else:
        statusText.set('Login successful...')