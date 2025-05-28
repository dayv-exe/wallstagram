import json
from unittest.mock import MagicMock
import pytest
from src.handlers.add_post import handler


@pytest.fixture
def mock_table():
    # mock dynamodb table
    return MagicMock()


def test_handler_success(mock_table):
    mock_table.put_item.return_value = {}  # simulates successful insert into dynamodb
    mock_event = {'body': json.dumps({
        'message': 'test message',
        'author': 'test user'
    })}

    res = handler(event=mock_event, context={}, table=mock_table)
    assert res['statusCode'] == 201


def test_empty_param(mock_table):
    mock_table.put_item.return_value = {}  # simulates successful insert into dynamodb
    mock_event = {'body': json.dumps({
        '': 'test message',
        'author': 'test user'
    })}

    res = handler(event=mock_event, context={}, table=mock_table)
    assert res['statusCode'] == 400
    assert json.loads(res['body'])['error'] == "Invalid request body."

def test_empty_sender(mock_table):
    mock_table.put_item.return_value = {}  # simulates successful insert into dynamodb
    mock_event = {'body': json.dumps({
        'message': 'test message',
        'author': '   '
    })}

    res = handler(event=mock_event, context={}, table=mock_table)
    assert res['statusCode'] == 400
    assert json.loads(res['body'])['error'] == "Invalid request body."

def test_empty_message(mock_table):
    mock_table.put_item.return_value = {}  # simulates successful insert into dynamodb
    mock_event = {'body': json.dumps({
        'message': ' ',
        'author': 'test'
    })}

    res = handler(event=mock_event, context={}, table=mock_table)
    assert res['statusCode'] == 400
    assert json.loads(res['body'])['error'] == "Invalid request body."

def test_invalid_json_format(mock_table):
    mock_table.put_item.return_value = {}  # simulates successful insert into dynamodb
    mock_event = {'body': json.dumps({
        'author': 'test sender',
    })}

    res = handler(event=mock_event, context={}, table=mock_table)
    assert res['statusCode'] == 400
    assert json.loads(res['body'])['error'] == "Invalid request body."
