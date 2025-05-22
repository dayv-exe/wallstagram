# adds post
import json
import os
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


def get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context, table=None):
    if table is None:
        table = get_table()

    try:
        body = json.loads(event['body'])
        post_id = str(uuid.uuid4())

        post_date = str(datetime.now())
        new_post = {
            'id': post_id,
            'message': body['message'],
            'sender': body['sender'],
            'date_added': post_date
        }

        table.put_item(Item=new_post)

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': f'Added new post with id {post_id}'
            })
        }
    except (json.JSONDecodeError, KeyError):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Post data is incomplete.'
            })
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Somthing went wrong, try again.'
            })
        }