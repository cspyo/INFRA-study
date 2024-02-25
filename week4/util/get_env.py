import os
from dotenv import load_dotenv

def get_sns():
    load_dotenv()
    return os.getenv("SNS_TOPIC_ARN")