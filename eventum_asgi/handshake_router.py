import functools
import typing
from eventum_asgi.connection import WSConnection
from eventum_asgi.exceptions import RequiredHeadersMissingException, HttpNotFoundException
from eventum_asgi.types import HandshakeRoutesDict, Handler


class HandshakeRouter:
    def __init__(self):
        self.routes: HandshakeRoutesDict = {}

    async def __call__(self, connection: WSConnection) -> None:
        """
        Handle the WebSocket handshake request by validating headers and routing to the appropriate handler.

        Parameters:
        - connection (WSConnection): The connection object.
        """
        path = self.routes.get(connection.path)
        if path:
            required_headers: list = path['required_headers']
            if required_headers is not None:
                connection_headers = connection.request_headers.model_dump()
                print(connection_headers)
                print(required_headers)
                if not all(item in connection_headers for item in required_headers):
                    raise RequiredHeadersMissingException()
            handler = path['handler']
            await handler(connection)
        else:
            raise HttpNotFoundException()

    def route(self,
              path: str,
              required_headers: typing.List[str] = None,
              ) -> typing.Callable[[Handler], Handler]:
        """
        A decorator that registers a WebSocket route with the specified path.

        Parameters:
        -----------
        path : str
            The route path to be registered.

        Returns:
        --------
        Callable[[Handler], Handler]
            A decorator that wraps the provided handler function.
        """

        def decorator(func: Handler) -> Handler:
            @functools.wraps(func)
            async def wrapped_handler(connection: WSConnection,
                                      *args: typing.Any,
                                      **kwargs: typing.Any
                                      ) -> Handler:
                """
                A wrapped handler function that ensures the handler is called asynchronously
                and passes additional arguments to the handler.

                Parameters:
                -----------
                connection : WSConnection
                    The WebSocket connection object.
                args : Any
                    Positional arguments passed to the handler.
                kwargs : Any
                    Keyword arguments passed to the handler.

                Returns:
                --------
                Any
                    The result of the asynchronous handler function.
                """
                return await func(connection, *args, **kwargs)

            # Register the route with the wrapped handler
            self.routes[path] = {'handler': wrapped_handler, 
                                 "required_headers": list(map(lambda x: x.lower(), required_headers)) if required_headers else None
                                 }
            return wrapped_handler

        return decorator

    def add_route(self,
                  path: str,
                  handler: Handler,
                  required_headers: typing.List[str] = None,
                  ) -> None:
        """
        A method to register a WebSocket route by directly passing the handler.

        Parameters:
        -----------
        path : str
            The route path to be registered.
        handler : Handler
            The asynchronous handler function for the route.
        required_headers : typing.List[str], optional
            A list of required headers that must be present in the connection request.
        """

        async def wrapped_handler(connection: WSConnection,
                                  *args: typing.Any,
                                  **kwargs: typing.Any
                                  ) -> typing.Any:
            return await handler(connection, *args, **kwargs)

        # Register the route with the wrapped handler
        self.routes[path] = {'handler': wrapped_handler, "required_headers": required_headers}