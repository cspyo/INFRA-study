import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from week4.util.get_env import get_sns
import concurrent.futures

session = boto3.Session(profile_name='pyo')
sns = boto3.client('sns')

topic_arn = get_sns()

def publish_events(num_events):
    for _ in range(num_events):
        timestamp = time.time() 
        message = str(timestamp)
        sns.publish(TopicArn=topic_arn, Message=message) 

num_events_per_second = 100
seconds_for_publish = 60
total_events = seconds_for_publish * num_events_per_second 

with concurrent.futures.ThreadPoolExecutor() as executor:
    for _ in range(seconds_for_publish):
        executor.map(publish_events, [num_events_per_second] * num_events_per_second)
        time.sleep(1) 
