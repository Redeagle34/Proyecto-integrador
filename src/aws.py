import boto3
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def getCSVfromAWS():
    # --- CREDENCIALES AWS desde variables de entorno ---
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_REGION', 'us-west-1')

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("Las credenciales AWS no están configuradas. Por favor, configura las variables de entorno.")

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