import json

class CV:
    def __init__(self, name: str, age: int, dob: str, email: str, phone: int, skills: list, education: list, work: list):
        self.name = name
        self.age = age
        self.dob = dob
        self.email = email
        self.phone = phone
        self.skills = skills
        self.education = education
        self.work = work

        self.CV={
            "profile":{
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

    def cvCreate(self):
        try:
            with open(f'CV/{self.name}.json', 'x') as file:
                json.dump(self.CV, file)
        except FileExistsError:
            print("file already exists")

    def cvUpdate(self):
        with open(f'CV/{self.name}.json', 'w') as file:
            json.dump(self.CV, file)