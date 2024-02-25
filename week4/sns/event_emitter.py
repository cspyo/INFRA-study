import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from week4.util.get_env import get_sns
from week4.event_emitter import emit_event

session = boto3.Session(profile_name='pyo')
sns = session.client('sns')

topic_arn = get_sns()

def publish_events(i):
    timestamp = time.time() 
    message = str(timestamp)
    sns.publish(TopicArn=topic_arn, Message=message) 

emit_event(publish_events)
