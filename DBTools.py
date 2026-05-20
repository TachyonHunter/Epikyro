import sqlite3
# Function returning a list of users from our database.
def ListUsers():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    users = [i[0] for i in cursor.fetchall()]
    cursor.close()
    conn.close()
    return users