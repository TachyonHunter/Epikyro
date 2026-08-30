import sqlite3
# welcomeNotification.set(f'Welcome {username.get()}!')
#             loginButton.grid_remove()
#             switchAccountButton.grid(row=0, column=0, sticky='E', padx=(0,4))
#             logOutButton.grid(row=0, column=1, sticky='E')
#             if GetValueFromUser(username.get(), 'designation') == 'admin':
#                 adminFrame.grid(row=0, column=1, sticky='E', padx=(0, 4))
#                 headerFrame.columnconfigure(1, weight=1)
#                 generalFrame.grid_remove()
#             else:
#                 generalFrame.grid(row=0, column=1, sticky='E', padx=(0, 4))
#                 headerFrame.columnconfigure(1, weight=1)
#                 adminFrame.grid_remove()


def searchFilter(Query: str, Filters: list):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username = '{Query}' AND " + " AND ".join([f"tags LIKE '%{i}%'" for i in Filters]))
        return cursor.fetchall()
