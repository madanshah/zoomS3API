import datetime
from datetime import date, timedelta
import os
import boto3

dynamodb = boto3.resource('dynamodb',
             aws_access_key_id=os.environ["ACCESS_KEY_ID"],
             aws_secret_access_key =os.environ["ACCESS_SECRET_KEY"],
             region_name=os.environ["AWS_REGION"])

from boto3.dynamodb.conditions import Key, Attr
# add= 10
# current = date.today().isoformat()
# expire = (date.today() + timedelta(days=add)).isoformat()
# print(type(current))
# print(expire)

# email = "madan.shah@genesesolution.com"
# # userName = request.form['userName']
# password = "Alpha@00"
# table = dynamodb.Table('zoomUser')
# response = table.query(KeyConditionExpression=Key('email').eq(email))
# items = response['Items']
# print(items)
# name = items[0]['userName']
# if password == items[0]['password']:
#     print(name)
#     print(items[0])


a = ""
print(a)
def apple(x):
    a = x
    print(a)

b = apple(apple)
print(a)

