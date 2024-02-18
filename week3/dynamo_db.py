import boto3
from csv_to_objects import read_csv_to_objects
from titanic import TitanicPassenger

class DynamoDB:
    def __init__(self):
        session = boto3.Session(profile_name='pyo')
        client = session.resource('dynamodb')
        self.table_name = "pyo-passenger"
        self.table = client.Table(self.table_name)
    
    def insert_data(self, data):
        return self.table.put_item(Item=data)

    def get_data(self, partition_key_value, sort_key_value = None):
        if sort_key_value:
            response = self.table.get_item(Key={'id': partition_key_value, 'name': sort_key_value})
        else:
            response = self.table.get_item(Key={'id': partition_key_value})
    
        item = response.get('Item')
        if item:
            print("Retrieved item:", item)
        else:
            print("Item not found.")


def main():
    dynamo = DynamoDB()
    passengers = read_csv_to_objects('./titanic.csv', TitanicPassenger)
    for passenger in passengers:
        dynamo.insert_data(data=passenger.to_dict())
    dynamo.get_data(partition_key_value=1, sort_key_value='Braund, Mr. Owen Harris')

main()