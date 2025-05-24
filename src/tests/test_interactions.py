import json
from unittest.mock import MagicMock
from src.handlers.interactions import handler

import pytest


@pytest.fixture
def mock_table():
    return MagicMock()

def test_follow_operation(mock_table):
    # test 1: simulate a successful follow
    current_user = "ronaldo"
    user_to_follow = "messi"
    mock_table.put_item.return_value = {}
    mock_event = {
        'pathParameters': {
            'username': user_to_follow,
            'operation': 'follow'
        },
        'body': json.dumps({
            'username': current_user
        })
    }
    res = handler(event=mock_event, context=None, table=mock_table)
    assert res['statusCode'] == 200
    assert json.loads(res['body'])['message'] == f"{current_user} now follows {user_to_follow}"

def test_follow_operation_invalid_username(mock_table):
    # test 2: simulate an unsuccessful follow due to invalid username
    current_user = " "
    user_to_follow = "messi"
    mock_table.put_item.return_value = {}
    mock_event = {
        'pathParameters': {
            'username': user_to_follow,
            'operation': 'follow'
        },
        'body': json.dumps({
            'username': current_user
        })
    }
    res = handler(event=mock_event, context=None, table=mock_table)
    assert res['statusCode'] == 400
    assert json.loads(res['body'])['error'] == f"Invalid request."

def test_follow_operation_invalid_other_username(mock_table):
    # test 3: simulate an unsuccessful follow due to invalid username
    current_user = "ronaldo"
    user_to_follow = " "
    mock_table.put_item.return_value = {}
    mock_event = {
        'pathParameters': {
            'username': user_to_follow,
            'operation': 'follow'
        },
        'body': json.dumps({
            'username': current_user
        })
    }
    res = handler(event=mock_event, context=None, table=mock_table)
    assert res['statusCode'] == 400
    assert json.loads(res['body'])['error'] == f"Invalid request."

def test_unfollow_operation(mock_table):
    # test 4: simulate a successful unfollow
    current_user = "ronaldo"
    user_to_unfollow = "messi"
    mock_table.put_item.return_value = {}
    mock_event = {
        'pathParameters': {
            'username': user_to_unfollow,
            'operation': 'unfollow'
        },
        'body': json.dumps({
            'username': current_user
        })
    }
    res = handler(event=mock_event, context=None, table=mock_table)
    assert res['statusCode'] == 200
    assert json.loads(res['body'])['message'] == f"{current_user} unfollowed {user_to_unfollow}"

def test_unfollow_operation_invalid_username(mock_table):
    # test 5: simulate an unsuccessful unfollow due to invalid username
    current_user = " "
    user_to_unfollow = "messi"
    mock_table.put_item.return_value = {}
    mock_event = {
        'pathParameters': {
            'username': user_to_unfollow,
            'operation': 'unfollow'
        },
        'body': json.dumps({
            'username': current_user
        })
    }
    res = handler(event=mock_event, context=None, table=mock_table)
    assert res['statusCode'] == 400
    assert json.loads(res['body'])['error'] == f"Invalid request."

def test_unfollow_operation_invalid_other_username(mock_table):
    # test 6: simulate an unsuccessful unfollow due to invalid username
    current_user = "ronaldo"
    user_to_unfollow = " "
    mock_table.put_item.return_value = {}
    mock_event = {
        'pathParameters': {
            'username': user_to_unfollow,
            'operation': 'unfollow'
        },
        'body': json.dumps({
            'username': current_user
        })
    }
    res = handler(event=mock_event, context=None, table=mock_table)
    assert res['statusCode'] == 400
    assert json.loads(res['body'])['error'] == f"Invalid request."

def test_invalid_operation(mock_table):
    # test 7: simulate an unsuccessful run due to invalid operation
    current_user = "ronaldo"
    user_to_unfollow = "messi"
    mock_table.put_item.return_value = {}
    mock_event = {
        'pathParameters': {
            'username': user_to_unfollow,
            'operation': 'random'
        },
        'body': json.dumps({
            'username': current_user
        })
    }
    res = handler(event=mock_event, context=None, table=mock_table)
    assert res['statusCode'] == 400
    assert json.loads(res['body'])['error'] == f"Invalid request."