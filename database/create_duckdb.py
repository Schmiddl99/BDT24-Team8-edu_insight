import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import duckdb
import pandas as pd
import dask.dataframe as ddf
from transformation.utility import extract_variables_from_notebook


### creating duckdb database

conn = duckdb.connect(database = "database/bdt.duckdb" , read_only = False)


### extract student_perf datafram from ipynb

# Path to your Jupyter Notebook
notebook_path = 'transformation/student_perf.ipynb'

# Extract variables
notebook_vars = extract_variables_from_notebook(notebook_path)

# Access the specific variable (assuming 'student_perf' is the variable you need)
student_perf = notebook_vars['student_perf']

# Now you can use the 'student_perf' variable in your script
print(student_perf)


### ingest data into duckdb database

# Map Pandas dtypes to DuckDB SQL types
dtype_mapping = {
    'int64': 'INTEGER',
    'float64': 'DOUBLE',
    'bool': 'BOOLEAN',
    'object': 'VARCHAR',
    'string': 'VARCHAR'
}

# Define table name
table_name = 'student_perf'

# Define DataFrame
ddf = student_perf

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
create_table_query = generate_create_table_statement(table_name=table_name, df=student_perf)

# Execute the CREATE TABLE statement
conn.execute(create_table_query)

ddf = ddf.repartition(partition_size="100MB")                           # should be changed for prod but for our purposes its enough

# Function to ingest a partition into DuckDB
def ingest_partition(conn, table_name, df):
    conn.register("temp_df", df)                                        # create temp. table to transform the DataFrame into the right format
    conn.execute(f"INSERT INTO {table_name} SELECT * FROM temp_df")
    conn.unregister("temp_df")

# Iterate over partitions and ingest them
for partition in ddf.to_delayed():
    df_partition = partition.compute()                                  # Compute each partition into a Pandas DataFrame
    ingest_partition(conn, table_name=table_name, df=df_partition)

# Verify the ingestion
result = conn.execute("SELECT * FROM student_perf").fetchdf()
print(result)

### Query to check if tables exist

tables = conn.execute("SHOW TABLES").fetchall()

### Print the list of tables

print("Tables in the database:")
for table in tables:
    print(table)

conn.close()