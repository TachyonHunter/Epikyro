import login as lgn
import sqlite3
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
#cursor.execute(f"INSERT INTO users (username, password) VALUES ({username}, {password})")