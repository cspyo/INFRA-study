import boto3
import time
from week4.util.get_env import get_sns


session = boto3.Session(profile_name='pyo')
sns = session.client('sns')

topic_arn = get_sns()

def produce_events(topic_arn):
    for i in range(1 * 100):  
        timestamp = int(time.time() * 1000000)
        message = str(timestamp)
        sns.publish(TopicArn=topic_arn, Message=message) 
        time.sleep(0.01)

produce_events(topic_arn)
