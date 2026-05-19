import json

class CV:
    def __init__(self, data: dict):
        self.data = data
        pass

    @classmethod
    def CVExisting(cls, searchQuery: str):
        with open(f"CV/{searchQuery}.json") as file:
            CV = json.load(file)
            return cls(CV)

    @classmethod
    def CVCreate(cls, name: str, age: int, dob: str, email: str, phone: int, skills: list, education: list, work: list):
        CV = {
            "profile": {
                "Name": name,
                "Age": age,
                "Date of Birth": dob,
                "e-mail": email,
                "Phone Number": phone,
                "Skills": skills,
                "Education": education,
                "Work Experience": work
            }
        }
        try:
            with open(f'CV/{self.name}.json', 'x') as file:
                json.dump(CV, file)
                return cls(CV)
        except FileExistsError:
            print("file already exists")
            return cls.cvExisting(name)

    def CVUpdate(self):
        with open(f'CV/{self.name}.json', 'w') as file:
            json.dump(self.CV, file)