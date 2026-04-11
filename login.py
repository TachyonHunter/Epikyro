# Error codes:
# incorrectUN - Incorrect Username passed
# incorrectPW - Incorrect Password passed
# correct - Success#
# @PreciselyUNkNowN what case scheme do you want to use in this project??
# I was thinking camelCase for variables and functions, and PascalCase for classes, unless we aren't using classes?

def login(username, password, userDB): #username, password, and the database with users.
    if username not in userDB:
        return (0, 'incorrectUN') 
    if password != userDB[username]:
        return (0, 'incorrectPW')
    else:
        return (1, 'correct')

# the 0s and 1s basically make this a boolean function while also being a string function
# so we can use the 0s and 1s to check if the login was successful or not, and the strings to get the specific error messages