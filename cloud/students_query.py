import json
import pandas as pd
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession

def students_query(project_id, dataset_id, table_id, service_account_path, student_id):

    with open(service_account_path, 'r') as f:
        service_account_info = json.load(f)

    # Define the required scopes
    scopes = ["https://www.googleapis.com/auth/bigquery", "https://www.googleapis.com/auth/cloud-platform"]

    # Create credentials using the service account key and the required scopes
    credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)

    # Create an authorized session
    authorized_session = AuthorizedSession(credentials)

    # Define the API endpoint and parameters
    url = f'https://bigquery.googleapis.com/bigquery/v2/projects/{project_id}/queries'
    query = f"""
                SELECT * 
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
    df_tor['semester'] = df_tor['semester'].astype(int)
    df_tor['grade'] = df_tor['grade'].astype(int)
    df_tor['exam_date'] = pd.to_datetime(df_tor['exam_date'])
    df_tor['absences_lectures'] = df_tor['absences_lectures'].astype(int)
    df_tor['credits'] = df_tor['credits'].astype(int)

    return df_tor

def abseces_query(project_id, dataset_id, table_id, service_account_path, student_id):

    with open(service_account_path, 'r') as f:
        service_account_info = json.load(f)

    # Define the required scopes
    scopes = ["https://www.googleapis.com/auth/bigquery", "https://www.googleapis.com/auth/cloud-platform"]

    # Create credentials using the service account key and the required scopes
    credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)

    # Create an authorized session
    authorized_session = AuthorizedSession(credentials)

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

    return total_absences

def grade_query(project_id, dataset_id, table_id, service_account_path, student_id):

    with open(service_account_path, 'r') as f:
        service_account_info = json.load(f)

    # Define the required scopes
    scopes = ["https://www.googleapis.com/auth/bigquery", "https://www.googleapis.com/auth/cloud-platform"]

    # Create credentials using the service account key and the required scopes
    credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)

    # Create an authorized session
    authorized_session = AuthorizedSession(credentials)

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

    return avg_grade

def failure_query(project_id, dataset_id, table_id, service_account_path, student_id):

    with open(service_account_path, 'r') as f:
        service_account_info = json.load(f)

    # Define the required scopes
    scopes = ["https://www.googleapis.com/auth/bigquery", "https://www.googleapis.com/auth/cloud-platform"]

    # Create credentials using the service account key and the required scopes
    credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)

    # Create an authorized session
    authorized_session = AuthorizedSession(credentials)

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

    return total_failures


# print(df_tor)
# print(avg_grade)
# print(total_absences)
# print(total_failures)