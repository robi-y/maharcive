from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd
import s3fs

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def extract_data(filename: str):
    """Extract data from MinIO/S3"""
    s3 = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'http://minio:9000'},
        key='minioadmin',
        secret='minioadmin'
    )
    with s3.open(f'data/{filename}', 'rb') as f:
        df = pd.read_csv(f)
    return df

@task
def transform_data(df: pd.DataFrame):
    """Transform the data"""
    # Add your transformations here
    return df

@task
def load_data(df: pd.DataFrame, output_filename: str):
    """Load data back to MinIO/S3"""
    s3 = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'http://minio:9000'},
        key='minioadmin',
        secret='minioadmin'
    )
    with s3.open(f'processed/{output_filename}', 'w') as f:
        df.to_csv(f, index=False)

@flow(name="ETL Pipeline")
def etl_flow(input_filename: str, output_filename: str):
    """Main ETL flow"""
    # Extract
    raw_data = extract_data(input_filename)
    
    # Transform
    transformed_data = transform_data(raw_data)
    
    # Load
    load_data(transformed_data, output_filename)

if __name__ == "__main__":
    etl_flow("input.csv", "output.csv")
