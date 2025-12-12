class Course:
    def __init__(self, course_id, course_name, credits=3):
        self.course_id, self.course_name, self.credits = course_id, course_name, credits

    def __str__(self):
        return f"ID: {self.course_id}, Name: {self.course_name}, Credits: {self.credits}"
