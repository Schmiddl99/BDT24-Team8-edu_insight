import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # setting the path of this project one level up (otherwise it can't find other files)

import duckdb
import pandas as pd
import dask.dataframe as ddf
from transformation.student_perf import StudentPerformance

pd.set_option('future.no_silent_downcasting', True)
pd.options.display.max_columns = None
pd.set_option('display.precision', 2)


### creating duckdb database

conn = duckdb.connect(database = "database/bdt.duckdb" , read_only = False)


### Define how to transform the student performance csv's.
student_perf_raw = ['student-mat.csv', 'student-por.csv']
keep_columns = ['sex', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
                'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 
                'activities', 'romantic', 'famrel', 'freetime', 'goout', 
                'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3']
conv_columns = ['sex', 'address', 'famsize', 'Pstatus', 'schoolsup', 'famsup', 'activities', 'romantic']
replace_dict = {'F': 0, 'M': 1, 'U': 0, 'R': 1, 'LE3': 0, 'GT3': 1, 'T': 0, 'A': 1, 'yes': 1, 'no': 0}
grades = ['G1', 'G2', 'G3']

sp = StudentPerformance(student_perf_raw, keep_columns, conv_columns, replace_dict, grades)
print(sp.get_student_performance().head())
student_perf = sp.get_student_performance()


### Ingest data into duckdb database

# Map Pandas dtypes to DuckDB SQL types
dtype_mapping = {
    'int64': 'INTEGER',
    'float64': 'DOUBLE',
    'bool': 'BOOLEAN',
    'object': 'VARCHAR',
    'string': 'VARCHAR'
}

# Generate the CREATE TABLE statement dynamically
def generate_create_table_statement(table_name, df):
    columns = []
    for column_name, dtype in df.dtypes.items():
        sql_type = dtype_mapping.get(str(dtype), 'VARCHAR')  # Default to VARCHAR if dtype is not found
        columns.append(f"{column_name} {sql_type}")
    columns_sql = ", ".join(columns)
    create_table_query = f"CREATE OR REPLACE TABLE {table_name} ({columns_sql})"
    return create_table_query

# Generate the CREATE TABLE statement
table_name = 'student_perf'
create_table_query = generate_create_table_statement(table_name=table_name, df=student_perf)
conn.execute(create_table_query)                                        # Execute the CREATE TABLE statement

student_perf = student_perf.repartition(partition_size="100MB")         # Should be changed for prod but for our purposes its enough

# Function to ingest a partition into DuckDB
def ingest_partition(conn, table_name, df):
    conn.register("temp_df", df)                                        # Create temp. table to transform the DataFrame into the right format
    conn.execute(f"INSERT INTO {table_name} SELECT * FROM temp_df")
    conn.unregister("temp_df")                                          # Delete temp. table to free up space

# Iterate over partitions and ingest them
for partition in student_perf.to_delayed():
    df_partition = partition.compute()                                  # Compute each partition into a Pandas DataFrame
    ingest_partition(conn, table_name=table_name, df=df_partition)

# Verify the ingestion
result = conn.execute("SELECT * FROM student_perf LIMIT 5").fetchdf()
print(result)


### Print the list of tables

tables = conn.execute("SHOW TABLES").fetchall()                         # Query to check if tables exist

print("Tables in the database:")
for table in tables:
    print(table)

conn.close()