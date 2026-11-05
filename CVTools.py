import json
import sqlite3
from DBTools import IsValueValid
from main import projectRootFolder

def GetExistingCV(value, column: str = 'ID'):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT fileName FROM CVs WHERE {column} = ?', (value,))
        data = cursor.fetchone()
        if data:
            fileName = data[0]
            filePath = projectRootFolder / "CVs" / fileName
            with filePath.open('r') as fileHandler:
                details = json.load(fileHandler)
            return details
        else:
            raise ValueError('CV not found.')

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

def GenerateTags(details):
    tags = {'ID': details['ID'],
            'name': details['name'],
            'address': details['address'],
            'nationality': details['nationality'],
            'eduMagnitude': len(details['eduQualifications']),
            'degrees': list(dict.fromkeys([i['degree'] for i in details['eduQualifications']])),
            'organizations': list(dict.fromkeys([i['organization'] for i in details['workExperience']])),
            'skills': list(dict.fromkeys(details['skills'])),
            'languages': list(dict.fromkeys(details['languages'])),
            'achievements': list(dict.fromkeys(details['miscAchievements']))
            }

    totalYearsWorked = sum(
        int(i['tenure'].split('-')[1]) - int(i['tenure'].split('-')[0])
        for i in details['workExperience']
    )

    tags['totalWorkExperience'] = totalYearsWorked
    return tags

def GetTags(ID):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT fileName FROM tags WHERE ID = ?', (ID,))
        results = cursor.fetchone()

        if results is not None:
            tagsFolder = projectRootFolder / "CVs" / "Tags"
            filePath = tagsFolder / results[0]
            with filePath.open('r') as fileHandler:
                tags = json.load(fileHandler)
                return tags
        else:
            raise ValueError('CV not found.')

def CreateTags(tags):
    requiredTags = ('ID',
                    'name',
                    'address',
                    'nationality',
                    'eduMagnitude',
                    'degrees',
                    'organizations',
                    'skills',
                    'languages',
                    'achievements',
                    'totalWorkExperience')

    elementValidities = tuple(IsValueValid(k, v) for k, v in tags.items())

    if (all(i == 'success' for i in elementValidities)
            and all(tag in tags for tag in requiredTags)):

        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            name = tags['name']
            address = tags['address']
            nationality = tags['nationality']
            eduMagnitude = tags['eduMagnitude']
            totalWorkExperience = tags['totalWorkExperience']
            ID = tags['ID']
            fileName = str(ID) + '.json'

            cursor.execute('''INSERT INTO tags (ID,
                                                    name, 
                                                    address, 
                                                    nationality, 
                                                    eduMagnitude, 
                                                    totalWorkExperience,
                                                    fileName) 
                                  VALUES(?, ?, ?, ?, ?, ?, ?)''', (ID,
                                                                          name,
                                                                          address,
                                                                          nationality,
                                                                          eduMagnitude,
                                                                          totalWorkExperience,
                                                                          fileName))
            conn.commit()

        filePath = projectRootFolder / "CVs" / "Tags" / fileName

        with filePath.open('w') as fileHandler:
            json.dump(tags, fileHandler, indent=4)
        return 'success'

    else:
        return '\n'.join(i for i in elementValidities if i != 'success')

def UpdateTags(tags):
    requiredTags = ('ID',
                    'name',
                    'address',
                    'nationality',
                    'eduMagnitude',
                    'degrees',
                    'organizations',
                    'skills',
                    'languages',
                    'achievements',
                    'totalWorkExperience')

    elementValidities = tuple(IsValueValid(k, v) for k, v in tags.items())

    if (all(i == 'success' for i in elementValidities)
            and all(tag in tags for tag in requiredTags)):

        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            name = tags['name']
            address = tags['address']
            nationality = tags['nationality']
            eduMagnitude = tags['eduMagnitude']
            totalWorkExperience = tags['totalWorkExperience']
            ID = tags['ID']

            cursor.execute('''UPDATE tags SET name = ?,
                                                  address = ?,
                                                  nationality = ?,
                                                  eduMagnitude = ?,
                                                  totalWorkExperience = ?
                                  WHERE ID = ?''', (name,
                                                              address,
                                                              nationality,
                                                              eduMagnitude,
                                                              totalWorkExperience,
                                                              ID))
            conn.commit()

            fileName = cursor.execute("SELECT fileName FROM tags WHERE ID = ?", (ID,)).fetchone()[0]

        filePath = projectRootFolder / "CVs" / "Tags" / fileName

        with filePath.open('w') as fileHandler:
            json.dump(tags, fileHandler, indent=4)
        return 'success'

    else:
        return '\n'.join(i for i in elementValidities if i != 'success')

def SearchForCVs(criteria):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()

        # queryCriteria = ' AND '.join(
        #     f'{k} = ?'
        #     for k in criteria
        #     if k not in (
        #         'degrees',
        #         'organizations',
        #         'skills',
        #         'languages',
        #         'achievements'
        #     )
        # )
        #
        # values = tuple(
        #     v
        #     for k, v in criteria.items()
        #     if k not in (
        #         'degrees',
        #         'organizations',
        #         'skills',
        #         'languages',
        #         'achievements'
        #     )
        # )
        #
        # query = 'SELECT ID, candidateName FROM CVs'
        # if queryCriteria:
        #     query += ' WHERE ' + queryCriteria

        cursor.execute('''SELECT ID, 
                              name, 
                              address, 
                              nationality, 
                              eduMagnitude, 
                              totalWorkExperience, 
                              fileName FROM tags''')

        records = cursor.fetchall()

    candidateCVs = {record[0]:record for record in records}
    for record in records:
        ID = record[0]
        name = record[1].strip().lower()
        address = record[2].strip().lower()
        nationality = record[3].strip().lower()
        eduMagnitude = record[4]
        totalWorkExperience = record[5]
        if 'candidateName' in criteria.keys():
            if name != criteria['candidateName'].lower():
                del candidateCVs[ID]

        if 'address' in criteria.keys():
            if address != criteria['address'].lower():
                del candidateCVs[ID]

        if 'nationality' in criteria.keys():
            if nationality != criteria['nationality'].lower():
                del candidateCVs[ID]

        if 'eduMagnitude' in criteria.keys():
            if eduMagnitude < criteria['eduMagnitude']:
                del candidateCVs[ID]

        if 'totalWorkExperience' in criteria.keys():
            if totalWorkExperience < criteria['totalWorkExperience']:
                del candidateCVs[ID]

        if 'degrees' in criteria.keys():
            if eduMagnitude == 0:
                del candidateCVs[ID]

        if 'organizations' in criteria.keys():
            if totalWorkExperience == 0:
                del candidateCVs[ID]

    CVs = {record[0]:record[1] for record in candidateCVs.values()}

    if any(key in criteria for key in ('degrees', 'organizations', 'skills', 'languages', 'achievements')):
        for ID, candidate in candidateCVs.items():
            ID = candidate[0]
            CV = GetExistingCV(ID)
            degrees = [eduQualification['degree'].strip().lower() for eduQualification in CV['eduQualifications']]
            organizations = [job['organization'].strip().lower() for job in CV['workExperience']]
            skills = [i.strip().lower() for i in CV['skills']]
            languages = [i.strip().lower() for i in CV['languages']]
            achievements = [i.strip().lower() for i in CV['miscAchievements']]

            if 'degrees' in criteria.keys():
                if not any(degree in [i.strip().lower() for i in criteria['degrees']] for degree in degrees):
                    del CVs[ID]

            if 'organizations' in criteria.keys():
                if not any(org in [i.strip().lower() for i in criteria['degrees']] for org in organizations):
                    del CVs[ID]

            if 'skills' in criteria.keys():
                if not any(skill in [i.strip().lower() for i in criteria['skills']] for skill in skills):
                    del CVs[ID]

            if 'languages' in criteria.keys():
                if not any(language in [i.strip().lower() for i in criteria['languages']] for language in languages):
                    del CVs[ID]

            if 'achievements' in criteria.keys():
                if not any(achievement in [i.strip().lower() for i in criteria['achievements']] for achievement in achievements):
                    del CVs[ID]

    return CVs

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