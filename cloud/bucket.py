from google.cloud import storage
from google.oauth2 import service_account

def upload_to_bucket(bucket_name, source_file_name, destination_blob_name, credentials_path):
    """Uploads a file to the bucket."""

    ### Initialize a storage client with credentials

    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    storage_client = storage.Client(credentials = credentials)

    ### Get the bucket

    bucket = storage_client.bucket(bucket_name)

    ### Create an object in the bucket if it doesn't exist

    blob = bucket.blob(destination_blob_name)

    if blob.exists():

        print(f"The file {destination_blob_name} already exists in the bucket {bucket_name}.")

    else:

        blob.upload_from_filename(source_file_name)
        print(f"File {source_file_name} uploaded to {destination_blob_name}.")

bucket_name = 'bdt-tor'
source_file_name = "../database/students.csv"
destination_blob_name = 'students_records.csv'
credentials_path = "bdt-2024-accesskey.json"

upload_to_bucket(bucket_name, source_file_name, destination_blob_name, credentials_path)