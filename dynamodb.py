import os
import boto3

AWS_DEFAULT_REGION = os.environ["AWS_REGION"]
ACCESS_KEY_ID = os.environ["ACCESS_KEY_ID"]
ACCESS_SECRET_KEY =  os.environ["ACCESS_SECRET_KEY"]
# AWS_SESSION_TOKEN = os.environ["AWS_SESSION_TOKEN"]

print(AWS_DEFAULT_REGION)
print(ACCESS_KEY_ID)
print(ACCESS_SECRET_KEY)
# print(AWS_SESSION_TOKEN)

dynamodb = boto3.resource('dynamodb',
             aws_access_key_id=os.environ["ACCESS_KEY_ID"],
             aws_secret_access_key =os.environ["ACCESS_SECRET_KEY"],
             region_name=os.environ["AWS_REGION"])

table = dynamodb.create_table(
    TableName = 'zoomUser',
    KeySchema = [
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits':5,
        'WriteCapacityUnits':5
    }
) 

table.meta.client.get_waiter('table_exists').wait(TableName='zoomUser')

print(table.item_count)