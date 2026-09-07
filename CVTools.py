import json
import sqlite3
from DBTools import IsValueValid
from main import projectRootFolder

def GetExistingCV(searchQuery, column: str = 'ID'):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT fileName FROM CVs WHERE {column} = ?', (searchQuery,))
        fileName = cursor.fetchone()[0]
        filePath = projectRootFolder / "CVs" / fileName

    with filePath.open('r') as fileHandler:
        details = json.load(fileHandler)

    return details

def ListOwnedCVs(user: str):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT ID, candidateName FROM CVs WHERE ownerName = ? AND isDeleted = FALSE', (user,))
        AssociatedCVs = dict(cursor.fetchall())
        return AssociatedCVs if AssociatedCVs else 'not found'

def CreateNewCV(ownerName: str, details: dict):
    requiredKeys = ('name',
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

    elementValidities = tuple(
        IsValueValid(k, v)
        for k, v in details.items()
    ) + (
        IsValueValid('owner', ownerName),
    )
    candidateName = details['name']

    if (all(i == 'success' for i in elementValidities)
        and all(key in details for key in requiredKeys)):

            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO CVs (candidateName, ownerName) VALUES (?, ?)',
                               (candidateName, ownerName))

                ID = cursor.lastrowid
                if ID is None:
                    return 'fatal error'

                details = {'ID':ID, 'owner':ownerName, **details}

                formattedName = candidateName.replace(' ', '_')
                fileName = f'{ID:05d}-{formattedName}.json'

                cursor.execute('UPDATE CVs SET fileName = ? WHERE ID = ?', (fileName, ID))
                filePath = projectRootFolder / 'CVs' / fileName

            with filePath.open('w') as fileHandler:
                json.dump(details, fileHandler, indent=4)

            return 'success'

    else:
        return '\n'.join(i for i in elementValidities if i != 'success')

def UpdateExistingCV(ID, details: dict):
    requiredKeys = ('owner',
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

    elementValidities = tuple(IsValueValid(k, v) for k, v in details.items())

    if (all(i == 'success' for i in elementValidities)
        and all(key in details for key in requiredKeys)):

        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT fileName FROM CVs WHERE ID = ?', (ID,))
            fileName = cursor.fetchone()[0]
            filePath = projectRootFolder / "CVs" / fileName

        with filePath.open('w') as fileHandler:
            json.dump(details, fileHandler, indent=4)

        return 'success'

    else:
        return '\n'.join(i for i in elementValidities if i != 'success')

def DeleteCV(ID: int):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT fileName FROM CVs WHERE ID = ?', (ID,))
        result = cursor.fetchone()
        if result is None:
            raise ValueError('CV not found?')

        fileName = result[0]

        CVFolder = projectRootFolder / "CVs"
        DeletedCVsFolder = CVFolder / "Recently Deleted"

        CVPath = CVFolder / fileName
        deletedPath = DeletedCVsFolder / fileName

        CVPath.rename(deletedPath)

        cursor.execute('UPDATE CVs SET isDeleted = TRUE WHERE ID = ?', (ID,))

    if cursor.rowcount == 0:
        raise ValueError('Not found...')

    return 'success'

# details = {
#     'name': 'CNO IZECE',
#     'address': '314P, 15th Street, Dubai',
#     'phoneNo': '3141592653',
#     'nationality': 'Indian',
#     'gender': 'Male',
#     'eduQualifications': ('12 - CBSE - 2026',
#                           'BSc - ??? - 2030',
#                           'MSc - ??? - 2032',
#                           'PhD - MIT - 2040',),
#     'workExperience': ('NA',),
#     'miscAchievements': ('NA',),
#     'skills': ('NA',),
#     'languages': ('English',
#                   'French',
#                   'Malayalam'),
#     'references': ('NA',)
# }
#
# CreateNewCV('tempUser', details)