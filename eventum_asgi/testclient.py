import typing
import pydantic
import uvicorn
import websockets
import asyncio
from eventum_asgi.app import Eventum
from eventum_asgi.types import Handler

class CustomServer(uvicorn.Server):
    def __init__(self, config):
        """
        Initialize the CustomServer with the given configuration.

        Parameters:
        - config (uvicorn.Config): The configuration for the server.
        """
        super().__init__(config)
        self._serve_task = None

    async def start(self):
        """
        Start the server asynchronously.
        """
        self._serve_task = asyncio.create_task(self.serve())

    async def stop(self):
        """
        Stop the server asynchronously.
        """
        self.should_exit = True
        if self._serve_task:
            await self._serve_task

class TestClient:
    def __init__(self, app: Eventum = Eventum()):
        """
        Initialize the TestClient with the given application.

        Parameters:
        - app (Eventum): The application to test.
        """
        self.app = app
        self.__server = None

    async def __aenter__(self):
        """
        Enter the context of the TestClient.
        """
        config = uvicorn.Config(app=self.app, host='127.0.0.1', port=7777, reload=False)
        self.__server = CustomServer(config)
        await self.__server.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Exit the context of the TestClient.
        """
        if self.__server:
            await self.__server.stop()
            self.__server = None
        

    def add_handshake_route(self,
                            path: str,
                            handler: Handler,
                            required_headers: typing.List[str] = None
                            ) -> None:
        """
        Add a handshake route to the application.

        Parameters:
        - path (str): The path for the handshake route.
        - handler (Handler): The handler for the handshake route.
        - required_headers (typing.List[str]): The list of required headers for the handshake route.
        """
        self.app.add_handshake_route(path=path,
                                     handler=handler,
                                     required_headers=required_headers
                                     )

    def add_event(self,
                  event: str,
                  handler: Handler,
                  validator: typing.Optional[typing.Type[pydantic.BaseModel]] = None
                  ) -> None:
        """
        Add an event to the application.

        Parameters:
        - event (str): The event name.
        - handler (Handler): The handler for the event.
        - validator (typing.Optional[typing.Type[pydantic.BaseModel]]): The validator for the event.
        """
        self.app.add_event(event=event,
                           handler=handler,
                           validator=validator)

    async def connect(self, url, path, extra_headers: typing.Dict[str, str] = None):
        """
        Connect to the WebSocket server.

        Parameters:
        - url (str): The URL of the WebSocket server.
        - path (str): The path to connect to.
        - extra_headers (typing.Dict[str, str]): Additional headers to send with the connection.
        """
        uri = f'{url}{path}'
        return await websockets.connect(uri, extra_headers=extra_headers)


