from shared.User import User


def user_exists(username: str, table) -> bool:
    response = table.get_item(Key= User.database_key(username))
    user = response.get('Item')
    return user is not None