import traceback
from typing import Any, Union
from eventum_asgi.connection import WSConnection
from eventum_asgi.middleware import CallNext, MiddlewareClass


class ServerErrorMiddleware(MiddlewareClass):
    """
    Middleware to handle exceptions during WebSocket connection processing.

    If an exception is raised during the processing of the connection, this middleware catches
    the exception and prints the full traceback to the console.
    """

    def __init__(self, call_next: Union[CallNext[WSConnection], MiddlewareClass[WSConnection]],
                 *args: Any, **kwargs: Any):
        """
        Initialize the ServerErrorMiddleware.

        Parameters
        ----------
        call_next : Union[CallNext[WSConnection], MiddlewareClass[WSConnection]]
            The next callable or middleware class in the chain.

        *args : Any
            Additional positional arguments (unused).

        **kwargs : Any
            Additional keyword arguments (unused).
        """
        self.call_next = call_next
        # Note: No call to super().__init__() since MiddlewareClass is a protocol, not a concrete class.

    async def __call__(self, connection: WSConnection) -> None:
        """
        Process the WebSocket connection and handle any exceptions that occur.

        This method attempts to pass the connection to the next middleware in the chain.
        If an exception occurs, it catches the exception and prints the full traceback.

        Parameters
        ----------
        connection : WSConnection
            The WebSocket connection to be processed.
        """
        try:
            await self.call_next(connection)
        except Exception as e:
            # Print the full exception traceback to the console
            traceback.print_exception(type(e), e, e.__traceback__)
