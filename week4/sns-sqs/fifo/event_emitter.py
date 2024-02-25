import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from week4.util.get_env import get_sns_sqs_fifo_topic
from week4.event_emitter import emit_event
from uuid import uuid4

session = boto3.Session(profile_name='pyo')
sns = session.client('sns')

topic_arn = get_sns_sqs_fifo_topic()

def publish_events(i):
    timestamp = time.time() 
    message = str(timestamp)
    sns.publish(TopicArn=topic_arn, Message=message, MessageDeduplicationId=str(uuid4()), MessageGroupId='group1') 

emit_event(publish_events)
