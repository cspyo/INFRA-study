import os
from dotenv import load_dotenv

def get_sns():
    load_dotenv()
    return os.getenv("SNS_TOPIC_ARN")

def get_sqs_std():
    load_dotenv()
    return os.getenv("SQS_STD_QUEUE_URL")

def get_sqs_fifo():
    load_dotenv()
    return os.getenv("SQS_FIFO_QUEUE_URL")