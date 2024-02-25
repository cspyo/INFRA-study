import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
from week4.util.get_env import get_kinesis_stream_arn
from week4.event_handler import handle_event
import threading
import json

session = boto3.Session(profile_name='pyo')
kinesis = session.client('kinesis')

def get_timestamp_from_body(body):
    dict_value = json.loads(body.replace("'", "\""))
    return float(dict_value.get("Message"))

def unpack_message(message):
    message_id = message['SequenceNumber']
    message_body = json.loads(message['Data'].decode('utf-8'))
    message_timestamp = float(message_body['Message'])
    return message_id, message_timestamp

def get_shard_iterator():
    stream_arn = get_kinesis_stream_arn()
    stream = kinesis.describe_stream(StreamARN=stream_arn)
    shard_iterator_response = kinesis.get_shard_iterator(
        StreamARN=stream_arn,
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
            message_id, message_timestamp = unpack_message(record)
            handle_event('kinesis', message_id, message_timestamp)

        shard_iterator = records_response['NextShardIterator']
            
if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
