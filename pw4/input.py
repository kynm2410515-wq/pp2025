import math
from domains import Student, Course


def get_positive_int(prompt, stdscr=None, output_module=None, y=5):
    """Get positive integer input - works with both curses and regular mode"""
    while True:
        try:
            if stdscr and output_module:
                user_input = output_module.get_input(stdscr, prompt, y, 5, 20)
                num = int(user_input)
            else:
                num = int(input(prompt))
            if num > 0:
                return num
            if stdscr and output_module:
                output_module.draw_status_bar(stdscr, "Must be > 0. Press any key...")
                stdscr.getch()
            else:
                print("Must be > 0")
        except ValueError:
            if stdscr and output_module:
                output_module.draw_status_bar(stdscr, "Invalid input. Press any key...")
                stdscr.getch()
            else:
                print("Invalid input")


def input_students(students, stdscr=None, output_module=None):
    """Input student information"""
    if stdscr and output_module:
        num = get_positive_int("Number of students:", stdscr, output_module, 5)
        students.clear()
        for i in range(num):
            y_offset = 8 + (i * 12)
            stdscr.addstr(y_offset, 5, f"Student {i+1}:")
            stdscr.refresh()
            sid = output_module.get_input(stdscr, "ID:", y_offset + 2, 5, 25)
            name = output_module.get_input(stdscr, "Name:", y_offset + 5, 5, 35)
            dob = output_module.get_input(stdscr, "DOB:", y_offset + 8, 5, 25)
            students.append(Student(sid, name, dob))
        output_module.draw_status_bar(stdscr, f"Added {num} student(s). Press any key...")
        stdscr.getch()
    else:
        num = get_positive_int("Number of students: ")
        students.clear()
        for i in range(num):
            print(f"Student {i+1}:")
            sid = input(" ID: ")
            name = input(" Full name: ")
            dob = input(" DOB: ")
            students.append(Student(sid, name, dob))
        print(f"Added {num} student(s).")


def input_courses(courses, stdscr=None, output_module=None):
    """Input course information"""
    if stdscr and output_module:
        num = get_positive_int("Number of courses:", stdscr, output_module, 5)
        courses.clear()
        for i in range(num):
            y_offset = 8 + (i * 12)
            stdscr.addstr(y_offset, 5, f"Course {i+1}:")
            stdscr.refresh()
            cid = output_module.get_input(stdscr, "Course ID:", y_offset + 2, 5, 25)
            cname = output_module.get_input(stdscr, "Course name:", y_offset + 5, 5, 35)
            credits = get_positive_int("Credits:", stdscr, output_module, y_offset + 8)
            courses.append(Course(cid, cname, credits))
        output_module.draw_status_bar(stdscr, f"Added {num} course(s). Press any key...")
        stdscr.getch()
    else:
        num = get_positive_int("Enter number of courses: ")
        courses.clear()
        for i in range(num):
            print(f"Course {i+1}:")
            cid = input("Course ID: ")
            cname = input("Course name: ")
            while True:
                try:
                    credits = int(input("Credits: "))
                    if credits > 0:
                        break
                    print("Credits must > 0")
                except ValueError:
                    print("Invalid input")
            courses.append(Course(cid, cname, credits))
        print(f"Added {num} course(s).")


def input_marks(students, courses, marks, stdscr=None, output_module=None):
    """Input marks for students in a course"""
    if stdscr and output_module:
        if not courses or not students:
            stdscr.addstr(5, 5, "Add courses and students first.")
            stdscr.refresh()
            return

        y = 5
        output_module.draw_highlight(stdscr, y, 5, "Select Course:")
        y += 2
        for index, course in enumerate(courses, 1):
            stdscr.addstr(y, 5, f"{index}: {course.course_name}")
            y += 1
        stdscr.refresh()

        choice = get_positive_int("Enter course number:", stdscr, output_module, y + 1)
        while choice > len(courses):
            output_module.draw_status_bar(stdscr, f"Enter 1-{len(courses)}. Press any key...")
            stdscr.getch()
            choice = get_positive_int("Enter course number:", stdscr, output_module, y + 1)

        course = courses[choice - 1]
        stdscr.clear()
        output_module.draw_title(stdscr, "STUDENT MANAGEMENT SYSTEM")
        stdscr.addstr(5, 5, f"Enter marks for: {course.course_name}")
        stdscr.refresh()

        y = 8
        for student in students:
            while True:
                try:
                    mark_str = output_module.get_input(stdscr, f"{student.name}:", y, 5, 10)
                    mark = float(mark_str)
                    if 0 <= mark <= 20:
                        mark = math.floor(mark * 10) / 10
                        marks[(student.id, course.course_id)] = mark
                        y += 3
                        break
                    output_module.draw_status_bar(stdscr, "Enter 0-20. Press any key...")
                    stdscr.getch()
                except ValueError:
                    output_module.draw_status_bar(stdscr, "Invalid input. Press any key...")
                    stdscr.getch()

        output_module.draw_status_bar(stdscr, f"Marks saved for {course.course_name}. Press any key...")
        stdscr.getch()
    else:
        if not courses or not students:
            return print("Add courses and students first.")

        for index, course in enumerate(courses, 1):
            print(f"{index}: {course.course_name}")

        choice = get_positive_int("Select course num: ")
        while choice > len(courses):
            choice = get_positive_int(f"Enter 1-{len(courses)}: ")

        course = courses[choice - 1]
        print(f"Marks for {course.course_name}:")

        for student in students:
            while True:
                try:
                    mark = float(input(f"{student.name}: "))
                    if 0 <= mark <= 20:
                        mark = math.floor(mark * 10) / 10
                        marks[(student.id, course.course_id)] = mark
                        break
                    print("Enter 0-20")
                except ValueError:
                    print("Invalid input")

        print(f"\n {course.course_name} marks")
        for student in students:
            key = (student.id, course.course_id)
            if key in marks:
                print(f"{student.name} (ID: {student.id}): {marks[key]}")
