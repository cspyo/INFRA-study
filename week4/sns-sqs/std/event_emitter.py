import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from week4.util.get_env import get_sns_sqs_std_topic
from week4.event_emitter import emit_event

session = boto3.Session(profile_name='pyo')
sns = session.client('sns')

topic_arn = get_sns_sqs_std_topic()

def publish_events(i):
    timestamp = time.time() 
    message_body = {
        'Message': timestamp
    }
    try:
        sns.publish(TopicArn=topic_arn, Message=str(message_body)) 
    except Exception as e:
        print(f"An error occurred in emit_event: {e}")

emit_event(60, publish_events)
