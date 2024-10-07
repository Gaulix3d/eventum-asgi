import pytest
from unittest.mock import AsyncMock, MagicMock
from eventum_asgi import WSConnection

@pytest.fixture
def mock_scope():
    return {
        'type': 'websocket',
        'headers': [(b'host', b'example.com')],
        'path': '/ws',
        'subprotocols': ['proto1', 'proto2'],
    }

@pytest.fixture
def mock_receive():
    return AsyncMock()

@pytest.fixture
def mock_send():
    return AsyncMock()

@pytest.mark.asyncio
async def test_connection_flags_add(mock_scope, mock_receive, mock_send):
    connection = WSConnection(scope=mock_scope, receive=mock_receive, send=mock_send)
    assert connection.get_flag('foo') is None
    connection.add_flag('foo', 'bar')
    assert connection.get_flag('foo') == 'bar'

@pytest.mark.asyncio
async def test_connection_flags_add_multiple(mock_scope, mock_receive, mock_send):
    connection = WSConnection(scope=mock_scope, receive=mock_receive, send=mock_send)
    connection.add_flags({'foo': 'bar', 'baz': 'qux'})
    assert connection.flags == {'foo': 'bar', 'baz': 'qux'}

@pytest.mark.asyncio
async def test_connection_flags_remove(mock_scope, mock_receive, mock_send):
    connection = WSConnection(scope=mock_scope, receive=mock_receive, send=mock_send)
    connection.add_flag('foo', 'bar')
    assert connection.get_flag('foo') == 'bar'
    connection.remove_flag('foo')
    assert connection.get_flag('foo') is None

@pytest.mark.asyncio
async def test_connection_flags_clear(mock_scope, mock_receive, mock_send):
    connection = WSConnection(scope=mock_scope, receive=mock_receive, send=mock_send)
    connection.add_flag('foo', 'bar')
    connection.add_flag('baz', 'qux')
    assert connection.get_flag('foo') == 'bar'
    assert connection.get_flag('baz') == 'qux'
    connection.clear_flags()
    assert connection.get_flag('foo') is None
    assert connection.get_flag('baz') is None

@pytest.mark.asyncio
async def test_connection_flags_remove_multiple(mock_scope, mock_receive, mock_send):
    connection = WSConnection(scope=mock_scope, receive=mock_receive, send=mock_send)
    connection.add_flags({'foo': 'bar', 'baz': 'qux'})
    assert connection.flags == {'foo': 'bar', 'baz': 'qux'}
    connection.remove_flags(['foo', 'baz'])
    assert connection.flags == {}

@pytest.mark.asyncio
async def test_connection_flags_get_copy(mock_scope, mock_receive, mock_send):
    connection = WSConnection(scope=mock_scope, receive=mock_receive, send=mock_send)
    connection.add_flags({'foo': 'bar', 'baz': 'qux'})
    copy = connection.get_all_flags()
    assert copy == {'foo': 'bar', 'baz': 'qux'}
    copy['ggg'] = 'hhh'
    assert connection.flags == {'foo': 'bar', 'baz': 'qux'}
    assert copy == {'foo': 'bar', 'baz': 'qux', 'ggg': 'hhh'}
    assert connection.flags != copy
