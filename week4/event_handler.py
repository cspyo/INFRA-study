import threading
import time
import pandas as pd

start_time = None
timer_running = False

total_events = 0
unique_events = set()
event_timestamps = []

def event_timer(queue_name):
    global start_time, total_events, unique_events, event_timestamps, timer_running
    start_time = time.time()
    time.sleep(60)
    metrics_to_csv(queue_name)

def metrics_to_csv(queue_name):
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

    csv_name = f'/home/ubuntu/code/INFRA-study/week4/metrics/{queue_name}_metrics.csv'
    metrics_df.to_csv(csv_name, index=False)

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

def handle_event(queue_name, message_id, message_timestamp):
    global total_events, unique_events, event_timestamps, timer_running

    if not timer_running:
        print("timer start")
        timer_thread = threading.Thread(target=event_timer, args=(queue_name,))
        timer_thread.start()
        timer_running = True

    total_events += 1
    unique_events.add(message_id)
    event_timestamps.append(message_timestamp)
