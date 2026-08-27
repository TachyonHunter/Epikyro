import json
import sqlite3
import pathlib
from DBTools import IsValueValid
from main import projectRootFolder

def GetExistingCV(searchQuery: str, column: str):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT fileName FROM CVs WHERE {column} = ?', (searchQuery,))
            fileName = cursor.fetchone()[0]
            filePath = projectRootFolder / "CVs" / fileName

        with filePath.open('r') as fileHandler:
            details = json.load(fileHandler)

        return details
    except Exception as e:
        return str(e)

def ListOwnedCVs(user: str):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ID, candidateName FROM CVs WHERE ownerName = ? AND isDeleted = FALSE', (user,))
            AssociatedCVs = dict(cursor.fetchall())
            return AssociatedCVs if AssociatedCVs else 'not found'
    except Exception as e:
        return str(e)

def CreateNewCV(candidateName: str, ownerName: str, details: dict):
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
        IsValueValid('candidateName', ownerName),
        IsValueValid('ownerName', candidateName)
    )

    if (all(i == 'success' for i in elementValidities)
        and all(key in details for key in requiredKeys)):

        try:
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO CVs (candidateName, ownerName) VALUES (?, ?)',
                               (candidateName, ownerName))

                ID = cursor.lastrowid
                if ID is None:
                    return 'fatal error'

                details['ID'] = ID

                formattedName = candidateName.replace(' ', '_')
                fileName = f'{ID:05d}-{formattedName}.json'

                cursor.execute('UPDATE CVs SET fileName = ? WHERE ID = ?', (fileName, ID))
                filePath = projectRootFolder / 'CVs' / fileName

            with filePath.open('w') as fileHandler:
                json.dump(details, fileHandler, indent=4)

            return 'success'
        except Exception as e:
            return str(e)

    else:
        return 'invalid value'

def UpdateExistingCV(details: dict):
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

    elementValidities = tuple(IsValueValid(k, v) for k, v in details.items())

    if (all(i == 'success' for i in elementValidities)
        and all(key in details for key in requiredKeys)):

        try:
            ID = details['ID']
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT fileName FROM CVs WHERE ID = ?', (ID,))
                fileName = cursor.fetchone()[0]
                filePath = projectRootFolder / "CVs" / fileName

            with filePath.open('w') as fileHandler:
                json.dump(details, fileHandler, indent=4)

            return 'success'
        except Exception as e:
            return str(e)

    else:
        return 'invalid value'

def DeleteCV(ID: int):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT fileName FROM CVs WHERE ID = ?', (ID,))
            result = cursor.fetchone()
            if result is None:
                return 'not found'

            fileName = result[0]

            CVFolder = projectRootFolder / "CVs"
            DeletedCVsFolder = CVFolder / "Recently Deleted"

            CVPath = CVFolder / fileName
            deletedPath = DeletedCVsFolder / fileName

            CVPath.rename(deletedPath)

            cursor.execute('UPDATE CVs SET isDeleted = TRUE WHERE ID = ?', (ID,))

    except Exception as e:
        return str(e)