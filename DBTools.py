import sqlite3

# Function returning a list of users from our database.
def ListUsers():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    users = [i[0] for i in cursor.fetchall()]
    conn.close()
    return users

# Function deleting a user and returning its relevant data.
def DeleteUser(user):
    pass

# Function retrieving user details for a given user.
def RetrieveUserDetails(user, detailsToRetrieve = ('firstName', 'lastName', 'email', 'designation', 'DOB', 'DOJoining')):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        columns = ', '.join(detailsToRetrieve)
        cursor.execute(f"SELECT {columns} FROM users WHERE username = ?", (user,))
        userDetails = dict(zip(detailsToRetrieve, cursor.fetchone()))
        conn.close()
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