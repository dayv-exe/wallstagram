# adds post.
import json
import os
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


def get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, _, table=None):
    if table is None:
        # get table if none is parsed (for testing)
        table = get_table()

    try:
        body = json.loads(event['body'])  # loads content of the post body
        post_id = str(uuid.uuid4())  # generates random uuid
        post_message = str(body['message'])
        post_sender: str = body['sender']
        post_date = str(datetime.now())  # gets current date and time

        if len(post_message.strip()) < 1 or len(post_sender.strip()) < 2:
            # if post data is incomplete
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Invalid request body.'
                })
            }

        # create new post object to send to db
        new_post = {
            'id': post_id,
            'message': post_message,
            'sender': post_sender,
            'date_added': post_date
        }
        table.put_item(Item=new_post)  # add new post to db
        return {
            # everything is okay :)
            'statusCode': 201,
            'body': json.dumps({
                'message': post_id
            })
        }
    except (json.JSONDecodeError, KeyError):
        # if there is a problem decoding the json parsed in request body
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Invalid request body.'
            })
        }

    except ClientError as e:
        # somthing has gone terribly wrong :(
        print(e)  # print the error message and don't send it to client
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Somthing went wrong, try again.'
            })
        }