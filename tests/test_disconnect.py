import pytest
import orjson
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from eventum_asgi.app import Eventum
from eventum_asgi.events import Event
from eventum_asgi.connection import WSConnection
from eventum_asgi.testclient import TestClient


@pytest.mark.asyncio
async def test_disconnect_client():
    """
    Test the disconnect functionality.
    """
    app = Eventum()

    @app.handshake_route('/')
    async def index(connection: WSConnection):
        await connection.accept()

    @app.event('message')
    async def on_message(connection: WSConnection, event: Event):
        await connection.send_text('Hello, world!')

    client = TestClient(app)
    async with client:
        conn = await client.connect(path='/', url='ws://127.0.0.1:7777')
        assert conn.state == 1
        await conn.close()
        assert conn.state == 3

@pytest.mark.asyncio
async def test_disconnect_server():
    """
    Test the disconnect functionality.
    """
    app = Eventum()

    @app.handshake_route('/')
    async def index(connection: WSConnection):
        await connection.accept()

    @app.event('message')
    async def on_message(connection: WSConnection, event: Event):
        await connection.close(1000, 'Test disconnect')
    
    client = TestClient(app)
    async with client:
        conn = await client.connect(path='/', url='ws://127.0.0.1:7777')
        await conn.send(orjson.dumps({'event': 'message', 'data': 'Hello, world!'}))
        with pytest.raises(ConnectionClosedOK):
            await conn.recv()

@pytest.mark.asyncio            
async def test_disconnect_server_with_error():
    """
    Test the disconnect functionality.
    """
    app = Eventum()

    @app.handshake_route('/')
    async def index(connection: WSConnection):
        await connection.accept()

    @app.event('message')
    async def on_message(connection: WSConnection, event: Event):
        await connection.close(3000, 'Test disconnect')
    
    client = TestClient(app)
    async with client:
        conn = await client.connect(path='/', url='ws://127.0.0.1:7777')
        await conn.send(orjson.dumps({'event': 'message', 'data': 'Hello, world!'}))
        with pytest.raises(ConnectionClosedError):
            await conn.recv()
            

