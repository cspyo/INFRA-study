import os
from dotenv import load_dotenv

def get_rds():
    load_dotenv()
    return os.getenv("RDS_HOST"), os.getenv("RDS_PORT"), os.getenv("RDS_DB_NAME"), os.getenv("RDS_USER"), os.getenv("RDS_PASSWORD")

def get_redshift():
    load_dotenv()
    return os.getenv("REDSHIFT_HOST"), os.getenv("REDSHIFT_PORT"), os.getenv("REDSHIFT_DB_NAME"), os.getenv("REDSHIFT_USER"), os.getenv("REDSHIFT_PASSWORD")