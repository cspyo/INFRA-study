import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from week4.util.get_env import get_kinesis_stream_arn
from week4.event_emitter import emit_event
import json

session = boto3.Session(profile_name='pyo')
kinesis = session.client('kinesis')

stream_arn = get_kinesis_stream_arn()

def publish_events(i):
    timestamp = time.time() 
    message_body = {
        'Message': timestamp
    }
    try:
        kinesis.put_record(
            StreamArn=stream_arn,
            Data=json.dumps(message_body),
            PartitionKey='partition_key'
        )
    except Exception as e:
        print(f"An error occurred in emit_event: {e}") 


emit_event(60, publish_events)