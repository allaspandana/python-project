import csv
import os
import sys
import statistics

CSV_FILE = "students.csv"
DELETED_FILE = "students_deleted.csv"
REPORT_FOLDER = "reports"
def read_students():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Roll_No","Name","Branch","Year","Gender","Age",
                             "Attendance","Mid1","Mid2","Quiz","Final"])
    with open(CSV_FILE, newline="") as f:
        return list(csv.DictReader(f))

def write_students(students):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=students[0].keys())
        writer.writeheader()
        writer.writerows(students)

def ensure_reports_folder():
    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)
def add_student():
    students = read_students()
    roll = input("Enter Roll No: ")
    if any(s["Roll_No"] == roll for s in students):
        print(" Duplicate Roll No.")
        return
    name = input("Enter Name: ")
    branch = input("Enter Branch: ")
    year = input("Enter Year: ")
    gender = input("Enter Gender: ")
    age = input("Enter Age: ")
    attendance = input("Enter Attendance %: ")
    mid1 = input("Mid1 Marks: ")
    mid2 = input("Mid2 Marks: ")
    quiz = input("Quiz Marks: ")
    final = input("Final Marks: ")

    new_student = {
        "Roll_No": roll, "Name": name, "Branch": branch, "Year": year,
        "Gender": gender, "Age": age, "Attendance": attendance,
        "Mid1": mid1, "Mid2": mid2, "Quiz": quiz, "Final": final
    }
    students.append(new_student)
    write_students(students)
    print(" Student added successfully.")
def search_student():
    students = read_students()
    query = input("Enter Roll No or Name: ")
    found = [s for s in students if s["Roll_No"] == query or query.lower() in s["Name"].lower()]
    if not found:
        print(" Student not found.")
    else:
        for s in found:
            print(s)
def update_student():
    students = read_students()
    roll = input("Enter Roll No to update: ")
    for s in students:
        if s["Roll_No"] == roll:
            print(f"Old Attendance: {s['Attendance']}, Old Final Marks: {s['Final']}")
            s["Attendance"] = input("Enter new Attendance % (Enter to skip): ") or s["Attendance"]
            s["Final"] = input("Enter new Final Marks (Enter to skip): ") or s["Final"]
            write_students(students)
            print(" Record updated.")
            return
    print(" Roll No not found.")


def delete_student():
    students = read_students()
    roll = input("Enter Roll No to delete: ")
    for s in students:
        if s["Roll_No"] == roll:
            confirm = input(f"Are you sure to delete {s['Name']}? (Y/N): ")
            if confirm.lower() == "y":
                students.remove(s)
                write_students(students)
                with open(DELETED_FILE, "a", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=s.keys())
                    if f.tell() == 0:
                        writer.writeheader()
                    writer.writerow(s)
                print("Student deleted and archived.")
            return
    print("Roll No not found.")
