# handles following or unfollowing
import json
import os

import boto3
from botocore.exceptions import ClientError

from shared.Interaction import Follow
from shared.response_body import invalid_request_error_res, created_successfully_res, server_error_res, \
    request_success_res


def handle_follow(this_user, other_user, table):
    # insert into the table pk: USERNAME#{this_user}, sk: FOLLOWS#{other_user} to store follower data
    try:
        if (len(this_user.strip()) < 2 or len(other_user.strip()) < 2) or this_user == other_user:
            return invalid_request_error_res()

        table.put_item(Item=Follow(this_user, other_user).database_format())
        return created_successfully_res()

    except (json.JSONDecodeError, KeyError):
        return invalid_request_error_res()

    except (ClientError, Exception) as e:
        return server_error_res(e)


def handle_unfollow(this_user, other_user, table):
    # delete from the table pk: USERNAME#{this_user}, sk: FOLLOWS#{other_user} to store follower data
    try:
        if len(this_user.strip()) < 2 or len(other_user.strip()) < 2:
            return invalid_request_error_res()

        table.delete_item(Key=Follow(this_user, other_user).database_format())
        return request_success_res()

    except (json.JSONDecodeError, KeyError):
        return invalid_request_error_res()

    except (ClientError, Exception) as e:
        return server_error_res(e)


def handle_like(this_user, other_post, table):
    pass


def handle_unlike(this_user, other_post, table):
    pass


def handle_comment(this_user, other_post, table):
    pass


def handle_uncomment(this_user, other_post, table):
    pass

OPERATIONS = {
    'follow': handle_follow,
    'unfollow': handle_unfollow
}

def get_table():
    # returns table associated with this function
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context, table=None):
    # /user/{operation}/{target}
    # in the case of follow, target is username, in case of like or comment target is a post_id
    if table is None:
        table = get_table()

    body = json.loads(event['body'])

    this_user = body['username']
    target = event['pathParameters']['target']
    operation = event['pathParameters']['operation']

    if operation in OPERATIONS:
        # if a valid operation is to be carried out
        return OPERATIONS[operation](this_user, target, table)
    else:
        # if the operation in the url is invalid
        return invalid_request_error_res()