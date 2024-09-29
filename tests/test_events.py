import pytest
import orjson
from eventum_asgi.events import Event
from eventum_asgi.app import Eventum
from eventum_asgi.connection import WSConnection
from eventum_asgi.testclient import TestClient

@pytest.mark.asyncio
async def test_basic_event():
    """
    Test the basic event functionality.
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
        await conn.send(orjson.dumps({'event': 'message', 'data': 'Hello, world!'}).decode('utf-8'))
        response = await conn.recv()
        assert response == 'Hello, world!'


