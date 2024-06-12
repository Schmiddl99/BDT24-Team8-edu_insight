import duckdb
import pandas as pd

### creating duckdb database

conn = duckdb.connect(database = "database/bdt.duckdb" , read_only = False)

### datasets path

student_mat = "Data/Predict student performance/student-mat.csv"
student_por = "Data/Predict student performance/student-por.csv"

### Create math students table from DataFrame

conn.execute("CREATE OR REPLACE TABLE student_mat AS SELECT * FROM 'Data/Predict student performance/student-mat.csv'")

### Create portuguese students table from DataFrame

conn.execute("CREATE OR REPLACE TABLE student_por AS SELECT * FROM 'Data/Predict student performance/student-por.csv'" )

### Query to check if tables exist

tables = conn.execute("SHOW TABLES").fetchall()

### Print the list of tables

print("Tables in the database:")
for table in tables:
    print(table)

conn.close()
