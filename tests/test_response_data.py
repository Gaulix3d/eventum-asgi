import pytest
from eventum_asgi.connection import WSConnection
from eventum_asgi.testclient import TestClient


async def handle_handshake(connection: WSConnection):
    await connection.accept()


@pytest.mark.asyncio
async def test_handshake_base_response():
    """
    Test the base response of the handshake.
    """
    client = TestClient()
    client.add_handshake_route(path='/', handler=handle_handshake)
    async with client as client:
        conn = await client.connect(url='ws://127.0.0.1:7777', path='/')
        assert conn.response_headers["Upgrade"] == "websocket"
        assert conn.response_headers["Connection"] == "Upgrade"
        assert len(conn.response_headers["Sec-WebSocket-Accept"]) == 28
        assert conn.response_headers["Sec-WebSocket-Extensions"] == "permessage-deflate"
