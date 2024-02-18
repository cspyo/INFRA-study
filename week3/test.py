from postgresql import Postgresql
from csv_to_objects import read_csv_to_objects
from titanic import TitanicPassenger
from elasticache import ElastiCache
from dynamo_db import DynamoDB
import timeit
import get_env
import pandas as pd

passengers = read_csv_to_objects('./titanic.csv', TitanicPassenger)
rds = Postgresql(get_env.get_rds())
redshift = Postgresql(get_env.get_redshift())
redis = ElastiCache()
dynamodb = DynamoDB()

def insert_test():
    results = []
    rds_insert_time = timeit.timeit(lambda: rds.insert_passenger(passengers), number=1)
    results.append(['rds', rds_insert_time])
    redshift_insert_time = timeit.timeit(lambda: redshift.insert_passenger(passengers), number=1)
    results.append(['redshift', redshift_insert_time])
    redis_insert_time = timeit.timeit(lambda: redis.insert_passenger(passengers), number=1)
    results.append(['redis', redis_insert_time])
    dynamodb_insert_time = timeit.timeit(lambda: dynamodb.insert_passenger(passengers), number=1)
    results.append(['dynamodb', dynamodb_insert_time])

    df = pd.DataFrame(results, columns=['DB', 'Time'])
    df.to_csv('./insert_test.csv', index=False)

def select_test():
    results =[]
    rds_select_time = timeit.timeit(lambda: rds.get_passengers_order_by_name(), number=1)
    results.append(['rds', rds_select_time])
    redshift_select_time = timeit.timeit(lambda: redshift.get_passengers_order_by_name(), number=1)
    results.append(['redshift', redshift_select_time])
    redis_select_time = timeit.timeit(lambda: redis.get_passengers_order_by_name(passengers), number=1)
    results.append(['redis', redis_select_time])
    dynamodb_select_time = timeit.timeit(lambda: dynamodb.get_passengers_order_by_name(passengers), number=1)
    results.append(['dynamodb', dynamodb_select_time])

    df = pd.DataFrame(results, columns=['DB', 'Time'])
    df.to_csv('./select_test.csv', index=False)

def update_test():
    results = []
    rds_update_time = timeit.timeit(lambda: rds.update_passenger(passengers[0]), number=1)
    results.append(['rds', rds_update_time])
    redshift_update_time = timeit.timeit(lambda: redshift.update_passenger(passengers[0]), number=1)
    results.append(['redshift', redshift_update_time])
    redis_update_time = timeit.timeit(lambda: redis.update_passenger(passengers[0]), number=1)
    results.append(['redis', redis_update_time])
    dynamodb_update_time = timeit.timeit(lambda: dynamodb.update_passenger(passengers[0]), number=1)
    results.append(['dynamodb', dynamodb_update_time])

    df = pd.DataFrame(results, columns=['DB', 'Time'])
    df.to_csv('./update_test.csv', index=False)

def delete_test():
    results = []
    rds_delete_time = timeit.timeit(lambda: rds.delete_passenger(passengers[0].id), number=1)
    results.append(['rds', rds_delete_time])
    redshift_delete_time = timeit.timeit(lambda: redshift.delete_passenger(passengers[0].id), number=1)
    results.append(['redshift', redshift_delete_time])
    redis_delete_time = timeit.timeit(lambda: redis.delete_passenger(passengers[0].id), number=1)
    results.append(['redis', redis_delete_time])
    dynamodb_delete_time = timeit.timeit(lambda: dynamodb.delete_passenger(passengers[0]), number=1)
    results.append(['dynamodb', dynamodb_delete_time])

    df = pd.DataFrame(results, columns=['DB', 'Time'])
    df.to_csv('./delete_test.csv', index=False)


insert_test()
select_test()
update_test()
delete_test()