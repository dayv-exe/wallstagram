# adds post.
import json
import os
import uuid
from datetime import datetime
from math import trunc

import boto3
from botocore.exceptions import ClientError

from shared.Interaction import PostCountData
from shared.Post import Post
from shared.response_body import invalid_request_error_res, created_successfully_res, server_error_res


def get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['TABLE_NAME'])


def send_to_sqs(post_count_data: PostCountData) -> bool:
    # triggers a lambda function that increases user count by one
    sqs = boto3.client('sqs')
    QUEUE_URL = os.environ['QUEUE_URL']

    try:
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=post_count_data.json_format()
        )
    except (ClientError, Exception) as e:
        print(e)
        return False

    return True


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
        queued = send_to_sqs(PostCountData(post_author, True))  # to increase the post count by one for this user
        if not queued:
            raise Exception("Failed to queue post count!")
        return created_successfully_res()

    except (json.JSONDecodeError, KeyError):
        # if there is a problem decoding the json parsed in request body
        return invalid_request_error_res()

    except (ClientError, Exception) as e:
        # somthing has gone terribly wrong :(
        return server_error_res(e)