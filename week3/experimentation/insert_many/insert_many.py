from week3.data_store.postgresql import Postgresql
from week3.util.csv_to_objects import read_csv_to_objects
from titanic import TitanicPassenger
from week3.data_store.elasticache import ElastiCache
from week3.data_store.dynamo_db import DynamoDB
import timeit
import week3.util.get_env as get_env
import pandas as pd

passengers = read_csv_to_objects('./titanic.csv', TitanicPassenger)
rds = Postgresql(*(get_env.get_rds()))
redshift = Postgresql(*(get_env.get_redshift()))
redis = ElastiCache()
dynamodb = DynamoDB()

def insert_passengers():
    results = []
    rds_insert_time = timeit.timeit(lambda: rds.insert_passengers(passengers), number=1)
    results.append(['rds', rds_insert_time])
    redshift_insert_time = timeit.timeit(lambda: redshift.insert_passengers(passengers), number=1)
    results.append(['redshift', redshift_insert_time])
    redis_insert_time = timeit.timeit(lambda: redis.insert_passengers(passengers), number=1)
    results.append(['redis', redis_insert_time])
    dynamodb_insert_time = timeit.timeit(lambda: dynamodb.insert_passengers(passengers), number=1)
    results.append(['dynamodb', dynamodb_insert_time])

    df = pd.DataFrame(results, columns=['DB', 'Time'])
    df.to_csv('./insert_many.csv', index=False)

insert_passengers()