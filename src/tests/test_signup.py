import json
from unittest.mock import MagicMock
import pytest
from src.handlers.signup import handler


@pytest.fixture
def mock_table():
    # mock dynamodb table
    return MagicMock()

def test_valid_user(mock_table):
    # simulate what should be a successful sign up
    mock_table.put_item.return_value = {}
    mock_event = {
        'body': json.dumps({
            'username': "test"
        })
    }
    response = handler(mock_event, None, mock_table)
    assert response['statusCode'] == 201

def test_invalid_user(mock_table):
    # send empty username to endpoint
    mock_table.put_item.return_value = {}
    mock_event = {
        'body': json.dumps({
            'username': " "
        })
    }
    response = handler(mock_event, None, mock_table)
    assert response['statusCode'] == 400
    assert json.loads(response['body'])['error'] == "Invalid request body."

def test_invalid_format(mock_table):
    # sends json in an invalid format to endpoint
    mock_table.put_item.return_value = {}
    mock_event = {
        'body': json.dumps({
            'first_name': "test"
        })
    }
    response = handler(mock_event, None, mock_table)
    assert response['statusCode'] == 400
    assert json.loads(response['body'])['error'] == "Invalid request body."