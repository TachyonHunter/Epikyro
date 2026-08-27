import sqlite3
from datetime import datetime
from passwordFunctions import GiveHashSalt


# Function returning a list of users from our database.
def ListUsers(skipAdmins: bool = False):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        if skipAdmins:
            cursor.execute("SELECT username FROM users WHERE isDeleted = 0 AND designation != 'admin'")
        else:
            cursor.execute("SELECT username FROM users WHERE isDeleted = 0")
        users = [i[0] for i in cursor.fetchall()]
    return users

# Function deleting a user and returning its relevant data.
def DeleteUser(user: str):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET isDeleted = TRUE WHERE username = ?", (user,))
        return 'success'
    except Exception as e:
        return str(e)

# Function retrieving user details for a given user.
def RetrieveUserDetails(user: str,
                        detailsToRetrieve: tuple = ('firstName', 'lastName', 'email', 'designation', 'DOB', 'DOJoining')):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            columns = ', '.join(detailsToRetrieve)
            cursor.execute(f"SELECT {columns} FROM users WHERE username = ?", (user,))
            userDetails = dict(zip(detailsToRetrieve, cursor.fetchone()))
        return userDetails
    except TypeError:
        print("User not found")
        return 'not found'

# Function updating all given columns with new values for a given user.
def UpdateUserDetails(user: str, details: dict):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            setClause = ", ".join(f"{k} = ?" for k in details.keys())
            cursor.execute(f"""
                           UPDATE users
                           SET {setClause}
                           WHERE username = ?
                           """, tuple(v for v in details.values())+(user,))
        return 'success'
    except Exception as e:
        return str(e)

# Function to add new users to the DB.
def AddUser(details: dict):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()

            password = details['password']
            hashedPassword, salt = GiveHashSalt(password)
            del details['password']
            details['hashedPassword'] = hashedPassword
            details['salt'] = salt
            details['isDeleted'] = False

            columns = ', '.join(details.keys())
            valuePlaceholders = ', '.join('?' for _ in details.keys())
            cursor.execute(f'INSERT INTO users ({columns}) VALUES ({valuePlaceholders})', tuple(details.values()))
        return 'success'
    except Exception as e:
        return str(e)

def GetValueFromUser(username: str, column: str):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {column} FROM users WHERE username = ?", (username,))
            return cursor.fetchone()[0]
    except Exception as e:
        return str(e)

def IsValueValid(valueType: str, value) -> str:
    supportedTypes = ('username',
                      'password',
                      'firstName',
                      'lastName',
                      'email',
                      'designation',
                      'DOB',
                      'DOJoining',
                      'name',
                      'address',
                      'phoneNo',
                      'nationality',
                      'gender',
                      'eduQualifications',
                      'workExperience',
                      'miscAchievements',
                      'skills',
                      'languages',
                      'references')

    # Below code handles invalidity.
    if valueType not in supportedTypes:
        return 'Unsupported.'
    elif valueType in ('username', 'address'):
        if not value.isalnum():
            return f'Invalid value provided for {valueType}.'
    elif valueType == 'password':
        if not (
                len(value) >= 8 and
                any(i.isupper() for i in value) and
                any(i.islower() for i in value) and
                any(i.isdigit() for i in value) and
                any(not i.isalnum() for i in value)
        ):
            return 'Weak password provided.'
    elif valueType in ('firstName',
                       'lastName',
                       'name',
                       'designation',
                       'nationality',
                       'gender',
                       'candidateName',
                       'ownerName'):
        if not value.isalpha():
            return f'Invalid value provided for {valueType}.'
    elif valueType == 'email':
        user, sep, domain = value.partition('@')
        if not (
                value.count('@') == 1 and
                user and
                domain and
                domain.count('.') == 1 and
                domain[0] != '.' and
                domain[-1] != '.'
        ):
           return 'Invalid email address.'
    elif valueType in ('DOB', 'DOJoining'):
        try:
            datetime.strptime(value, '%d-%m-%Y')
            return 'success'
        except ValueError:
            return f'Invalid date provided for {valueType}.'
    elif valueType == 'phoneNo':
        if value.isdigit() and len(value) == 10:
            return 'Invalid phone number.'
    elif valueType in ('eduQualifications',
                       'workExperience',
                       'miscAchievements',
                       'skills',
                       'languages',
                       'references'):
        if not(isinstance(value, tuple) and all(isinstance(i, str) for i in value)):
            return f'Invalid value provided for {valueType}.'
    return 'success' # If checks passed.