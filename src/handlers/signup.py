# adds user.
import json
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

from shared.User import User
from shared.response_body import invalid_request_error_res, created_successfully_res, server_error_res


def get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context, table=None):
    if table is None:
        # get table if none is parsed (for testing)
        table = get_table()

    try:
        body = json.loads(event['body'])  # loads content of the post body
        username = body['username']

        if len(username.strip()) < 1:
            # if posts data is incomplete
            return invalid_request_error_res()

        # create a new user object to send to the table
        table.put_item(Item=User(username=username, num_posts=0, date_joined=datetime.now()).database_format())  # add new user to db
        return created_successfully_res()

    except (json.JSONDecodeError, KeyError):
        # if there is a problem decoding the json parsed in request body
        return invalid_request_error_res()

    except (ClientError, Exception) as e:
        # somthing has gone terribly wrong :(
        print(e)  # print the error message and don't send it to client
        server_error_res()