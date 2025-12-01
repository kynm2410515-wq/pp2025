class Student:
    def __init__(self, student_id, name, dob):
        self.id, self.name, self.dob = student_id, name, dob

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, DOB: {self.dob}"


class Course:
    def __init__(self, course_id, course_name):
        self.course_id, self.course_name = course_id, course_name

    def __str__(self):
        return f"ID: {self.course_id}, Name: {self.course_name}"

class StudentManagementSystem:
    def __init__(self):
        self.students, self.courses, self.marks = [], [], {}

    def get_positive_int(self, prompt):
        while True:
            try:
                num = int(input(prompt))
                if num > 0:
                    return num
                print("Must be > 0")
            except ValueError:
                print("Invalid input")

    def input_students(self):
        num = self.get_positive_int(" number of students: ")
        self.students = []
        for i in range(num):
            print(f"Student {i+1}:")
            sid = input(" ID: ")
            name = input(" full name: ")
            dob = input("DOB: ")
            self.students.append(Student(sid, name, dob))
        print(f"Added {num} student(s).")

    def input_courses(self):
        num = self.get_positive_int("Enter number of courses: ")
        self.courses = []
        for i in range(num):
            print(f"Course {i+1}:")
            cid = input("Course ID: ")
            cname = input("Course name: ")
            self.courses.append(Course(cid, cname))
        print(f"Added {num} course(s).")

    def list_items(self, items, title):
        if not items:
            return print(f"\nNo {title.lower()} available.")
        print(f"\n {title}")
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")
        print(f"Total: {len(items)}")

    def list_students(self):
        self.list_items(self.students, "Students")

    def list_courses(self):
        self.list_items(self.courses, "Courses")

    def input_marks(self):
        if not self.courses or not self.students:
            return print("Add courses and students first.")

        for index, course in enumerate(self.courses, 1):
            print(f"{index}: {course.course_name}")

        choice = self.get_positive_int("Select course num: ")
        while choice > len(self.courses):
            choice = self.get_positive_int(f"Enter 1-{len(self.courses)}: ")

        course = self.courses[choice - 1]
        print(f"Marks for {course.course_name}:")

        for student in self.students:
            while True:
                try:
                    mark = float(input(f"{student.name}: "))
                    if 0 <= mark <= 20:
                        self.marks[(student.id, course.course_id)] = mark
                        break
                    print("Enter 0-20")
                except ValueError:
                    print("Invalid input")

        print(f"\n {course.course_name} marks")
        for student in self.students:
            key = (student.id, course.course_id)
            if key in self.marks:
                print(f"{student.name} (ID: {student.id}): {self.marks[key]}")

    def run(self):
        actions = {
            '1': self.input_students,
            '2': self.input_courses,
            '3': self.list_students,
            '4': self.list_courses,
            '5': self.input_marks 
        }

        while True:
            choice = input("Enter choice ")
            if choice == '0':
                print("Exiting.")
                break
            elif choice in actions:
                actions[choice]()
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    system = StudentManagementSystem()
    system.run()
