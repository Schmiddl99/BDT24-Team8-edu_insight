import duckdb
import pandas
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

### creating and connecting to database

con = duckdb.connect('database/students.duckdb')

### table with header

con.execute("""
            CREATE TABLE IF NOT EXISTS students (
            studentID INTEGER,
            course_name VARCHAR ,
            subject VARCHAR ,
            semester INTEGER ,
            grade INTEGER ,
            exam_date DATE ,
            absences_lectures INTEGER ,
            credits INTEGER 
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
    ] ,
    "Chemistry": [
        "Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Analytical Chemistry",
        "Biochemistry", "Environmental Chemistry", "Materials Chemistry", "Quantum Chemistry",
        "Chemical Engineering", "Polymer Chemistry", "Spectroscopy", "Chemical Thermodynamics",
        "Electrochemistry", "Chemistry Lab Techniques", "Medicinal Chemistry", "Industrial Chemistry"
    ],
    "Psychology": [
        "Introduction to Psychology", "Developmental Psychology", "Cognitive Psychology", "Social Psychology",
        "Clinical Psychology", "Behavioral Neuroscience", "Research Methods", "Psychological Statistics",
        "Abnormal Psychology", "Personality Psychology", "Health Psychology", "Educational Psychology",
        "Forensic Psychology", "Industrial-Organizational Psychology", "Counseling Psychology", "Psychopharmacology"
    ],
    "Biology": [
        "Cell Biology", "Genetics", "Microbiology", "Biochemistry",
        "Ecology", "Evolutionary Biology", "Molecular Biology", "Physiology",
        "Botany", "Zoology", "Immunology", "Developmental Biology",
        "Marine Biology", "Neurobiology", "Biophysics", "Bioinformatics"
    ],
    "Electrical Engineering": [
        "Circuits", "Electromagnetics", "Signals and Systems", "Digital Logic",
        "Microelectronics", "Control Systems", "Power Systems", "Communication Systems",
        "Embedded Systems", "VLSI Design", "Renewable Energy", "Robotics",
        "Electromechanical Systems", "Network Analysis", "Digital Signal Processing", "Analog Circuits"
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

num_students = 1000

def insert_student_records():
    con.execute("BEGIN TRANSACTION")

    for _ in range(num_students):
        studentID = random.randint(1000, 9999)
        course_name = random.choice(list(course_subjects.keys()))
        max_exams_per_student = len(course_subjects[course_name])
        num_exams = random.randint(1, max_exams_per_student)

        for _ in range(num_exams):
            subject = random.choice(course_subjects[course_name])
            semester = random.choice(semesters)
            grade = random.randint(0, 31)
            exam_date = random_exam_date()
            credits = random.choice([6, 9, 12])
            credits_to_add = credits if grade >= 18 else 0
            absences_lectures = int(min(max(random.triangular(0, 20, 0), 0), 20))

            print(f"Inserting: {studentID}, {subject}, {course_name}, {semester}, {grade}, {exam_date}, {absences_lectures}, {credits_to_add}")

            con.execute('''
                INSERT INTO students (studentID, course_name, subject, semester, grade, exam_date, absences_lectures, credits)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (studentID, course_name, subject, semester, grade, exam_date, absences_lectures, credits_to_add))

    con.execute("COMMIT")


        

# Insert student records
insert_student_records()

# Remove duplicates
con.execute("""
    CREATE TABLE students_unique AS
    SELECT DISTINCT ON (studentID, subject) *
    FROM students
    ORDER BY studentID, subject, exam_date DESC
""")

# Drop the original table and rename the new one
con.execute("DROP TABLE students")
con.execute("ALTER TABLE students_unique RENAME TO students")

# Remove records with same studentID but different course_name
# Create a temporary table with the records we want to keep
con.execute("""
    CREATE TEMPORARY TABLE students_to_keep AS
    SELECT s1.*
    FROM students s1
    LEFT JOIN students s2
    ON s1.studentID = s2.studentID AND s1.course_name > s2.course_name
    WHERE s2.studentID IS NULL
""")

# Replace the contents of the original table with the records we want to keep
con.execute("""
    DELETE FROM students
""")

con.execute("""
    INSERT INTO students
    SELECT * FROM students_to_keep
""")

# Drop the temporary table
con.execute("""
    DROP TABLE students_to_keep
""")

# Verify if data has been inserted correctly
result = con.execute('SELECT COUNT(*) FROM students').fetchone()
print(f"Total records after removing duplicates: {result[0]}")

# Query the table and fetch all records
result = con.execute('SELECT * FROM students').fetchall()

for row in result:
    print(row)

# Export table to CSV
csv_export_query = "COPY students TO 'database/students.csv' (HEADER, DELIMITER ',')"
con.execute(csv_export_query)

con.close()

print("Database and table filled successfully!")