import sqlite3

# Function returning a list of users from our database.
def ListUsers():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    users = [i[0] for i in cursor.fetchall()]
    cursor.close()
    conn.close()
    return users

# Function deleting a user and returning its relevant data.
def DeleteUser(user):
    pass

# Function retrieving user details for a given user.
def RetrieveUserDetails(user):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT firstName, lastName, designation, DOB, DOJoining FROM users WHERE username = ?", (user,))
    userDetails = cursor.fetchone()
    cursor.close()
    conn.close()
    return userDetails