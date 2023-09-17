import logging
from menu_definitions import menu_main, student_select, debug_select
from db_connection import engine, Session
from orm_base import metadata

from Student import Student
from Department import Department
from Option import Option
from Menu import Menu


def add_department(session: Session):
    """
        Prompt the user for the information for a new department and validate
        the input to make sure that we do not create any duplicates.
        :param session: The connection to the database.
        :return:        None
        """
    unique_abbr = False
    unique_chair = False
    unique_office = False
    unique_desc = False
    departmentName: str = ''
    abbreviation: str = ''
    chairName: str = ''
    building: str = ''
    officeNum: int = 0
    description: str = ''

    while not unique_abbr or not unique_chair or not unique_office or not unique_desc:
        departmentName = input("Department name --> ")
        abbreviation = input("Department's abbreviation --> ")
        chairName = input("Department Chair name --> ")
        building = input("Building name --> ")
        officeNum = int(input("Office number --> "))
        description = input("Description of department --> ")

        abbr_count = session.query(Department).filter(Department.abbreviation == abbreviation).count()
        chair_count = session.query(Department).filter(Department.chairName == chairName).count()
        office_count = session.query(Department).filter(Department.building == building,
                                                        Department.officeNum == officeNum).count()
        desc_count = session.query(Department).filter(Department.description == description).count()

        unique_abbr = abbr_count == 0
        unique_chair = chair_count == 0
        unique_office = office_count == 0
        unique_desc = desc_count == 0

        if not unique_abbr:
            print("We already have a department by that abbreviation. Try again.")
        elif not unique_chair:
            print("The named individual is already a chair of a different department. Try again.")
        elif not unique_office:
            print("That office room is already occupied by another department. Try again.")
        elif not unique_desc:
            print("That description matches the description of another department. Try again.")
    newDepartment = Department(departmentName, abbreviation, chairName, building, officeNum, description)
    session.add(newDepartment)

def list_departments(sess: Session):
    """
        List all the departments, sorted by the abbreviations.
        :param session:
        :return:
        """

    deps: [Department] = list(sess.query(Department).order_by(Department.abbreviation))
    print("")
    for i, department in enumerate(deps):
        print(f"{i+1}.{department.abbreviation} - {department.departmentName}")

def select_department_name(sess: Session) -> Department:
    """
        List all the departments, sorted by the abbreviations.
        :param session: The connection to the database
        :return:        Department
    """

    list_departments(sess)

    found = False

    while not found:
        selection = input("\nEnter the abbreviation for the department: ")
        dep: int = sess.query(Department).filter(Department.abbreviation == selection).count()
        found = dep == 1

        if not found:
            print("No department found with that abbreviation. Try again")

        returned = sess.query(Department).filter(Department.abbreviation == selection).first()
    print(f"Department Information:\n{returned}")

    return returned


def delete_department(sess: Session):
    """
        Prompt the user for a department by the abbreviation and delete that
        department.
        :param session: The connection to the database.
        :return:        None
    """

    department = select_department_name(sess)
    sess.delete(department)


def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    lastName: str = ''
    firstName: str = ''
    email: str = ''

    while not unique_name or not unique_email:
        lastName = input("Student last name--> ")
        firstName = input("Student first name--> ")
        email = input("Student e-mail address--> ")
        name_count: int = session.query(Student).filter(Student.lastName == lastName,
                                                        Student.firstName == firstName).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = session.query(Student).filter(Student.eMail == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that e-mail address.  Try again.")
    newStudent = Student(lastName, firstName, email)
    session.add(newStudent)


def select_student_id(sess: Session) -> Student:
    """
    Prompt the user for a specific student by the student ID.  Generally
    this is not a terribly useful approach, but I have it here for
    an example.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    ID: int = -1
    while not found:
        ID = int(input("Enter the student ID--> "))
        id_count: int = sess.query(Student).filter(Student.studentId == ID).count()
        found = id_count == 1
        if not found:
            print("No student with that ID.  Try again.")
    return_student: Student = sess.query(Student).filter(Student.studentId == ID).first()
    return return_student


def select_student_first_and_last_name(sess: Session) -> Student:
    """
    Select a student by the combination of the first and last name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student last name to delete--> ")
        firstName = input("Student first name to delete--> ")
        name_count: int = sess.query(Student).filter(Student.lastName == lastName,
                                                     Student.firstName == firstName).count()
        found = name_count == 1
        if not found:
            print("No student by that name.  Try again.")
    oldStudent = sess.query(Student).filter(Student.lastName == lastName,
                                            Student.firstName == firstName).first()
    return oldStudent


def select_student_email(sess: Session) -> Student:
    """
    Select a student by the e-mail address.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    email: str = ''
    while not found:
        email = input("Enter the student email address --> ")
        id_count: int = sess.query(Student).filter(Student.eMail == email).count()
        found = id_count == 1
        if not found:
            print("No student with that email address.  Try again.")
    return_student: Student = sess.query(Student).filter(Student.eMail == email).first()
    return return_student


def find_student(sess: Session) -> Student:
    """
    Prompt the user for attribute values to select a single student.
    :param sess:    The connection to the database.
    :return:        The instance of Student that the user selected.
                    Note: there is no provision for the user to simply "give up".
    """
    find_student_command = student_select.menu_prompt()
    match find_student_command:
        case "ID":
            old_student = select_student_id(sess)
        case "first/last name":
            old_student = select_student_first_and_last_name(sess)
        case "email":
            old_student = select_student_email(sess)
        case _:
            old_student = None
    return old_student


def delete_student(session: Session):
    """
    Prompt the user for a student by the last name and first name and delete that
    student.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a student")
    oldStudent = find_student(session)
    session.delete(oldStudent)


def list_students(session: Session):
    """
    List all of the students, sorted by the last name first, then the first name.
    :param session:
    :return:
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    students: [Student] = list(session.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


def select_student_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Students.
    :param session:     The connection to the database.
    :return:            None
    """

    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
    options: [Option] = []  # The list of menu options that we're constructing.
    for student in students:
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    text_studentId: str = temp_menu.menu_prompt()

    returned_student = sess.query(Student).filter(Student.studentId == int(text_studentId)).first()

    print("Selected student: ", returned_student)


if __name__ == '__main__':
    print('\nStarting off')
    #logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    # logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    #logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    #logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our "Entity" classes.
    metadata.create_all(bind=engine)

    with Session() as sess:
        main_action: str = ''
        run = True
        while run:
            do = int(input(
                "\nWhat do you want to do? \n1. Add Department \n2. Find Department\n3. Delete Department\n4. Quit\n"
            ))
            if do == 1:
                add_department(sess)
            elif do == 2:
                select_department_name(sess)
            elif do == 3:
                delete_department(sess)
            elif do == 4:
                run = False
            else:
                print("Invalid Selection. Try Again.\n")
        sess.commit()
    print('\nEnding normally')
#5gAg$v$H
