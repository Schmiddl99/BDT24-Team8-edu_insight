import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # setting the path of this project one level up (otherwise it can't find other files)

import json
import pandas as pd
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession

# Ensure the environment variable is set
service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if not service_account_path:
    raise ValueError("The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

def create_authorized_session(service_account_path):
    """
    Creates an authorized session using the service account JSON file.

    Args:
        service_account_path (str): Path to the service account JSON file.

    Returns:
        AuthorizedSession: An authorized session for making authenticated requests.
    """
    with open(service_account_path, 'r') as f:
        service_account_info = json.load(f)

    # Define the required scopes
    scopes = ["https://www.googleapis.com/auth/bigquery", "https://www.googleapis.com/auth/cloud-platform"]

    # Create credentials using the service account key and the required scopes
    credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)

    # Create an authorized session
    return AuthorizedSession(credentials)


# Function to query students data
def students_query(project_id, dataset_id, table_id, student_id):

    authorized_session = create_authorized_session(service_account_path)

    # Define the API endpoint and parameters
    url = f'https://bigquery.googleapis.com/bigquery/v2/projects/{project_id}/queries'
    query = f"""
                SELECT studentID, course_name, subject, grade, credits 
                FROM `{project_id}.{dataset_id}.{table_id}`
                WHERE studentID = {student_id}
                OR course_name IN (
                    SELECT course_name
                    FROM `{project_id}.{dataset_id}.{table_id}` 
                    WHERE studentID = {student_id}
                )
                OR subject IN (
                    SELECT subject
                    FROM `{project_id}.{dataset_id}.{table_id}` 
                    WHERE studentID = {student_id}
                );
                """
    params = {
        'query': query,
        'useLegacySql': False
    }

    ### Make the request to the BigQuery API

    response = authorized_session.post(url, json = params)
    response.raise_for_status()  # Raise an error for bad responses

    ### Extract the data from the response

    data = response.json()
    rows = data.get('rows', [])
    field_names = [field['name'] for field in data['schema']['fields']]

    records = []
    for row in rows:
        record = {}
        for field, value in zip(field_names, row['f']):
            record[field] = value['v']
        records.append(record)

    df_tor = pd.DataFrame(records)

    # Convert data types
    df_tor['studentID'] = df_tor['studentID'].astype(int)
    df_tor['course_name'] = df_tor['course_name'].astype(str)
    df_tor['subject'] = df_tor['subject'].astype(str)
    # df_tor['semester'] = df_tor['semester'].astype(int)
    df_tor['grade'] = df_tor['grade'].astype(int)
    # df_tor['exam_date'] = pd.to_datetime(df_tor['exam_date'])
    # df_tor['absences_lectures'] = df_tor['absences_lectures'].astype(int)
    df_tor['credits'] = df_tor['credits'].astype(int)

    return df_tor

# Function to query the total absences
def absences_query(project_id, dataset_id, table_id, student_id) -> int:

    authorized_session = create_authorized_session(service_account_path)

    # Define the API endpoint and parameters
    url = f'https://bigquery.googleapis.com/bigquery/v2/projects/{project_id}/queries'
    query = f"""
                SELECT SUM(absences_lectures) AS total_absences
                FROM `{project_id}.{dataset_id}.{table_id}` 
                WHERE studentID = {student_id};
                """
    params = {
        'query': query,
        'useLegacySql': False
    }

    ### Make the request to the BigQuery API

    response = authorized_session.post(url, json = params)
    response.raise_for_status()  # Raise an error for bad responses

    ### Extract the data from the response

    data = response.json()
    rows = data.get('rows', [])
    field_names = [field['name'] for field in data['schema']['fields']]

    records = []
    for row in rows:
        record = {}
        for field, value in zip(field_names, row['f']):
            record[field] = value['v']
        records.append(record)

    total_absences = pd.DataFrame(records)
    total_absences['total_absences'] = total_absences['total_absences'].astype(int)
    total_absences = total_absences.loc[0, 'total_absences']
    total_absences = int(total_absences / 10)

    return total_absences

# Function to query the average grade
def grade_query(project_id, dataset_id, table_id, student_id) -> float:

    authorized_session = create_authorized_session(service_account_path)

    # Define the API endpoint and parameters
    url = f'https://bigquery.googleapis.com/bigquery/v2/projects/{project_id}/queries'
    query = f"""
                SELECT SUM(grade * credits) / SUM(credits) AS weighted_average_grade
                FROM `{project_id}.{dataset_id}.{table_id}`
                WHERE studentID = {student_id};
                """
    params = {
        'query': query,
        'useLegacySql': False
    }

    ### Make the request to the BigQuery API

    response = authorized_session.post(url, json = params)
    response.raise_for_status()  # Raise an error for bad responses

    ### Extract the data from the response

    data = response.json()
    rows = data.get('rows', [])
    field_names = [field['name'] for field in data['schema']['fields']]

    records = []
    for row in rows:
        record = {}
        for field, value in zip(field_names, row['f']):
            record[field] = value['v']
        records.append(record)

    avg_grade = pd.DataFrame(records)
    avg_grade['weighted_average_grade'] = avg_grade['weighted_average_grade'].astype(float)
    avg_grade = avg_grade.loc[0, 'weighted_average_grade']
    avg_grade = float(avg_grade)

    return avg_grade


# Function to query the total failed exams
def failure_query(project_id, dataset_id, table_id, student_id) -> int:

    authorized_session = create_authorized_session(service_account_path)

    # Define the API endpoint and parameters
    url = f'https://bigquery.googleapis.com/bigquery/v2/projects/{project_id}/queries'
    query = f"""
                SELECT COUNT(credits) AS total_failures
                FROM `{project_id}.{dataset_id}.{table_id}` 
                WHERE 
                    studentID = {student_id}
                    AND credits = 0;
                """
    params = {
        'query': query,
        'useLegacySql': False
    }

    ### Make the request to the BigQuery API

    response = authorized_session.post(url, json = params)
    response.raise_for_status()  # Raise an error for bad responses

    ### Extract the data from the response

    data = response.json()
    rows = data.get('rows', [])
    field_names = [field['name'] for field in data['schema']['fields']]

    records = []
    for row in rows:
        record = {}
        for field, value in zip(field_names, row['f']):
            record[field] = value['v']
        records.append(record)

    total_failures = pd.DataFrame(records)
    total_failures['total_failures'] = total_failures['total_failures'].astype(int)
    total_failures = total_failures.loc[0, 'total_failures']
    total_failures = int(total_failures)

    return total_failures

## for debugging purposes

# project_id = 'bdt-2024'
# dataset_id = 'Students_table_of_records'  
# table_id = 'students_rec'
# if os.path.exists(os.path.join("cloud", "bdt-2024-accesskey.json")):
#     service_account_path = os.path.join("cloud", "bdt-2024-accesskey.json")
# else:
#     service_account_path = '../cloud/bdt-2024-accesskey.json'
# student_id = 2254

# df_tor = students_query(project_id, dataset_id, table_id, student_id)
# avg_grade = grade_query(project_id, dataset_id, table_id, student_id)
# total_absences = absences_query(project_id, dataset_id, table_id, student_id)
# total_failures = failure_query(project_id, dataset_id, table_id, student_id)

# print(df_tor, "\n")
# print(df_tor.dtypes, "\n")

# print(avg_grade, "\n")
# print(type(avg_grade), "\n")

# print(total_absences, "\n")
# print(type(total_absences), "\n")

# print(total_failures, "\n")
# print(type(total_failures), "\n")