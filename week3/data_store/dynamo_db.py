import boto3
from week3.util.csv_to_objects import read_csv_to_objects

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
            response = self.table.get_item(Key={'id': partition_key_value, 'age': sort_key_value})
        else:
            response = self.table.get_item(Key={'id': partition_key_value})
    
        item = response.get('Item')
        if item:
            print("Retrieved item:", item)
        else:
            print("Item not found.")
    
    def insert_passengers(self, passengers):
        for passenger in passengers:
            self.insert_data(data=passenger.to_dict())
    
    def insert_passenger(self, passenger):
        self.insert_data(data=passenger.to_dict())

    def get_passenger_by_id(self, id, age):
        return self.get_data(partition_key_value=id, sort_key_value=age)

    def get_passengers_by_age(self, age):
        response = self.table.scan(
            FilterExpression='age = :age',
            ExpressionAttributeValues={':age': {'N': str(age)}}
        )
        return response['Items']
    
    def get_passengers_range_age(self, age):
        response = self.table.scan(
            FilterExpression='age > :age',
            ExpressionAttributeValues={':age': {'N': str(age)}}
        )
        return response['Items']
    
    def get_passengers_order_by_age(self):
        response = self.table.scan()
        sorted_items = sorted(response['Items'], key=lambda x: x['age'])
        return sorted_items

    
    def update_name_by_id(self, name, id):
        update_expression = "SET #nm = :name_val"
        expression_attribute_names = {"#nm": "embarked"}
        expression_attribute_values = {":name_val": name}

        response = self.table.update_item(
            Key={'id': id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"  
        )
        updated_item = response['Attributes']
        return updated_item

    def delete_passenger(self, passenger):
        response = self.table.delete_item(Key={'id': passenger.id, 'name': passenger.name})
        return response