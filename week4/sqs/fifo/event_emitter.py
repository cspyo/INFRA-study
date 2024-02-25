import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from week4.util.get_env import get_sqs_fifo
from week4.event_emitter import emit_event

session = boto3.Session(profile_name='pyo')
sqs = session.client('sqs')

queue_url = get_sqs_fifo()

def publish_events(i):
    timestamp = time.time() 
    message_body = {
        'Message': timestamp,
        'MessageAttributes': {}
    }
    sqs.send_message(QueueUrl=queue_url, MessageBody=str(message_body)) 


emit_event(publish_events)