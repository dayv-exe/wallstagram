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
        'sender': 'test user'
    })}

    res = handler(event=mock_event, context={}, table=mock_table)
    assert res['statusCode'] == 201

    message = json.loads(res['body'])
