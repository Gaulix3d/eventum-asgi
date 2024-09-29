import pytest
import asyncio
from websockets.exceptions import InvalidStatusCode, InvalidHeader
from eventum_asgi import HttpResponse
from eventum_asgi.app import Eventum
from eventum_asgi.connection import WSConnection
from eventum_asgi.testclient import TestClient

@pytest.mark.asyncio
async def test_http_response_model_200():
    app = Eventum()

    @app.handshake_route('/')
    async def index(connection: WSConnection):
        response = HttpResponse(code=200, body='Hello, world!')
        await connection.send_http_response(response)

    client = TestClient(app)
    async with client:
        with pytest.raises(InvalidStatusCode) as e:
            conn = await client.connect(path='/', url='ws://127.0.0.1:7777')

@pytest.mark.asyncio
async def test_http_response_model_400():
    app = Eventum()

    @app.handshake_route('/')
    async def index(connection: WSConnection):
        response = HttpResponse(code=400, body='Hello, world!')
        await connection.send_http_response(response)

    client = TestClient(app)
    async with client:
        with pytest.raises(InvalidStatusCode) as e:
            conn = await client.connect(path='/', url='ws://127.0.0.1:7777')

@pytest.mark.asyncio
async def test_http_response_model_302():
    app = Eventum()

    @app.handshake_route('/')
    async def index(connection: WSConnection):
        response = HttpResponse(code=302, body='Hello, world!')
        await connection.send_http_response(response)

    client = TestClient(app)
    async with client:
        with pytest.raises(InvalidHeader) as e:
            conn = await client.connect(path='/', url='ws://127.0.0.1:7777')