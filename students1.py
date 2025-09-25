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
def generate_report():
    students = read_students()
    branch = input("Enter Branch: ")
    year = input("Enter Year: ")
    subset = [s for s in students if s["Branch"] == branch and s["Year"] == year]
    if not subset:
        print(" No data for given branch/year.")
        return

    marks = [int(s["Final"]) for s in subset if s["Final"].isdigit()]
    avg = statistics.mean(marks) if marks else 0
    highest = max(marks) if marks else 0
    lowest = min(marks) if marks else 0

    print(f"\nReport for {branch} - Year {year}")
    print(f"Total Students: {len(subset)}")
    print(f"Average: {avg:.2f}, Highest: {highest}, Lowest: {lowest}")

    ensure_reports_folder()
    fname = os.path.join(REPORT_FOLDER, f"report_{branch}_{year}.csv")
    with open(fname, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=subset[0].keys())
        writer.writeheader()
        writer.writerows(subset)
    print(f" Report exported: {fname}")
def bulk_import():
    file = input("Enter CSV file path to import: ")
    if not os.path.exists(file):
        print(" File not found.")
        return
    existing = read_students()
    rolls = {s["Roll_No"] for s in existing}
    errors = []
    with open(file, newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            if row["Roll_No"] in rolls:
                errors.append((i, row, "Duplicate Roll_No"))
                continue
            existing.append(row)
            rolls.add(row["Roll_No"])
    write_students(existing)
    if errors:
        with open("import_errors.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Line","Data","Error"])
            for e in errors:
                writer.writerow(e)
        print(" Errors saved to import_errors.csv")
    print(" Bulk import completed.")
def sort_filter():
    students = read_students()
    print("1. Sort by Final Marks")
    print("2. Filter by Attendance < threshold")
    choice = input("Enter choice: ")
    if choice == "1":
        sorted_list = sorted(students, key=lambda x: int(x["Final"]) if x["Final"].isdigit() else -1, reverse=True)
        for s in sorted_list:
            print(s)
    elif choice == "2":
        th = int(input("Enter threshold %: "))
        filtered = [s for s in students if s["Attendance"].isdigit() and int(s["Attendance"]) < th]
        for s in filtered:
            print(s)
    else:
        print(" Invalid choice.")
