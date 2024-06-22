from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound

def create_dataset_if_not_exists(client, dataset_id):
    """Create a BigQuery dataset if it does not exist."""

    dataset_ref = client.dataset(dataset_id)

    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} already exists.")

    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset = client.create_dataset(dataset)
        print(f"Created dataset {client.project}.{dataset.dataset_id}")

    except Exception as e:
        print(f"Error creating dataset: {e}")

def create_table_if_not_exists(client, dataset_id, table_id, schema):
    """Create the students table of records if it doesn't exist"""

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    try:
        client.get_table(table_ref)
        print(f"Table {table_id} already exists in dataset {dataset_id}.")

    except NotFound:
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)
        print(f"Created table {table.table_id} in dataset {dataset_id}")

    except Exception as e:
        print(f"Error creating table: {e}")

def load_csv_to_bigquery(dataset_id, table_id, gcs_uri, credentials_path, schema):
    """Load a CSV file from Google Cloud Storage into a BigQuery table."""

    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    create_dataset_if_not_exists(client, dataset_id)
    create_table_if_not_exists(client, dataset_id, table_id, schema)

    job_config = bigquery.LoadJobConfig(
        source_format = bigquery.SourceFormat.CSV,
        autodetect = True,
        skip_leading_rows = 1,
        write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE 
    )

    load_job = client.load_table_from_uri(
        gcs_uri,
        f"{client.project}.{dataset_id}.{table_id}",
        job_config=job_config
    )

    load_job.result()
    print(f"Loaded {load_job.output_rows} rows into {dataset_id}:{table_id} from {gcs_uri}.")

dataset_id = 'Students_table_of_records'
table_id = 'students_data'
gcs_uri = 'gs://bdt-tor/students_tor.csv'
credentials_path = 'bdt-2024-accesskey.json'

### automatically get schema

schema = []

load_csv_to_bigquery(dataset_id, table_id, gcs_uri, credentials_path, schema)