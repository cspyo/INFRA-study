import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
from week4.util.get_env import get_kinesis_stream_arn
from week4.event_handler import handle_event
import threading
import json

session = boto3.Session(profile_name='pyo')
kinesis = session.client('kinesis')

def get_shard_iterator():
    stream_arn = get_kinesis_stream_arn()
    stream = kinesis.describe_stream(StreamArn=stream_arn)
    shard_iterator_response = kinesis.get_shard_iterator(
        StreamArn=stream_arn,
        ShardId=stream['StreamDescription']['Shards'][0]['ShardId'] ,
        ShardIteratorType='TRIM_HORIZON'
    )
    shard_iterator = shard_iterator_response['ShardIterator']

    return shard_iterator


def start_listener():
    shard_iterator = get_shard_iterator()
    while True:
        records_response = kinesis.get_records(
            ShardIterator=shard_iterator,
            Limit=10
        )
        records = records_response['Records']

        for record in records:
            data = json.loads(record['Data'].decode('utf-8'))
            print("Received event:", data)

        shard_iterator = records_response['NextShardIterator']
            
if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
