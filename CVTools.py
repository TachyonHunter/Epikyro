import json
import sqlite3


# class CVs:
#     def __init__(self, data: dict):
#         self.data = data
#         self.ID = data['ID']
#
#     @classmethod
#     def ReturnExistingCV(cls, searchQuery: str):
#         try:
#             with open(f"CV/{searchQuery}.json") as file:
#                 CV = json.load(file)
#                 return cls(CV)
#         except:
#             return 'not found'
#
#     @classmethod
#     def CreateNewCV(cls, employee, details):
#         ID = f'0001_{details["name"]}'
#         CVData = {
#             "employee": employee,
#             "ID": ID,
#             "profile": details
#         }
#         try:
#             with open(f'CV/{ID}.json', 'x') as fHandler:
#                 json.dump(CVData, fHandler)
#                 return cls(CVData)
#         except FileExistsError:
#             print("file already exists")
#             ExistingCV = cls.ReturnExistingCV(ID)
#             if ExistingCV.data == CVData:
#                 print("Same file.")
#                 return ExistingCV
#             else:
#                 print("Assigning new ID as data was not found to be the same.")
#                 CVData['ID'] = f'0002_{details["name"]}'
#
#     def UpdateCV(self):
#         with open(f'CV/{self.name}.json', 'w') as file:
#             json.dump(self.data, file)

def GetExistingCV(searchQuery, column):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT ID FROM CVs WHERE {column} = ?', (searchQuery,))
        return cursor.fetchall()

def ListOwnedCVs(user):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT ID, candidateName FROM CVs WHERE ownerName = ?', (user,))
        AssociatedCVs = dict(cursor.fetchall())
        return AssociatedCVs if AssociatedCVs else 'not found'