import sys
sys.path.append('/home/ubuntu/code/INFRA-study')
from week3.data_store.postgresql import Postgresql
from week3.util.csv_to_objects import read_csv_to_objects
from week3.titanic import TitanicPassenger
from week3.data_store.elasticache import ElastiCache
from week3.data_store.dynamo_db import DynamoDB
import week3.util.get_env as get_env
import timeit
import pandas as pd

rds = Postgresql(*(get_env.get_rds()))
redshift = Postgresql(*(get_env.get_redshift()))
redis = ElastiCache()
dynamodb = DynamoDB()
passenger = TitanicPassenger(999,1,1,"pyo",'male',27,1,0,"A/5 21171",7,None,'S')

def get_passenger_by_id():
    results = []

    rds_insert_time = timeit.timeit(lambda: rds.get_passenger_by_id(999), number=1)
    results.append(['rds', rds_insert_time])

    redshift_insert_time = timeit.timeit(lambda: redshift.get_passenger_by_id(999), number=1)
    results.append(['redshift', redshift_insert_time])

    redis_insert_time = timeit.timeit(lambda: redis.get_passenger_by_id(999), number=1)
    results.append(['redis', redis_insert_time])

    dynamodb_insert_time = timeit.timeit(lambda: dynamodb.get_passenger_by_id(999, 27), number=1)
    results.append(['dynamodb', dynamodb_insert_time])

    df = pd.DataFrame(results, columns=['DB', 'Time'])
    df.to_csv('./select_one.csv', index=False)

get_passenger_by_id()