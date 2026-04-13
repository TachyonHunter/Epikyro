import sqlite3
# Error codes:
# incorrectUN - Incorrect Username passed
# incorrectPW - Incorrect Password passed
# correct - Success#
# what case scheme do you want to use in this project??
# I was thinking camelCase for variables and functions, and PascalCase for classes, unless we aren't using classes?

def Login(username, password):#username, password, and the database with users.

    #connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    #get the username
    cursor.execute(f"SELECT 1 FROM users WHERE name = ?", (username,))
    usernameDB = cursor.fetchone();

    #get the corresponding password
    cursor.execute(f"SELECT password FROM users WHERE name = ?", (username,))
    passwordDB = cursor.fetchone();

    #close the connection
    cursor.close()
    conn.close()

    #check the inputted values against the DB
    if usernameDB==None:
        return (0, 'incorrectUN') 
    if password != passwordDB[0]:
        return (0, 'incorrectPW')
    else:
        return (1, 'correct')

# the 0s and 1s basically make this a boolean function while also being a string function
# so we can use the 0s and 1s to check if the login was successful or not, and the strings to get the specific error messages