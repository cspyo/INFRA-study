import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
from week4.util.get_env import get_sqs_std
from week4.event_handler import handle_event
import threading

session = boto3.Session(profile_name='pyo')
sqs = session.client('sqs')
queue_url = get_sqs_std()

def receive_message():
    messages = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    return messages

def unpack_message(message):
    message_id = message['MessageId']
    message_timestamp = float(message['Body'])
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
