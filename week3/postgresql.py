import psycopg2
from dotenv import load_dotenv
import os 

class Postgresql:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def get_connection(self):
        if self.conn is not None:
            return self.conn
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return self.conn
        except (Exception, psycopg2.Error) as error:
            print("오류 발생:", error)

    def insert_passenger(self, passengers):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            for passenger in passengers:
                sql = f"INSERT INTO passenger (id, survived, p_class, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, passenger.to_tuple())
            conn.commit()
            cursor.close()
        except (Exception, psycopg2.Error) as error:
            print("오류 발생:", error)


        