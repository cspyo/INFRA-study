import time
import concurrent.futures

def emit_event(emit_function):
    num_events_per_second = 100
    seconds_for_publish = 60

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(seconds_for_publish):
            executor.map(emit_function, range(num_events_per_second))
            time.sleep(1) 
    end_time = time.time()

    print("Total publish time", end_time-start_time)
    print("Total publish count", num_events_per_second*seconds_for_publish)