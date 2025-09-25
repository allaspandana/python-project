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
