import requests
import json
import pandas as pd
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession

def students_query(project_id, dataset_id, table_id, service_account_path):

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
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
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

    df = pd.DataFrame(records)

    return df

project_id = 'bdt-2024'
dataset_id = 'Students_table_of_records'  
table_id = 'students_data'
service_account_path = 'bdt-2024-accesskey.json'  # Replace with the actual path

df = students_query(project_id, dataset_id, table_id, service_account_path)
print(df)
