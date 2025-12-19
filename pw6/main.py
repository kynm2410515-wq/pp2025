import curses
import os
import pickle
import gzip
from curses import wrapper

from domains import Student, Course
import input as input_module
import output as output_module


DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DATA_DIR, "students.dat")


def save_data_pickle(students, courses, marks):
    """Save students, courses, and marks using pickle with gzip compression"""
    data = {
        'students': students,
        'courses': courses,
        'marks': marks
    }

    try:
        with gzip.open(DATA_FILE, 'wb') as f:
            pickle.dump(data, f)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


def load_data_pickle():
    """Load students, courses, and marks from pickle with gzip compression"""
    students = []
    courses = []
    marks = {}

    if not os.path.exists(DATA_FILE):
        return students, courses, marks

    try:
        with gzip.open(DATA_FILE, 'rb') as f:
            data = pickle.load(f)
            students = data.get('students', [])
            courses = data.get('courses', [])
            marks = data.get('marks', {})
    except Exception as e:
        print(f"Error loading data: {e}")

    return students, courses, marks


class StudentManagementSystem:
    def __init__(self, stdscr=None):
        self.students = []
        self.courses = []
        self.marks = {}
        self.stdscr = stdscr
        if stdscr:
            output_module.setup_colors()

    def load_data(self):
        """Load data from students.dat if it exists"""
        if os.path.exists(DATA_FILE):
            self.students, self.courses, self.marks = load_data_pickle()
            return True
        return False

    def save_data(self):
        """Save data using pickle with compression"""
        save_data_pickle(self.students, self.courses, self.marks)

    def run_curses(self):
        """Run the system with curses-decorated UI"""
        # Load existing data on startup
        if self.load_data():
            output_module.draw_status_bar(self.stdscr, "Data loaded from students.dat. Press any key...")
            self.stdscr.getch()

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
            output_module.draw_menu(self.stdscr, current_row, menu_options,
                                    self.students, self.courses)

            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
                current_row += 1
            elif key == ord('\n'):
                if current_row == len(menu_options) - 1:  # Exit
                    self.save_data()
                    break
                else:
                    self.handle_menu_selection(current_row)

    def handle_menu_selection(self, selection):
        """Handle menu selections with curses UI"""
        self.stdscr.clear()
        output_module.draw_title(self.stdscr, "STUDENT MANAGEMENT SYSTEM")

        if selection == 0:
            input_module.input_students(self.students, self.stdscr, output_module)
        elif selection == 1:
            input_module.input_courses(self.courses, self.stdscr, output_module)
        elif selection == 2:
            output_module.list_students(self.stdscr, self.students)
        elif selection == 3:
            output_module.list_courses(self.stdscr, self.courses)
        elif selection == 4:
            input_module.input_marks(self.students, self.courses, self.marks,
                                     self.stdscr, output_module)
        elif selection == 5:
            output_module.show_student_gpa(self.stdscr, self.students,
                                           self.courses, self.marks)
        elif selection == 6:
            output_module.sort_students_by_gpa(self.stdscr, self.students,
                                               self.courses, self.marks)

        output_module.draw_status_bar(self.stdscr, "Press any key to continue...")
        self.stdscr.getch()

    def run(self):
        """Run in console mode (non-curses)"""
        # Load existing data on startup
        if self.load_data():
            print("Data loaded from students.dat")
            print(f"  Loaded {len(self.students)} students, {len(self.courses)} courses, {len(self.marks)} marks")

        while True:
            print("\n1. Input students")
            print("2. Input courses")
            print("3. List students")
            print("4. List courses")
            print("5. Input marks")
            print("6. Show student GPAs")
            print("7. Sort students by GPA")
            print("0. Exit")
            choice = input("Enter choice: ")

            if choice == '0':
                self.save_data()
                print("Data compressed to students.dat. Exiting.")
                break
            elif choice == '1':
                input_module.input_students(self.students)
            elif choice == '2':
                input_module.input_courses(self.courses)
            elif choice == '3':
                output_module.list_students(None, self.students)
            elif choice == '4':
                output_module.list_courses(None, self.courses)
            elif choice == '5':
                input_module.input_marks(self.students, self.courses, self.marks)
            elif choice == '6':
                output_module.show_student_gpa(None, self.students,
                                               self.courses, self.marks)
            elif choice == '7':
                output_module.sort_students_by_gpa(None, self.students,
                                                   self.courses, self.marks)
            else:
                print("Invalid choice.")


def main(stdscr):
    """Main function to run with curses"""
    curses.curs_set(0)  # hide cursor
    stdscr.keypad(True)  # keypad mode for arrow keys

    system = StudentManagementSystem(stdscr)
    system.run_curses()


if __name__ == "__main__":
    wrapper(main)
