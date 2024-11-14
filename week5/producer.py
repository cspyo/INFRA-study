import json
import time
from confluent_kafka import Producer
import pandas as pd
import matplotlib.pyplot as plt

class MessageProducer:
    brokers = ""
    topic = ""
    producer = None
    results = []
    acks = ""

    def __init__(self, brokers, topic, acks):
        config  = {
            'bootstrap.servers': brokers,
            'client.id': 'message-producer',
            'acks': acks
        }
        self.acks = acks
        self.topic = topic
        self.producer = Producer(**config)
        self.results = []

    def delivery_report(self, err, msg):
        end_time = time.time()
        if err is not None:
            print(f"메시지 전송 실패: {err}")
        else:
            start_time = json.loads(msg.value())['timestamp']
            duration = end_time - float(start_time)
            key = msg.key().decode('utf-8')

            new_row = [int(key), start_time,  end_time,  duration]
            self.results.append(new_row)

    def produce_message(self):
        count = 0
        start_time = time.time()
        print("메세지 전송 시작")

        while time.time() - start_time < 100:
            key = str(count)
            value = {'timestamp': time.time()}

            try:
                self.producer.produce(self.topic, key=key, value=json.dumps(value), callback=self.delivery_report)
                self.producer.flush()
            except Exception as e:
                print(f"메시지 생성 실패: {e}")
            
            count += 1
        
        print("메세지 전송 끝")

        df = pd.DataFrame(self.results, columns=['key', 'start_time', 'end_time', 'duration'])
        # df.to_csv(f'producer_{self.acks}.csv', index=False)
        avg = df['duration'].mean()
        count = df['key'].count()

        return count, avg        
        


results = []

brokers = "localhost:9092,localhost:10092,localhost:11092"
# topic = "test-1"

# acks_list = ["0", "1", "all"]

# for acks in acks_list:
#     producer = MessageProducer(brokers, topic, acks)
#     produce_count, avg = producer.produce_message()
#     results.append([acks, produce_count, avg])
#     print(f"acks: {acks}, produce_count: {produce_count}, avg: {avg}")

topics = ["test-1", "test-3", "test-5"]
acks = "0"

for topic in topics:
    producer = MessageProducer(brokers, topic, acks)
    produce_count, avg = producer.produce_message()
    # results.append([acks, produce_count, avg])
    # print(f"acks: {acks}, produce_count: {produce_count}, avg: {avg}")

# acks = "0"
# producer = MessageProducer(brokers, topic, acks)
# produce_count, avg = producer.produce_message()
# # results.append([acks, produce_count, avg])
# print(f"acks: {acks}, produce_count: {produce_count}, avg: {avg}")

# df = pd.DataFrame(results, columns=['acks', 'produce_count', 'avg'])
# df.to_csv('producer.csv', index=False)

