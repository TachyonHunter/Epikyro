# Error codes:
# incorrectUN - Incorrect Username passed
# incorrectPW - Incorrect Password passed
# correct - Success#
# @PreciselyUNkNowN what case scheme do you want to use in this project??
# I was thinking camelCase for variables and functions, and PascalCase for classes, unless we aren't using classes?
def login(username, password, userDB): #username, password, and the database with users.
    if username not in userDB:
        return 'incorrectUN'
    if password != userDB[username]:
        return 'incorrectPW'
    else:
        return 'correct'