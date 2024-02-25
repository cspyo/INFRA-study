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

def get_sns_sqs_std_topic():
    load_dotenv()
    return os.getenv("SNS_SQS_STD_TOPIC_ARN")

def get_sns_sqs_fifo_topic():
    load_dotenv()
    return os.getenv("SNS_SQS_FIFO_TOPIC_ARN")

def get_sns_sqs_std_queue():
    load_dotenv()
    return os.getenv("SNS_SQS_STD_QUEUE_URL")

def get_sns_sqs_fifo_queue():
    load_dotenv()
    return os.getenv("SNS_SQS_FIFO_QUEUE_URL")