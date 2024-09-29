import pytest
from eventum_asgi.app import Eventum
from eventum_asgi.connection import WSConnection
from eventum_asgi.testclient import TestClient


@pytest.mark.asyncio
async def test_handshake_route_registration():
    app = Eventum()

    @app.handshake_route('/')
    async def handler(connection: WSConnection):
        await connection.accept()

    client = TestClient(app)
    async with client:
        conn = await client.connect(url='ws://127.0.0.1:7777', path='/')
        assert conn.request_headers["Upgrade"] == "websocket"

@pytest.mark.asyncio
async def test_handshake_route_not_found():
    app = Eventum()
    client = TestClient(app)
    async with client:
        with pytest.raises(Exception):  # You might want to create a specific exception for this
            await client.connect(url='ws://127.0.0.1:7777', path='/nonexistent')

@pytest.mark.asyncio
async def test_handshake_with_required_headers():
    """
    Test the handshake route with required headers.
    """
    app = Eventum()

    @app.handshake_route('/', required_headers=['X-Custom-Header'])
    async def handler(connection: WSConnection):
        print(connection.request_headers)
        await connection.accept()

    client = TestClient(app)
    async with client:
        with pytest.raises(Exception):  # Should fail without required header
            await client.connect(url='ws://127.0.0.1:7777', path='/')

        conn = await client.connect(url='ws://127.0.0.1:7777', path='/', extra_headers={"X-Custom-Header": "Value"})
        assert conn.request_headers["X-Custom-Header"] == "Value"


