import json

class CVs:
    def __init__(self, data: dict):
        self.data = data
        self.name = data['name']

    @classmethod
    def ReturnExistingCV(cls, searchQuery: str):
        try:
            with open(f"CV/{searchQuery}.json") as file:
                CV = json.load(file)
                return cls(CV)
        except:
            return 'not found'

    @classmethod
    def CreateNewCV(cls, employee, details):
        CVData = {
            "employee": employee,
            "ID": ID,
            "profile": details
        }
        try:
            with open(f'CV/{name}.json', 'x') as fHandler:
                json.dump(CVData, fHandler)
                return cls(CV)
        except FileExistsError:
            print("file already exists")
            return cls.ReturnExistingCV(name)

    def UpdateCV(self):
        with open(f'CV/{self.name}.json', 'w') as file:
            json.dump(self.CV, file)