# handles following or unfollowing
import json
import os

import boto3
from botocore.exceptions import ClientError


#-users (stores users metadata):
#    pk: USERNAME#{username}, sk: META, date_joined (post table)
#    pk: USERNAME#{username}, sk: FOLLOWS#{username}  # to store follower data

def handle_follow(this_user, other_user, table):
    # insert into the table pk: USERNAME#{this_user}, sk: FOLLOWS#{other_user} to store follower data
    try:
        if len(this_user.strip()) < 2 or len(other_user.strip()) < 2:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Invalid request.'
                })
            }

        new_data = {
            'pk': f'USERNAME#{this_user}',
            'sk': f'FOLLOWS#{other_user}'
        }
        table.put_item(Item=new_data)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'{this_user} now follows {other_user}'
            })
        }
    except (json.JSONDecodeError, KeyError):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Invalid request.'
            })
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Somthing went wrong.'
            })
        }


def handle_unfollow(this_user, other_user, table):
    # delete from the table pk: USERNAME#{this_user}, sk: FOLLOWS#{other_user} to store follower data
    try:
        if len(this_user.strip()) < 2 or len(other_user.strip()) < 2:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Invalid request.'
                })
            }

        table.delete_item(Key={
            'pk': f'USERNAME#{this_user}',
            'sk': f'FOLLOWS#{other_user}'
        })
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'{this_user} unfollowed {other_user}'
            })
        }
    except (json.JSONDecodeError, KeyError):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Invalid request.'
            })
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Somthing went wrong.'
            })
        }

OPERATIONS = {
    'follow': handle_follow,
    'unfollow': handle_unfollow
}

def get_table():
    # returns table associated with this function
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(os.environ['POSTS_TABLE_NAME'])

def handler(event, context, table=None):
    # /user/{username}/{operation}
    if table is None:
        table = get_table()

    body = json.loads(event['body'])

    this_user = body['username']
    other_user = event['pathParameters']['username']
    operation = event['pathParameters']['operation']

    if operation in OPERATIONS:
        # if a valid operation is to be carried out
        return OPERATIONS[operation](this_user, other_user, table)
    else:
        # if the operation in the url is invalid
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Invalid request.'
            })
        }