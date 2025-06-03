import json
import os
import boto3
from botocore.exceptions import ClientError

from shared.User import User


def get_table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(os.environ["table_name"])

def handler(event, context, table=None):
    if table is None:
        table = get_table()

    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            username = body['username']
            increase_count = body['increase_count']
            if username is None or increase_count is None:
                raise ClientError(error_response='One or more parameters are missing', operation_name="update post count")

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