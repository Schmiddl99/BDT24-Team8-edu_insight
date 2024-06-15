import duckdb
import pandas
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

### creating and connecting to database

con = duckdb.connect('students.duckdb')

### table with header

con.execute("""
            CREATE TABLE IF NOT EXISTS students (
            studentID INTEGER ,
            course_name VARCHAR ,
            subject VARCHAR ,
            semester INTEGER ,
            grade INTEGER ,
            exam_date DATE ,
            absences_lectures INTEGER ,
            credits INTEGER ,
            PRIMARY KEY (studentID , subject)
            )""")

### defining data

course_subjects = {
    "Computer Science": [
        "Algorithms", "Data Structures", "Programming", "Math",
        "Databases", "Artificial Intelligence", "Data Mining",
        "Computer Networks", "Operating Systems", "Software Engineering",
        "Web Development", "Mobile Computing", "Cyber Security",
        "Cloud Computing", "Human-Computer Interaction", "Computer Graphics"
    ] ,
    "Mechanical Engineering": [
        "Thermodynamics", "Fluid Mechanics", "Solid Mechanics", "Dynamics",
        "Heat Transfer", "Math", "Physics", "Material Science",
        "Mechanical Design", "Manufacturing Processes", "Control Systems",
        "Robotics", "Energy Systems", "Mechanics of Materials",
        "CAD/CAM", "Vibration Analysis"
    ] ,
    "Business Administration": [
        "Accounting", "Marketing", "Finance", "Management",
        "Business Law", "Public Law", "Math", "Microeconomics",
        "Macroeconomics", "Organizational Behavior", "Strategic Management",
        "Operations Management", "Business Ethics", "Human Resource Management",
        "International Business", "Supply Chain Management"
    ] ,
    "Physics": [
        "Quantum Mechanics", "Electromagnetism", "Thermodynamics", "Optics",
        "Astrophysics", "Nuclear Physics", "Statistical Mechanics", "Classical Mechanics",
        "Solid State Physics", "Particle Physics", "Mathematical Physics",
        "Plasma Physics", "Computational Physics", "Biophysics",
        "Condensed Matter Physics", "Geophysics"
    ] ,
    "Data Science": [
        "Big Data Technologies", "Algorithms", "Statistical Models", "Statistical Methods",
        "Programming", "Machine Learning", "Deep Learning", "Data Visualization",
        "Data Engineering", "Natural Language Processing", "Law and data",
        "Cloud Computing", "Data Mining", "Introduction to machine learning",
        "Time Series Analysis", "Quantitative methods"
    ] ,
    "Mathematics": [
        "Calculus", "Linear Algebra", "Discrete Mathematics", "Probability",
        "Statistics", "Analysis", "Number Theory", "Topology",
        "Abstract Algebra", "Differential Equations", "Mathematical Logic",
        "Real Analysis", "Complex Analysis", "Combinatorics",
        "Geometry", "Mathematical Modeling"
    ] 
}

semesters = [1 , 2 , 3 , 4]

### generate random exam dates within a range

def random_exam_date():
    start_date = datetime.strptime("2022-09-01" , "%Y-%m-%d")
    end_date = datetime.strptime("2024-06-25" , "%Y-%m-%d")
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days = random_days)).date()

### fictional data

num_students = 100

### avoid duplicates in subject

inserted_records = set()

### Begin a transaction

con.execute("BEGIN TRANSACTION")

for i in range(num_students):
    studentID = random.randint(1000 , 9999)
    course_name = random.choice(list(course_subjects.keys()))
    max_exams_per_student = len(course_subjects[course_name]) - 1
    num_exams = random.randint(1, max_exams_per_student)

    ### avoid duplicates

    subject_taken = set()

    for i in range(num_exams):
        subject = random.choice(course_subjects[course_name])

        while (studentID , subject) in inserted_records:
            subject = random.choice(course_subjects[course_name])

        subject_taken.add(subject)
        inserted_records.add((studentID, subject))
        semester = random.choice(semesters)
        grade = random.randint(0 , 31)
        exam_date = random_exam_date()

        ### adding credits only if exam passed

        credits = random.choice([6 , 9 , 12])
        credits_to_add = credits if grade >= 18 else 0
        absences_lectures = random.randint(0 , 20)

        print(f"Inserting: {studentID}, {subject}, {course_name}, {semester}, {grade}, {exam_date}, {absences_lectures}, {credits_to_add}")


        con.execute('''
                INSERT INTO students (studentID , course_name , subject , semester , grade , exam_date , absences_lectures , credits)
                VALUES (?, ? , ? , ? , ? , ? , ? , ?)
        ''' , (studentID , course_name , subject , semester , grade , exam_date , absences_lectures , credits_to_add)
        )


### commit

con.execute("COMMIT")

### Verify if data has been inserted correctly

result = con.execute('SELECT COUNT(*) FROM students').fetchone()
print(f"Total records inserted: {result[0]}")


### Query the table and fetch all records

result = con.execute('SELECT * FROM students').fetchall()

for row in result:
    print(row)

### table in csv

csv_export_query = "COPY students TO 'students.csv' (HEADER, DELIMITER ',')"
con.execute(csv_export_query)

con.close()

print("Database and table filled successfully!")