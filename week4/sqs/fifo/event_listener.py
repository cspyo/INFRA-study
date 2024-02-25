import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
from week4.util.get_env import get_sqs_fifo
from week4.event_handler import handle_event
import threading
import json

session = boto3.Session(profile_name='pyo')
sqs = session.client('sqs')
queue_url = get_sqs_fifo()

def receive_message():
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10
    )
    if response:
        return response['Messages']
    return []

def get_timestamp_from_body(body):
    dict_value = json.loads(body.replace("'", "\""))
    return float(dict_value.get("Message"))

def unpack_message(message):
    message_id = message['MessageId']
    message_body = message['Body']
    message_timestamp = get_timestamp_from_body(message_body)
    receipt_handle = message['ReceiptHandle']
    return message_id, message_timestamp, receipt_handle

def delete_message(receipt_handle):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

def start_listener():
    while True:
        for message in receive_message():
            message_id, message_timestamp, receipt_handle = unpack_message(message)
            handle_event('sqs_std', message_id, message_timestamp)
            delete_message(receipt_handle)
            
if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
