import json
import os
import boto3
from botocore.exceptions import ClientError

from shared.Post import Post
from shared.response_body import not_found_res, retrieved_item_res, invalid_request_error_res, server_error_res


def get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context, table=None):
    if table is None:
        table = get_table()

    # checks database for post id and returns it
    post_id = event['pathParameters']['post_id']

    try:
        response = table.get_item(Key=Post.database_key(post_id))
        post = response.get('Item')

        if post is None:
            return not_found_res('Post not found.')

        return retrieved_item_res({
            'content': post
        })

    except (json.JSONDecodeError, KeyError):
        return invalid_request_error_res()

    except (Exception, ClientError) as e:
        return server_error_res(e)
