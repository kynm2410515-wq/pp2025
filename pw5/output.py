import curses
from curses.textpad import rectangle
import numpy as np


def setup_colors():
    """Initialize color pairs for decorative UI"""
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)      # title
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)     # menu
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)    # highlight
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)       # error
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)      # select
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)   # status


def draw_title(stdscr, title):
    """Draw a decorated title banner"""
    height, width = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(0, 0, "=" * (width - 1))
    title_text = f" {title} "
    x = (width - len(title_text)) // 2
    stdscr.addstr(1, x, title_text)
    stdscr.addstr(2, 0, "=" * (width - 1))
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)


def draw_box(stdscr, y, x, height, width, title=""):
    """Draw a box with optional title"""
    rectangle(stdscr, y, x, y + height - 1, x + width - 1)
    if title:
        title_text = f" {title} "
        title_x = x + (width - len(title_text)) // 2
        stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(y, title_x, title_text)
        stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)


def draw_status_bar(stdscr, message):
    """Draw status bar at the bottom of screen"""
    height, width = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(6))
    stdscr.addstr(height - 1, 0, " " * (width - 1))
    stdscr.addstr(height - 1, 2, message[:width-4])
    stdscr.attroff(curses.color_pair(6))


def draw_highlight(stdscr, y, x, text):
    """Draw highlighted text"""
    stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(y, x, text)
    stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)


def get_input(stdscr, prompt, y, x, width=30):
    """Get user input with a decorated input box"""
    curses.echo()
    curses.curs_set(1)
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(y, x, prompt)
    stdscr.attroff(curses.color_pair(2))
    input_y, input_x = y, x + len(prompt) + 1
    draw_box(stdscr, input_y - 1, input_x - 1, 3, width + 2)
    stdscr.move(input_y, input_x)
    stdscr.refresh()
    user_input = stdscr.getstr(input_y, input_x, width).decode('utf-8')
    curses.noecho()
    curses.curs_set(0)
    return user_input


def list_items(stdscr, items, title):
    """Display a list of items"""
    if stdscr:
        if not items:
            stdscr.addstr(5, 5, f"No {title.lower()} available.")
            stdscr.refresh()
            return
        y = 5
        stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(y, 5, f"{title}:")
        stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
        y += 2
        for idx, item in enumerate(items, 1):
            stdscr.addstr(y, 5, f"{idx}. {item}")
            y += 1
        y += 1
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(y, 5, f"Total: {len(items)}")
        stdscr.attroff(curses.color_pair(2))
        stdscr.refresh()
    else:
        if not items:
            return print(f"No {title.lower()} available.")
        print(f"\n{title}")
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")
        print(f"Total: {len(items)}")


def list_students(stdscr, students):
    """Display list of students"""
    list_items(stdscr, students, "Students")


def list_courses(stdscr, courses):
    """Display list of courses"""
    list_items(stdscr, courses, "Courses")


def calculate_gpa(student, courses, marks):
    """Calculate GPA for a student using numpy"""
    if not courses:
        return 0.0
    marks_array = []
    credits_array = []
    for course in courses:
        key = (student.id, course.course_id)
        if key in marks:
            marks_array.append(marks[key])
            credits_array.append(course.credits)

    if not marks_array:
        return 0.0

    marks_np = np.array(marks_array)
    credits_np = np.array(credits_array)

    weighted_sum = np.sum(marks_np * credits_np)
    total_credits = np.sum(credits_np)

    return weighted_sum / total_credits if total_credits > 0 else 0.0


def show_student_gpa(stdscr, students, courses, marks):
    """Display GPA for all students"""
    if stdscr:
        if not students:
            stdscr.addstr(5, 5, "No students available.")
            stdscr.refresh()
            return
        y = 5
        stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(y, 5, "Student GPAs:")
        stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
        y += 2
        for student in students:
            gpa = calculate_gpa(student, courses, marks)
            stdscr.addstr(y, 5, f"{student.name} (ID: {student.id}): GPA = {gpa:.2f}")
            y += 1
        stdscr.refresh()
    else:
        if not students:
            return print("No students available.")
        print("\nGPA:")
        for student in students:
            gpa = calculate_gpa(student, courses, marks)
            print(f"{student.name} (ID: {student.id}): GPA = {gpa:.2f}")


def sort_students_by_gpa(stdscr, students, courses, marks):
    """Display students sorted by GPA"""
    if stdscr:
        if not students:
            stdscr.addstr(5, 5, "No students available.")
            stdscr.refresh()
            return
        student_gpa_list = [(student, calculate_gpa(student, courses, marks)) for student in students]
        student_gpa_list.sort(key=lambda x: x[1], reverse=True)
        y = 5
        stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(y, 5, "Students sorted by GPA (Highest to Lowest):")
        stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
        y += 2
        for rank, (student, gpa) in enumerate(student_gpa_list, 1):
            stdscr.addstr(y, 5, f"{rank}. {student.name} (ID: {student.id}): GPA = {gpa:.2f}")
            y += 1
        stdscr.refresh()
    else:
        if not students:
            return print("No students available.")
        student_gpa_list = [(student, calculate_gpa(student, courses, marks)) for student in students]
        student_gpa_list.sort(key=lambda x: x[1], reverse=True)
        print("\nSorted by GPA:")
        for rank, (student, gpa) in enumerate(student_gpa_list, 1):
            print(f"{rank}. {student.name} (ID: {student.id}): GPA = {gpa:.2f}")


def draw_menu(stdscr, current_row, menu_options, students, courses):
    """Draw the main menu with selection highlight"""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    draw_title(stdscr, "STUDENT MANAGEMENT SYSTEM IN USTH")
    menu_start_y = 5
    menu_height = len(menu_options) + 4
    menu_width = 50
    menu_x = (width - menu_width) // 2
    draw_box(stdscr, menu_start_y, menu_x, menu_height, menu_width, "MAIN MENU")

    for idx, option in enumerate(menu_options):
        y = menu_start_y + idx + 2
        x = menu_x + 5

        if idx == current_row:
            stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
            stdscr.addstr(y, x, f"> {idx + 1}. {option}".ljust(menu_width - 10))
            stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
        else:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, f"  {idx + 1}. {option}")
            stdscr.attroff(curses.color_pair(2))

    draw_status_bar(stdscr, f" Students: {len(students)} | Courses: {len(courses)}")
    stdscr.refresh()
