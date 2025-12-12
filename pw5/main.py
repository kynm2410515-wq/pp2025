import curses
import os
import pickle
import zipfile
from curses import wrapper

from domains import Student, Course
import input as input_module
import output as output_module


DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DATA_DIR, "students.dat")


def compress_data():
    """Compress students.txt, courses.txt, marks.txt into students.dat using ZIP"""
    files_to_compress = ["students.txt", "courses.txt", "marks.txt"]
    existing_files = []

    for filename in files_to_compress:
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            existing_files.append((filepath, filename))

    if existing_files:
        with zipfile.ZipFile(DATA_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filepath, filename in existing_files:
                zipf.write(filepath, filename)
        # Remove original txt files after compression
        for filepath, _ in existing_files:
            os.remove(filepath)
        return True
    return False


def decompress_data():
    """Decompress students.dat and return students, courses, marks"""
    students = []
    courses = []
    marks = {}

    if not os.path.exists(DATA_FILE):
        return students, courses, marks

    try:
        with zipfile.ZipFile(DATA_FILE, 'r') as zipf:
            zipf.extractall(DATA_DIR)

        # Load students
        students_file = os.path.join(DATA_DIR, "students.txt")
        if os.path.exists(students_file):
            with open(students_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 3:
                            students.append(Student(parts[0], parts[1], parts[2]))

        # Load courses
        courses_file = os.path.join(DATA_DIR, "courses.txt")
        if os.path.exists(courses_file):
            with open(courses_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 3:
                            courses.append(Course(parts[0], parts[1], int(parts[2])))

        # Load marks
        marks_file = os.path.join(DATA_DIR, "marks.txt")
        if os.path.exists(marks_file):
            with open(marks_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 3:
                            marks[(parts[0], parts[1])] = float(parts[2])
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
            self.students, self.courses, self.marks = decompress_data()
            return True
        return False

    def save_data(self):
        """Compress all data files into students.dat"""
        # Save current data to txt files first
        if self.students:
            input_module.save_students_to_file(self.students)
        if self.courses:
            input_module.save_courses_to_file(self.courses)
        if self.marks:
            input_module.save_marks_to_file(self.marks)
        # Compress into students.dat
        compress_data()

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
