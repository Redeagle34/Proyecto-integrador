import boto3
import pandas as pd

def getCSVfromAWS():
    # --- CREDENCIALES AWS (directamente en el código, solo temporalmente) ---
    aws_access_key_id = '.'
    aws_secret_access_key = '.'
    region = '.'

    # Crear cliente S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

    # --- Parámetros del CSV ---
    bucket_name = 'csv-data-python-aws'
    csv_key = 'Sleep_health_and_lifestyle_dataset.csv'  # ruta dentro del bucket

    # Obtener el objeto de S3
    obj = s3.get_object(Bucket=bucket_name, Key=csv_key)

    # Leerlo en pandas
    df = pd.read_csv(obj['Body'])

    return df