import hashlib
import sqlite3
import os
import main

def HashSaltSignUp(password):
    salt=os.urandom(main.size)
    passwordHash=hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, main.iterations).hex()
    return passwordHash, salt


def signUp(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE name = ?", (username,))
    usernameDB = cursor.fetchone()
    if usernameDB is not None:
        print("Username is already taken")
        return

    passwordHash, salt = HashSaltSignUp(password)
    cursor.execute("INSERT INTO users (name, password, salt) VALUES (?, ?, ?)", (username, passwordHash, salt))

    conn.commit()
    cursor.close()
    conn.close()