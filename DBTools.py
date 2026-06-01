import sqlite3

from passwordFunctions import GiveHashSalt


# Function returning a list of users from our database.
def ListUsers():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE isDeleted = 0")
        users = [i[0] for i in cursor.fetchall()]
    return users

# Function deleting a user and returning its relevant data.
def DeleteUser(user):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET isDeleted = TRUE WHERE username = ?", (user,))
        return 'success'
    except Exception as e:
        return str(e)

# Function retrieving user details for a given user.
def RetrieveUserDetails(user, detailsToRetrieve = ('firstName', 'lastName', 'email', 'designation', 'DOB', 'DOJoining')):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            columns = ', '.join(detailsToRetrieve)
            cursor.execute(f"SELECT {columns} FROM users WHERE username = ?", (user,))
            userDetails = dict(zip(detailsToRetrieve, cursor.fetchone()))
        return userDetails
    except TypeError:
        print("User not found")
        return 'not found'

# Function updating all given columns with new values for a given user.
def UpdateUserDetails(user, details):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            setClause = ", ".join(f"{k} = ?" for k in details.keys())
            cursor.execute(f"""
                           UPDATE users
                           SET {setClause}
                           WHERE username = ?
                           """, tuple(v for v in details.values())+(user,))
        return 'success'
    except Exception as e:
        return str(e)

# Function to add new users to the DB.
def AddUser(details):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()

            password = details['password']
            hashedPassword, salt = GiveHashSalt(password)
            del details['password']
            details['hashedPassword'] = hashedPassword
            details['salt'] = salt
            details['isDeleted'] = False

            columns = ', '.join(details.keys())
            valuePlaceholders = ', '.join('?' for _ in details.keys())
            cursor.execute(f'INSERT INTO users ({columns}) VALUES ({valuePlaceholders})', tuple(details.values()))
        return 'success'
    except Exception as e:
        return str(e)

def GetValueFromUser(username, column):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {column} FROM users WHERE username = ?", (username,))
            return cursor.fetchone()[0]
    except Exception as e:
        return str(e)