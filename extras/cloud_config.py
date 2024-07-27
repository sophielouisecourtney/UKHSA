import pandas as pd
from sqlalchemy import create_engine
import boto3

# Configuration
CSV_FILE_PATH = 'data.csv'
DATABASE_URI = 'postgresql+psycopg2://username:password@host:port/database'
AWS_ACCESS_KEY = 'users-access-key'
AWS_SECRET_KEY = 'users-secret-key'
AWS_BUCKET_NAME = 'users-bucket-name'
S3_FILE_KEY = 'data.csv'

# Extract
def extract_data_from_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data extracted successfully from CSV.")
        return data
    except Exception as e:
        print(f"Error while extracting data: {e}")
        return None

def extract_data_from_s3(bucket_name, file_key):
    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        data = pd.read_csv(obj['Body'])
        print("Data extracted successfully from S3.")
        return data
    except Exception as e:
        print(f"Error while extracting data from S3: {e}")
        return None

# Transform
def transform_data(data):
    try:
        # Example transformation: dropping rows with missing values
        data = data.dropna()
        
        # Example validation: check for required columns
        required_columns = ['column1', 'column2', 'column3']
        if not all(col in data.columns for col in required_columns):
            raise ValueError("Missing required columns.")
        
        print("Data transformed successfully.")
        return data
    except Exception as e:
        print(f"Error while transforming data: {e}")
        return None

# Load
def load_data_to_sql(data, db_uri):
    try:
        engine = create_engine(db_uri)
        data.to_sql('table_name', engine, if_exists='replace', index=False)
        print("Data loaded successfully into SQL database.")
    except Exception as e:
        print(f"Error while loading data into SQL: {e}")

# Main ETL process
def etl_process(file_path, db_uri, from_s3=False, bucket_name=None, file_key=None):
    if from_s3:
        data = extract_data_from_s3(bucket_name, file_key)
    else:
        data = extract_data_from_csv(file_path)
    
    if data is not None:
        data = transform_data(data)
        
    if data is not None:
        load_data_to_sql(data, db_uri)

# Run ETL process
if __name__ == "__main__":
    etl_process(CSV_FILE_PATH, DATABASE_URI)
    # To use S3 as the source, use:
    # etl_process(None, DATABASE_URI, from_s3=True, bucket_name=AWS_BUCKET_NAME, file_key=S3_FILE_KEY)
