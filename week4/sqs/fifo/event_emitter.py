import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from week4.util.get_env import get_sqs_fifo
from week4.event_emitter import emit_event
from uuid import uuid4

session = boto3.Session(profile_name='pyo')
sqs = session.client('sqs')

queue_url = get_sqs_fifo()

def publish_events(i):
    timestamp = time.time() 
    message_body = {
        'Message': timestamp,
    }
    try:
        sqs.send_message(
            QueueUrl=queue_url, 
            MessageBody=str(message_body), 
            MessageDeduplicationId=str(uuid4()), 
            MessageGroupId='group1') 
    except Exception as e:
        print(f"An error occurred in emit_event: {e}")

print(queue_url)
emit_event(publish_events)