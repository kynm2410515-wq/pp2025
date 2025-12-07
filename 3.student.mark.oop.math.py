import math
import numpy as np
import curses
from curses import wrapper
from curses.textpad import rectangle

class Student:
    def __init__(self, student_id, name, dob):
        self.id, self.name, self.dob = student_id, name, dob

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, DOB: {self.dob}"


class Course:
    def __init__(self, course_id, course_name, credits=3):
        self.course_id, self.course_name, self.credits = course_id, course_name, credits

    def __str__(self):
        return f"ID: {self.course_id}, Name: {self.course_name}, Credits: {self.credits}"

class StudentManagementSystem:
    def __init__(self, stdscr=None):
        self.students, self.courses, self.marks = [], [], {}
        self.stdscr = stdscr
        if stdscr:
            self.setup_colors()

    def setup_colors(self):
        """Initialize color pairs for decorative UI"""
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)      # title
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)     # menu 
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)    # highlight
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)       # errora
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)      # select
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)   # status 

    def draw_title(self, title):
        """Draw a decorated title banner"""
        height, width = self.stdscr.getmaxyx() #screen dimension
        self.stdscr.attron(curses.color_pair(1) | curses.A_BOLD) #enable text styling 
        self.stdscr.addstr(0, 0, "=" * width) #drawing top border
        title_text = f" {title} "          
        x = (width - len(title_text)) // 2 
        self.stdscr.addstr(1, x, title_text) 
        self.stdscr.addstr(2, 0, "=" * width) #draww bottom border
        self.stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)  #disable styling

    def draw_box(self, y, x, height, width, title=""):
       
        rectangle(self.stdscr, y, x, y + height - 1, x + width - 1) 
        if title:
            title_text = f" {title} "
            title_x = x + (width - len(title_text)) // 2   #horizontal position for title
            self.stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
            self.stdscr.addstr(y, title_x, title_text) #draw text on screen
            self.stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)

    def draw_status_bar(self, message):
       
        height, width = self.stdscr.getmaxyx()
        self.stdscr.attron(curses.color_pair(6))
        self.stdscr.addstr(height - 1, 0, " " * width)
        self.stdscr.addstr(height - 1, 2, message[:width-4])
        self.stdscr.attroff(curses.color_pair(6))

    def get_input(self, prompt, y, x, width=30):
        """Get user input with a decorated input box"""
        curses.echo()
        curses.curs_set(1)
        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(y, x, prompt)
        self.stdscr.attroff(curses.color_pair(2))
        input_y, input_x = y, x + len(prompt) + 1
        self.draw_box(input_y - 1, input_x - 1, 3, width + 2)
        self.stdscr.move(input_y, input_x)
        self.stdscr.refresh()
        user_input = self.stdscr.getstr(input_y, input_x, width).decode('utf-8')

        curses.noecho()
        curses.curs_set(0)
        return user_input

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
            while True:
                try:
                    credits = int(input("Credits: "))
                    if credits > 0:
                        break
                    print("Credits must > 0")
                except ValueError:
                    print("Invalid input")
            self.courses.append(Course(cid, cname, credits))
        print(f"Added {num} course(s).")

    def list_items(self, items, title):
        if not items:
            return print(f" No {title.lower()} available.")
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
                        mark = math.floor(mark * 10) / 10
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

    def calculate_gpa(self, student):
        if not self.courses:
            return 0.0
        marks_array = []
        credits_array = []
        for course in self.courses:
            key = (student.id, course.course_id)
            if key in self.marks:
                marks_array.append(self.marks[key])
                credits_array.append(course.credits)

        if not marks_array:
            return 0.0

        marks_np = np.array(marks_array)
        credits_np = np.array(credits_array)

        weighted_sum = np.sum(marks_np * credits_np)
        total_credits = np.sum(credits_np)

        return weighted_sum / total_credits if total_credits > 0 else 0.0

    def show_student_gpa(self):
        if not self.students:
            return print("No students available.")
        print("\nGPA:")
        for student in self.students:
            gpa = self.calculate_gpa(student)
            print(f"{student.name} (ID: {student.id}): GPA = {gpa:.2f}")

    def sort_students_by_gpa(self):
        if not self.students:
            return print("No students available.")
        student_gpa_list = [(student, self.calculate_gpa(student)) for student in self.students]
        student_gpa_list.sort(key=lambda x: x[1], reverse=True)
        print("\n sorted by GPA:")
        for rank, (student, gpa) in enumerate(student_gpa_list, 1):
            print(f"{rank}. {student.name} (ID: {student.id}): GPA = {gpa:.2f}")

    def run_curses(self):
        """Run the system with curses-decorated UI"""
        current_row = 0
        menu_options = [
            "Input students",
            "Input courses",
            "List students",
            "List courses",
            "Input marks",
            "Show student GPAs",
            "Sort students by GPA",
            "Exit"
        ]

        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            self.draw_title("STUDENT MANAGEMENT SYSTEM")
            menu_start_y = 5
            menu_height = len(menu_options) + 4
            menu_width = 50
            menu_x = (width - menu_width) // 2
            self.draw_box(menu_start_y, menu_x, menu_height, menu_width, "MAIN MENU")

            for idx, option in enumerate(menu_options):
                y = menu_start_y + idx + 2
                x = menu_x + 5

                if idx == current_row:
                    self.stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
                    self.stdscr.addstr(y, x, f"> {idx + 1}. {option}".ljust(menu_width - 10))
                    self.stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
                else:
                    self.stdscr.attron(curses.color_pair(2))
                    self.stdscr.addstr(y, x, f"  {idx + 1}. {option}")
                    self.stdscr.attroff(curses.color_pair(2))

            self.draw_status_bar(" Students: {} | Courses: {}".format(
                len(self.students), len(self.courses)))

            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
                current_row += 1
            elif key == ord('\n'):  
                if current_row == len(menu_options) - 1:  
                    break
                else:
                    self.handle_menu_selection(current_row)

    def handle_menu_selection(self, selection):
        """Handle menu selections with curses UI"""
        self.stdscr.clear()
        self.draw_title("STUDENT MANAGEMENT SYSTEM")
        actions = [
            self.input_students,
            self.input_courses,
            self.list_students,
            self.list_courses,
            self.input_marks,
            self.show_student_gpa,
            self.sort_students_by_gpa
        ]

        if selection < len(actions):
            actions[selection]()
            self.draw_status_bar("Press any key to continue...")
            self.stdscr.getch()

    def run(self):
        actions = {
            '1': self.input_students,
            '2': self.input_courses,
            '3': self.list_students,
            '4': self.list_courses,
            '5': self.input_marks,
            '6': self.show_student_gpa,
            '7': self.sort_students_by_gpa
        }

        while True:
            print("\n--- Menu ---")
            print("1. Input students")
            print("2. Input courses")
            print("3. List students")
            print("4. List courses")
            print("5. Input marks")
            print("6. Show student GPAs")
            print("7. Sort students by GPA")
            print("0. Exit")
            choice = input("Enter choice: ")
            if choice == '0':
                print("Exiting.")
                break
            elif choice in actions:
                actions[choice]()
            else:
                print("Invalid choice.")

def main(stdscr):
    """Main function to run with curses"""
    curses.curs_set(0)  # hide cursor
    stdscr.keypad(True)  # kaypad mode for arrow keys

    system = StudentManagementSystem(stdscr)
    system.run_curses()

if __name__ == "__main__":
    wrapper(main)
