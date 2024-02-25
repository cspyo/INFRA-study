import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
from flask import Flask, request
import json
from event_handler import handle_event

app = Flask(__name__)

@app.route('/event', methods=['POST'])
def listen_event():
    request_data = request.data.decode('utf-8')
    event_dict = json.loads(request_data)
    timestamp = int(event_dict['Timestamp'])
    message_id = event_dict['MessageId']
    handle_event('sns', message_id, timestamp)
    return 'Event received'

@app.route('/')
def home():
    return 'Hello'

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000)