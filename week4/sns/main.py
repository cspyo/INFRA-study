from flask import Flask, request
import threading
import time

app = Flask(__name__)

# 이벤트 수신 시간 기록을 위한 변수
start_time = None
event_queue = []
timer_running = False

# 수신된 이벤트를 저장할 변수들
total_events = 0
unique_events = set()
event_timestamps = []

def event_timer():
    global start_time, total_events, unique_events, event_timestamps, timer_running

    # 타이머 시작 시간 기록
    start_time = time.time()

    # 60초 대기
    time.sleep(60)

    # 타이머 종료 후 지표 출력
    print_metrics()

    # 변수 초기화
    total_events = 0
    unique_events = set()
    event_timestamps = []
    start_time = time.time()
    timer_running = False

def print_metrics():
    global total_events, unique_events, event_timestamps, start_time

    # 마지막 이벤트 수신 시간 기록
    end_time = time.time()

    # 중복된 이벤트 개수 계산
    duplicates = total_events - len(unique_events)

    # 순서가 보장되지 않은 이벤트 개수 계산
    unordered_events = count_unordered_events(event_timestamps)

    # 연산 결과 출력
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

    # 이벤트 수신
    event = request.data.decode('utf-8')
    print(event)
    print(request)
    
    if not timer_running:
        # 타이머가 실행 중이 아니면 타이머 시작
        timer_thread = threading.Thread(target=event_timer)
        timer_thread.start()
        timer_running = True

    # 현재 시간 기록
    current_time = time.time()

    # 이벤트 연산
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
