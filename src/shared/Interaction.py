import json


class Follow:
    # pk: USERNAME#{this_user}, sk: FOLLOWS#{other_user}
    def __init__(self, follower_username: str, following_username: str):
        self.follower = follower_username
        self.following = following_username

    def database_format(self):
        return {
            'pk': f'USERNAME#{self.follower}',
            'sk': f'FOLLOWS#{self.following}'
        }

    @staticmethod
    def json_format(self, pk: str, sk: str):
        follower = pk.split("#")[1]
        following = sk.split("#")[1]
        return {
            'follower': follower,
            'following': following
        }

class PostCountData:
    def __init__(self, username: str, increase_post_count: bool):
        self.username = username
        self.increase_post_count = increase_post_count

    def json_format(self):
        return json.dumps({
            'username': self.username,
            'increase_count': self.increase_post_count
        })