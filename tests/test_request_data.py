import pytest
import base64
from eventum_asgi.connection import WSConnection
from eventum_asgi.testclient import TestClient


async def handle_handshake(connection: WSConnection):
    await connection.accept()



@pytest.mark.asyncio
async def test_handshake_base_headers():
    """
    Test the base headers of the handshake.
    """
    client = TestClient()
    client.add_handshake_route(path='/', handler=handle_handshake)
    websocket_headers = {
    "Host": "127.0.0.1:7777",
    "Upgrade": "websocket",
    "Connection": "Upgrade",
    "Sec-WebSocket-Version": "13" ,
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    "User-Agent": "Python/3.12 websockets/13.1"
    }
    async with client as client:
        conn = await client.connect(url='ws://127.0.0.1:7777', path='/')
        assert conn.request_headers["Host"] == websocket_headers["Host"]
        assert conn.request_headers["Upgrade"] == websocket_headers["Upgrade"]
        assert conn.request_headers["Connection"] == websocket_headers["Connection"]
        assert conn.request_headers["Sec-WebSocket-Version"] == websocket_headers["Sec-WebSocket-Version"]
        assert conn.request_headers["Sec-WebSocket-Extensions"] == websocket_headers["Sec-WebSocket-Extensions"]
        assert conn.request_headers["User-Agent"] == websocket_headers["User-Agent"]

@pytest.mark.asyncio
async def test_handshake_key_header():
    """
    Test the Sec-WebSocket-Key header of the handshake.
    """
    client = TestClient()
    client.add_handshake_route(path='/', handler=handle_handshake)
    async with client as client:
        conn = await client.connect(url='ws://127.0.0.1:7777', path='/')
        key = conn.request_headers["Sec-WebSocket-Key"]
        decoded_key = base64.b64decode(key)
        
        assert key is not None, "Sec-WebSocket-Key should not be None"
        assert len(decoded_key) == 16, f"Decoded key should be 16 bytes, got {len(decoded_key)}"
        assert len(key) == 24, f"Encoded key should be 24 characters, got {len(key)}"

@pytest.mark.asyncio
async def test_handshake_extra_headers():
    """
    Test the extra headers of the handshake.
    """
    client = TestClient()
    client.add_handshake_route(path='/', handler=handle_handshake)
    async with client as client:
        conn = await client.connect(url='ws://127.0.0.1:7777', path='/', extra_headers={"X-Test": "Test"})
        assert conn.request_headers["X-Test"] == "Test"


