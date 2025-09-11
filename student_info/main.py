import os
from student import Student

def save_students(f_name, Students):
    with open(f_name, "w") as f:
        for student in Students:
            grade = ",".join(map(str, student.grades))
            f.write(f"{student.id},{student.name},{grade}\n")

def load_students(f_name):
    student_data = []
    if not os.path.exists(f_name):
        return student_data

    with open(f_name, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            student_id = parts[0]
            student_name = parts[1]
            student_grades = ",".join(parts[2:])  
            student_data.append(Student(student_id, student_name, student_grades))
                
    return student_data            

def find_student_by_id(id, Students):
    for student in Students:
        if student.id == id:
            return student
    return None


def main():
    f_name = "students.txt"
    student_data = load_students(f_name)

    while True:
        print("1. Add new student")
        print("2. show students")
        print("3. update student grades")
        print("4. find student by id")
        print("5. program exit")

        option = input("enter your option: ")

        if option == "1":
            student_id = input("enter id: ")
            student_name = input("enter name: ")
            student_grades = input("enter grades  ")
            student_data.append(Student(student_id, student_name, student_grades))
            save_students(f_name, student_data)
            print("student added")

        elif option == "2":
            if not student_data:
                print("no students in data")
            else:
                for student in student_data:
                    print(student)

        elif option == "3":
            student_id = input("enter student id: ")
            student = find_student_by_id(student_id, student_data)
            if student:
                new_grades = input("enter new grades  ")
                student.grades = [int(x) for x in new_grades.split(",") if x]
                save_students(f_name, student_data)
                print("grades updated")
                print (student)
            else:
                print("student not found")

        elif option == "4":
            student_id = input("enter the id: ")
            student = find_student_by_id(student_id, student_data)
            if student:
                print(student)
            else:
                print("student not found")

        elif option == "5":
            break
        else:
            print("invalid option")


if __name__ == "__main__":
    main()
