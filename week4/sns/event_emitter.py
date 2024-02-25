import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from week4.util.get_env import get_sns
import concurrent.futures

session = boto3.Session(profile_name='pyo')
sns = session.client('sns')

topic_arn = get_sns()

def publish_events(i):
    timestamp = time.time() 
    message = str(timestamp)
    sns.publish(TopicArn=topic_arn, Message=message) 

num_events_per_second = 100
seconds_for_publish = 60

start_time = time.time()
with concurrent.futures.ThreadPoolExecutor() as executor:
    for _ in range(seconds_for_publish):
        executor.map(publish_events, range(num_events_per_second))
        time.sleep(1) 
end_time = time.time()

print("Total publish time", end_time-start_time)
print("Total publish count", num_events_per_second*seconds_for_publish)
