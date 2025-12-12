class Student:
    def __init__(self, student_id, name, dob):
        self.id, self.name, self.dob = student_id, name, dob

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, DOB: {self.dob}"
