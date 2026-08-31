import sqlite3

def searchFilter(Query: str, Filters: list):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username = '{Query}' AND " + " AND ".join([f"tags LIKE '%{i}%'" for i in Filters]))
        return cursor.fetchall()