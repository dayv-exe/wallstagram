import json
from datetime import datetime

# pk: USERNAME#{username}, sk: USER, num_posts:{num_of_posts}, date_joined: {date_joined}

class User:
    def __init__(self, username: str, num_posts: int, date_joined: datetime):
        self.username = username
        self.date_joined = date_joined
        self.num_posts = num_posts

    @staticmethod
    def database_key(username: str) -> dict[str, str]:
        return {
            'pk': f'USERNAME#{username}',
            'sk': 'USER'
        }

    def database_format(self) -> dict[str, str]:
        # formats the user info for storage in dynamodb following our access pattern
        return {
            'pk': f"USERNAME#{self.username}",
            'sk': f"USER",
            'post_count': self.num_posts,
            'date_joined': f"{self.date_joined}",
        }

    @staticmethod
    def json_format(pk: str, num_posts: int, date_joined: datetime):
        # converts user details gotten from dynamodb to readable JSON format using our access pattern
        username = pk.split('#')[1]
        return {
            'username': username,
            'post_count': num_posts,
            'date_joined': str(date_joined)
        }