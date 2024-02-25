from flask import Flask, request
import threading
import time
import pandas as pd

app = Flask(__name__)

start_time = None
event_queue = []
timer_running = False

total_events = 0
unique_events = set()
event_timestamps = []

def event_timer():
    global start_time, total_events, unique_events, event_timestamps, timer_running

    start_time = time.time()

    time.sleep(5)

    metrics_to_csv()

    total_events = 0
    unique_events = set()
    event_timestamps = []
    start_time = time.time()
    timer_running = False

def metrics_to_csv():
    global total_events, unique_events, event_timestamps, start_time

    end_time = time.time()

    duplicates = total_events - len(unique_events)

    unordered_events = count_unordered_events(event_timestamps)

    metrics_df = pd.DataFrame({
        'total_events': [total_events],
        'duplicates': [duplicates],
        'unordered_events': [unordered_events],
        'duration': [end_time-start_time]
    })

    # metrics_df.to_csv('./sns_metrics.csv', index=False)

    print("Total events received:", total_events)
    print("Duplicate events:", duplicates)
    print("Unordered events:", unordered_events)
    print("Time taken to receive events:", end_time - start_time, "seconds")

def count_unordered_events(events):
    unordered_events = 0
    max_timestamp = float('-inf')
    for timestamp in events:
        if timestamp < max_timestamp:
            unordered_events += 1
        else:
            max_timestamp = timestamp
    return unordered_events

@app.route('/event', methods=['POST'])
def handle_event():
    global total_events, unique_events, event_timestamps, timer_running

    event = request.data.decode('utf-8')
    print(event)
    
    if not timer_running:
        timer_thread = threading.Thread(target=event_timer)
        timer_thread.start()
        timer_running = True

    current_time = time.time()

    total_events += 1
    unique_events.add(event)
    event_timestamps.append(current_time)
    event_queue.append((event, current_time))

    return 'Event received'

@app.route('/')
def home():
    return 'Hello'

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000)
