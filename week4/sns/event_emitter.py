import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from week4.util.get_env import get_sns


session = boto3.Session(profile_name='pyo')
sns = session.client('sns')

topic_arn = get_sns()

def produce_events(topic_arn):
    for i in range(1 * 1):  
        timestamp = time.time()
        message = str(timestamp)
        start_time = time.time()
        sns.publish(TopicArn=topic_arn, Message=message) 
        end_time = time.time()
        print(end_time-start_time)
        time.sleep(0.01)

produce_events(topic_arn)
