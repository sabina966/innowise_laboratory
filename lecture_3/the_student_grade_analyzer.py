#Create list (of dictionaries) to store student data
students = []

#Implement the Menu options

#Option 1: Add a new student
def add_a_new_student(name):
    """
    Check if a student name is already in the list, if not
    create a new dictionary (in list students) with keys "name" and "grade"

    Args:
        name (str): name of the student

    Returns:
        students (list): list of dictionaries with keys "name" and "grade"
    """
    if any(student["name"] == name.title() for student in students):
        print(f"Student with name {name.title()} already exists")
    else:
        student = {"name": name.title(), "grade": []}
        students.append(student)
        #print(f"Student with name {name.title()} added")
        #print(students)

#Option 2: Add a grade for a student
def add_a_grade_for_a_student(name):
    """
    Add grades in grade list in student dictionary in students list

    Args:
        name (str): name of the student

    Returns:
        grade (list): list of grades in student dictionary in students list
    """
    for student in students:
        if student["name"] == name.title():
            while True:
                try:
                    grade = input("Enter a greate (or 'done' to finish): ")
                    if grade == "done":
                        break
                    elif int(grade) >= 0 and int(grade) <= 100:
                        student["grade"].append(int(grade))
                    else:
                        print(f"Grade {grade} is out of range."
                              "Please choose grade between 0 and 100 inclusive.")
                except ValueError:
                    print("Invalid input. Please enter a number or 'done' to finish.")
    if all(student["name"] != name.title() for student in students):
        print(f"Student with name {name.title()} doesn't exist."
                "If you would like to add a student, use the option 1.")

#Option 3: Show report (all students)
def show_report(students):
    """
    Calculate the average grade for each student in students list.
    And print an overall summary: max average, min average, overall average.

    Args:
        students (list): students list

    Returns:
        average (float): average grade
    """
    averages = []
    if students == []:
        print("No students found.")
    elif all(student["grade"] == [] for student in students):
        print("No students grades found.")
    else:
        for student in students:
            try:
                average = sum(student["grade"]) / len(student["grade"])
                averages.append(average)
            except ZeroDivisionError:
                average = "N/A"
            finally:
                print(f"{student['name']}'s average grade is {average}")
        # Print an overall summary
        print(f"Max Average: {max(averages)}\n"
              f"Min Average: {min(averages)}\n"
              f"Overall Average: {sum(averages) / len(averages)}\n")

#Option 4: Find top performer
def find_top_performer(students):
    """
    Find the student with the highest average grade.

    Args: students (list): students list

    Returns: name (str): name of the top student,
            average (float): the highest average grade
    """
    if students == []:
        print("No students found.")
    elif all(student["grade"] == [] for student in students):
        print("No students grades found.")
    else:
        students_with_grades = filter(lambda student: student["grade"] != [], students)#keeps only the students with any grades
        try:
            top_student = max(students_with_grades, key=lambda student: sum(student["grade"])/len(student["grade"]))
            print(f"The student with the highest average is {top_student['name']} "
                  f"with a grade of {sum(top_student['grade']) / len(top_student['grade'])}.")
        except KeyError or ValueError:
            print("No students found.")
        except  ZeroDivisionError:
            print("No grades found.")

# The Menu (create main program loop)
while True:
    try:
        choice = int(input(
            "---Student Grade Analyzer---\n"
            "1. Add a new student\n"
            "2. Add grades for a student\n"
            "3. Generate a full report\n"
            "4. Find the top student\n"
            "5. Exit program\n"
            "Enter your choice: "))

        choices = [1,2,3,4,5] #list of possible options
        if choice == choices[0]:
            add_a_new_student(input("Enter a student name: "))
        elif choice == choices[1]:
            add_a_grade_for_a_student(input("Enter a student name: : "))
        elif choice == choices[2]:
            show_report(students)
        elif choice == choices[3]:
            find_top_performer(students)
        elif choice == choices[4]:
            print("Exiting program.")
            break
        else:
            print("Invalid input.  Please enter an option number from 1 to 5.")
    except ValueError:
        print("Invalid input. Please enter an option number from 1 to 5.")







