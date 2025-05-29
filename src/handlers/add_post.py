# adds post.
import json
import os
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

from shared.Post import Post
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
        post_message = str(body['message'])
        post_author: str = body['author']

        if len(post_message.strip()) < 1 or len(post_author.strip()) < 2:
            # if post data is incomplete
            return invalid_request_error_res()

        # create new post object to send to post db
        new_post = Post(
            post_id=str(uuid.uuid4()),
            post_author=post_author,
            post_message=post_message,
            post_date=datetime.now()
        ).database_format()
        table.put_item(Item=new_post)  # add new post to db
        return created_successfully_res()

    except (json.JSONDecodeError, KeyError):
        # if there is a problem decoding the json parsed in request body
        return invalid_request_error_res()

    except (ClientError, Exception) as e:
        # somthing has gone terribly wrong :(
        return server_error_res(e)