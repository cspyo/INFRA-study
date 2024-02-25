import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from datetime import datetime
from week4.util.get_env import get_sns


session = boto3.Session(profile_name='pyo')
sns = session.client('sns')

topic_arn = get_sns()

def produce_events(topic_arn):
    for i in range(1 * 1):  
        timestamp = datetime.now().timestamp()
        message = str(timestamp)
        sns.publish(TopicArn=topic_arn, Message=message) 
        time.sleep(0.01)

produce_events(topic_arn)
