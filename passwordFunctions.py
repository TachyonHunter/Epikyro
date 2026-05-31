import hashlib
import sqlite3
import os
import main

def GiveHashSalt(password):
    salt=os.urandom(main.size)
    hashedPassword=hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, main.iterations).hex()
    return hashedPassword, salt

def ChangePassword(username, password):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        usernameFromDB = cursor.fetchone()
        if usernameFromDB is None:
            print("No such user")
            return

        hashedPassword, salt = GiveHashSalt(password)
        cursor.execute("UPDATE users SET hashedPassword = ?, salt = ? WHERE username = ?", (hashedPassword, salt, username))