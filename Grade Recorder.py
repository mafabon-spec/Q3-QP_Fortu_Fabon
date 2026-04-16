import json
import os
import statistics

DATA_FILE = "data.json"

SUBJECTS = [
    "Math 2", "Math 3", "Social Science 2", "Earth Science 1",
    "Physics 1", "Bio 1", "Chem 1", "AdTech 2",
    "Computer Science", "PEHM", "English 2", "Filipino 21"
]


# ourrrrrr file 

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


#  FUNCTIONS  

def add_class():
    data = load_data()
    class_name = input("Enter class name: ")

    if class_name in data:
        print("Class already exists.")
        return

    data[class_name] = {}
    save_data(data)
    print("Class added!")

def add_student():
    data = load_data()
    class_name = input("Enter class name: ")

    if class_name not in data:
        print("Class not found.")
        return

    student = input("Enter student name: ")

    if student in data[class_name]:
        print("Student already exists.")
        return

    # initialize all subjects
    data[class_name][student] = {subj: None for subj in SUBJECTS}
    data[class_name][student]["ValEd"] = "Incomplete"

    save_data(data)
    print("Student added!")

def input_grade_per_subject():
    data = load_data()
    class_name = input("Enter class name: ")
    student = input("Enter student name: ")

    if class_name not in data or student not in data[class_name]:
        print("Not found.")
        return

    print("\nSubjects:")
    for i, subj in enumerate(SUBJECTS, 1):
        print(f"{i}. {subj}")
    print("13. ValEd")

    choice = input("Choose subject number: ")

    # Handle ValEd separately
    if choice == "13":
        valed = input("Enter ValEd (Complete/Incomplete): ")
        data[class_name][student]["ValEd"] = valed
        save_data(data)
        print("ValEd updated!")
        return

    try:
        subj = SUBJECTS[int(choice) - 1]
    except:
        print("Invalid choice.")
        return

    try:
        grade = float(input(f"Enter grade for {subj}: "))
        data[class_name][student][subj] = grade
        save_data(data)
        print("Grade recorded!")
    except:
        print("Invalid grade.")

def student_stats():
    data = load_data()
    class_name = input("Class: ")
    student = input("Student: ")

    if class_name not in data or student not in data[class_name]:
        print("Not found.")
        return

    grades_dict = data[class_name][student]

    # get only numeric grades
    grades = [v for v in grades_dict.values() if isinstance(v, (int, float))]

    if not grades:
        print("No grades available.")
        return

    print("\n--- Student Stats ---")
    print("Highest:", max(grades))
    print("Lowest:", min(grades))
    print("Mean:", round(statistics.mean(grades), 2))
    print("Mode:", statistics.multimode(grades))

def class_stats():
    data = load_data()
    class_name = input("Class: ")

    if class_name not in data:
        print("Class not found.")
        return

    all_grades = []

    for student in data[class_name]:
        for subj, grade in data[class_name][student].items():
            if isinstance(grade, (int, float)):
                all_grades.append(grade)

    if not all_grades:
        print("No grades.")
        return

    print("\n--- Class Stats ---")
    print("Highest:", max(all_grades))
    print("Lowest:", min(all_grades))
    print("Mean:", round(statistics.mean(all_grades), 2))
    print("Mode:", statistics.multimode(all_grades))

def show_data():
    print(json.dumps(load_data(), indent=4))

# ---------------- MENU ---------------- #

def menu():
    while True:
        print("\n===== GRADE SYSTEM =====")
        print("1. Add Class")
        print("2. Add Student")
        print("3. Input Grades")
        print("4. Student Stats")
        print("5. Class Stats")
        print("6. Show Data")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_class()
        elif choice == "2":
            add_student()
        elif choice == "3":
            input_grades()
        elif choice == "4":
            student_stats()
        elif choice == "5":
            class_stats()
        elif choice == "6":
            show_data()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

menu()
