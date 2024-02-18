from postgresql import Postgresql
from csv_to_objects import read_csv_to_objects
from titanic import TitanicPassenger

import get_env

passengers = read_csv_to_objects('./titanic.csv', TitanicPassenger)
rds = Postgresql(get_env.get_rds())
rds.insert_passenger(passengers)
