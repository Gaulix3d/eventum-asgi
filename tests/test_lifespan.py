import pytest
from eventum_asgi.app import Eventum
from eventum_asgi.testclient import TestClient
from eventum_asgi.connection import WSConnection

@pytest.mark.asyncio
async def test_lifespan_events():
    """
    Test the lifespan events.
    """
    app = Eventum()
    startup_called = False
    shutdown_called = False

    @app.lifespan_event('startup')
    async def on_startup():
        print('startup')
        nonlocal startup_called
        startup_called = True

    @app.lifespan_event('shutdown')
    async def on_shutdown():
        print('shutdown')
        nonlocal shutdown_called
        shutdown_called = True

    @app.handshake_route('/')
    async def index(connection: WSConnection):
        print('handler speaks')
        await connection.accept()

    client = TestClient(app)
    async with client:
        await client.connect(path='/', url='ws://127.0.0.1:7777')
        assert startup_called
    assert shutdown_called
