import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
import boto3
import time
from week4.util.get_env import get_sqs_std

session = boto3.Session(profile_name='pyo')
sqs = session.client('sqs')
queue_url = get_sqs_std()

def receive_message(sqs, queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )
    if 'Messages' in response:
        message = response['Messages'][0]
        message_body = json.loads(message['Body'])
        print('Received message: ', message_body)
        # SQS 메시지 삭제
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])