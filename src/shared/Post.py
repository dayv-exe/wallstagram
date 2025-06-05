import json
from datetime import datetime


class Post:
    # -post (stores post metadata):
    #    pk: USERNAME#{username}, sk: POST#{post_date}#{post_id}, post_message
    def __init__(self, post_id: str, post_author: str, post_message: str, post_date: datetime):
        self.post_id = post_id
        self.post_author = post_author
        self.post_message = post_message
        self.post_date = post_date

    def database_format(self):
        return {
            'pk': f"USERNAME#{self.post_author}",
            'sk': f"POST#{self.post_date}#{self.post_id}",
            'post_body': self.post_message,
        }

    @staticmethod
    def database_key(compound_post_id: str):
        post_info = compound_post_id.split('#')

        username = post_info[1]
        post_uuid = post_info[0]
        post_date = post_info[2]

        return {
            'pk': f'USERNAME#{username}',
            'sk': f'POST#{post_date}#{post_uuid}'
        }

    @staticmethod
    def json_format(pk: str, sk: str, post_message: str):
        post_meta_arr = sk.split("#")

        post_id = post_meta_arr[2]
        post_author = pk.split("#")[1]
        post_date = post_meta_arr[1]

        return {
            'id': f'{post_id}#{post_author}#{post_date}',
            'author': post_author,
            'message': post_message,
            'date': post_date
        }