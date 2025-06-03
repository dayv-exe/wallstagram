import json
import os
import boto3
from botocore.exceptions import ClientError

from shared.User import User


def get_table():
    # injects table
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['TABLE_NAME'])

def user_exists(username: str, table) -> bool:
    response = table.get_item(Key= User.database_key(username))
    user = response.get('Item')
    return user is not None

def handler(event, context, table=None):
    if table is None:
        # allows function to be tested without a real dynamodb table
        table = get_table()

    for record in event['Records']:
        try:

            body = json.loads(record['body'])  # extracts body from pipeline or whatever
            username = body['username']  # gets username
            increase_count = body['increase_count']  # gets whether we will increase count on user data
            if username is None or increase_count is None or not user_exists(username, table):
                # if data from sqs is incomplete
                continue

            # to actually update the table
            table.update_item(
                Key=User.database_key(username),
                UpdateExpression='ADD post_count :inc' if increase_count else 'ADD post_count :dec',
                ExpressionAttributeValues={':inc': 1} if increase_count else {':dec': -1}
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f'FATAL ERROR: Invalid JSON or key error in record: {record}. Details:{e}')
            raise e  # to retry or send to dead letter queue
        except ClientError as e:
            print(f'FATAL ERROR: Details:{e}')
            raise e  # to retry or send to dlq