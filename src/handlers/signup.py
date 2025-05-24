# adds user.
import json
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

#-users (stores users metadata):
#    pk: USERNAME#{username}, sk: META, date_joined (post table)
#    pk: USERNAME${username}, sk: FOLLOWS#{username}  # to store follower data

def get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['USERS_TABLE_NAME'])

def handler(event, context, table=None):
    if table is None:
        # get table if none is parsed (for testing)
        table = get_table()

    try:
        body = json.loads(event['body'])  # loads content of the post body
        username = body['username']
        date_joined = str(datetime.now())

        if len(username.strip()) < 1:
            # if post data is incomplete
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Invalid request body.'
                })
            }

        # create new user object to send to post db
        new_post = {
            'pk': f"USERNAME#{username}",
            'sk': f"META",
            'date_joined': date_joined
        }

        table.put_item(Item=new_post)  # add new user to db
        return {
            # everything is okay :)
            'statusCode': 201,
            'body': json.dumps({
                'message': f"Added {username} successfully."
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