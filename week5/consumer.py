from confluent_kafka import Consumer, KafkaError
import time
import threading

class MyConsumer:
    consumer = None
    topic = ""

    def __init__(self, topic):
        config  = {
            'bootstrap.servers': 'localhost:9092,localhost:10092,localhost:11092',
            'group.id': 'event-handler-group',
            'auto.offset.reset': 'earliest'
        }
        self.topic = topic
        self.consumer = Consumer(config)
        self.consumer.subscribe([topic])

    def consume(self):
        total_events_processed = 0
        start_time = time.time()

        while time.time() - start_time < 1:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            total_events_processed += 1

        self.consumer.close()
        print(f"Topic: {self.topic}")
        print(f"Total events processed: {total_events_processed}")
        return total_events_processed


topics = ['test-1', 'test-3', 'test-5']
handlers = [1, 3, 5]
results = []

consumer = MyConsumer(topics[0])
consumer_thread = threading.Thread(target=consumer.consume)
consumer_thread.start()
results.append(consumer_thread)


