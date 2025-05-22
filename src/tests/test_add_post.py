from unittest.mock import MagicMock
import pytest


@pytest.fixture
def mock_table():
    # mock dynamodb table
    return MagicMock()

def test_handler_success():
    pass

def test_handler_fail():
    pass