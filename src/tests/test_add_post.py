import json
from unittest.mock import MagicMock
import pytest
from ..handlers.add_post import handler


@pytest.fixture
def mock_table():
    # mock dynamodb table
    return MagicMock()


def test_handler_success(mock_table):
    mock_event = {'body': {
        'message': 'test message',
        'sender': 'test user'
    }}
    mock_table.put_item.return_value = {}  # simulates successful insert into dynamodb
    res = handler(mock_event, context={})

    body = json.loads(res['body'])
    assert body['response'] == 200