# Error codes:
# incorrectUN - Incorrect Username passed
# incorrectPW - Incorrect Password passed
# correct - Success
def login(username, password, userDB): #username, password, and the database with users.
    if username not in userDB:
        return 'incorrectUN'
    if password != userDB[username]:
        return 'incorrectPW'
    else:
        return 'correct'