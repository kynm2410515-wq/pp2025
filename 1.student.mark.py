def input_number_of_student():
    while True:
        try:
            num = int(input("Enter number of students: "))
            if num > 0:
                return num
            else:
                print("Students cannot be <= 0")
                print("Please enter a positive number")
        except ValueError:
            print("Invalid input")


def input_student_information(num_student):
    students = []
    for i in range(num_student):
        print(f"Enter the information of student {i+1}")
        student_id = input("Enter ID: ")
        student_name = input("Enter your full name: ")
        dob = input("Date of birth (DD/MM/YYYY): ")
        student = {
            'id': student_id,
            'name': student_name,
            'dob': dob
        }
        students.append(student)
    return students

def input_number_of_course():
    while True:
        try:
            num_course = int(input("Enter number of courses: "))
            if num_course > 0:
                return num_course
            else:
                print("Courses cannot be <= 0")
        except ValueError:
            print("Invalid input")

def input_course_information(numcourse):
    courses = []
    for i in range(numcourse):
        print(f"Enter the information of course {i+1}")
        course_id = input("Enter course ID: ")
        course_name = input("Enter the course name: ")
        course = {
            'course id': course_id,
            'course name': course_name
        }
        courses.append(course)
    return courses
     

def list_courses(courses):
    if not courses:
        print("\nNo courses available.")
        print("Please add courses first (Option 3 then Option 4).")
        return
    print("\n=== List of Courses ===")
    for idx, course in enumerate(courses, 1):
        print(f"{idx}. ID: {course['course id']}, Name: {course['course name']}")
    print(f"\nTotal courses: {len(courses)}")

def list_students(students):
    if not students:
        print("\nNo students available.")
        print("Please add students first (Option 1 then Option 2).")
        return
    print("\n=== List of Students ===")
    for idx, student in enumerate(students, 1):
        print(f"{idx}. ID: {student['id']}, Name: {student['name']}, DOB: {student['dob']}")
    print(f"\nTotal students: {len(students)}")

def show_mark(students, courses, marks):
    if not courses:
        print("No courses available, adding first")
        return
    if not students:
        print("No students available, adding first")
        return

    print("List of Courses:")
    for index, course in enumerate(courses):
        print(f"{index + 1}: {course['course name']} (ID: {course['course id']})")

    while True:
        try:
            choice = int(input("Select course num: "))
            if 1 <= choice <= len(courses):
                select_course = courses[choice - 1]
                break
            print(f"Enter a number between 1 and {len(courses)}")
        except ValueError:
            print("Invalid input. Please enter a number.")

    course_id = select_course['course id']
    print(f"Entering marks for course: {select_course['course name']}")

    for student in students:
        while True:
            try:
                mark = float(input(f"Enter mark for {student['name']} (ID: {student['id']}): "))
                if 0 <= mark <= 20:
                    key = (student['id'], course_id)
                    marks[key] = mark
                    break
                else:
                    print("Invalid mark. Please enter a value between 0 and 20.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    print("\n--- Marks for", select_course['course name'], "---")
    has_marks = False
    for student in students:
        key = (student['id'], course_id)
        if key in marks:
            print(f"Student: {student['name']} (ID: {student['id']}) - Mark: {marks[key]}")
            has_marks = True

    if not has_marks:
        print("No marks recorded for this course yet.")

def main():
    s = {'students': [], 'courses': [], 'marks': {}, 'num_s': 0, 'num_c': 0}

    while True:
        c = input("Enter choice: ")

        match c:
            case '1':
                s['num_s'] = input_number_of_student()
                print(f"Number of students set to {s['num_s']}")
            case '2':
                if s['num_s'] == 0:
                    print("Please set the number of students first (Option 1).")
                else:
                    s['students'] = input_student_information(s['num_s'])
                    print(f"Successfully added {len(s['students'])} student(s).")
            case '3':
                s['num_c'] = input_number_of_course()
                print(f"Number of courses set to {s['num_c']}")
            case '4':
                if s['num_c'] == 0:
                    print("Please set the number of courses first (Option 3).")
                else:
                    s['courses'] = input_course_information(s['num_c'])
                    print(f"Successfully added {len(s['courses'])} course(s).")
            case '5':
                list_courses(s['courses'])
            case '6':
                list_students(s['students'])
            case '7':
                show_mark(s['students'], s['courses'], s['marks'])
            case '0':
                print("Exiting program.")
                break
            case _:
                print("Invalid choice, please pick from 0 to 7.")

if __name__ == "__main__":
    main()