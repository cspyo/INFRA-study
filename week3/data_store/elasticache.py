import redis
import json
from week3.util.get_env import get_elasticache

class ElastiCache:
    def __init__(self):
        host, port = get_elasticache()
        self.client = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def delete(self, key):
        self.client.delete(key)

    def exists(self, key):
        return self.client.exists(key)

    def keys(self, pattern):
        return self.client.keys(pattern)

    def flush_all(self):
        self.client.flushall()
    
    def insert_passengers(self, passengers):
        for passenger in passengers:
            self.set(passenger.id, json.dumps(passenger.to_dict()))
    
    def insert_passenger(self, passenger):
        self.set(passenger.id, json.dumps(passenger.to_dict()))

    def get_passenger_by_id(self, id):
        return self.get(id)
    
    def get_passengers_by_age(self, age):
        all_passengers = self.keys('*')
        results = []
        for passenger in all_passengers:
            passenger = json.loads(self.get(passenger))
            if passenger['age'] == age:
                results.append(passenger)
        return results
    
    def get_passengers_range_age(self, age):
        all_passengers = self.keys('*')
        results = []
        for passenger in all_passengers:
            passenger = json.loads(self.get(passenger))
            if passenger['age'] > age:
                results.append(passenger)
        return results

    def get_passengers_order_by_age(self, passengers):
        result = []
        for passenger in passengers:
            result.append(self.get(passenger.id))
        return sorted(result, key=lambda result: result.age)
    
    def update_passenger(self, passenger):
        new_passenger = {
            'id': passenger.id,
            'name': 'pyo',
            'survived': passenger.survived,
            'p_class': passenger.p_class,
            'sex': passenger.sex,
            'age': passenger.age,
            'sibsp': passenger.sibsp,
            'parch': passenger.parch,
            'ticket': passenger.ticket,
            'fare': passenger.fare,
            'cabin': passenger.cabin,
            'embarked': passenger.embarked
        }
        self.set(passenger.id, new_passenger)

    def delete_passenger(self, id):
        self.delete(id)
        