import typing
from eventum_asgi.connection import WSConnection
from eventum_asgi.handshake_router import HandshakeRouter
from eventum_asgi.middleware import MiddlewareClass, Middleware
from eventum_asgi.middleware.exceptions_middleware import ExceptionMiddleware
from eventum_asgi.middleware.server_error_middleware import ServerErrorMiddleware


class HandshakeMiddlewareConstructor:
    """
    A class to manage and construct a chain of middleware for WebSocket connection handling.

    Attributes
    ----------
    router : HandshakeRouter
        The final callable or router that handles the WebSocket connection after all middleware.

    Methods
    -------
    add_user_middleware(middleware: _MiddlewareClass) -> None
        Adds a user-defined middleware to the middleware chain.

    construct_middleware() -> typing.Callable[[WSConnection], typing.Any]
        Constructs and returns the complete middleware chain.
    """

    def __init__(self, router: HandshakeRouter) -> None:
        """
        Initialize the HandshakeMiddlewareConstructor with a router.

        Parameters
        ----------
        router : HandshakeRouter
            The final callable that processes the WebSocket connection.
        """
        self.__user_middlewares: typing.List[MiddlewareClass] = []
        self.router: HandshakeRouter = router

    def add_user_middleware(self, middleware: MiddlewareClass) -> None:
        """
        Add a user-defined middleware to the middleware chain.

        Parameters
        ----------
        middleware : _MiddlewareClass
            An instance of a class that implements the `_MiddlewareClass` protocol.
        """
        self.__user_middlewares.append(middleware)

    def construct_middleware(self) -> typing.Callable[[WSConnection], typing.Any]:
        """
        Construct and return the complete middleware chain.

        The middleware chain includes the `ServerErrorMiddleware` as the first middleware,
        followed by any user-defined middlewares, and ending with the router.

        Returns
        -------
        typing.Callable[[WSConnection], typing.Any]
            A callable representing the constructed middleware chain, which takes a `WSConnection`
            instance and returns any result that the router might produce.
        """
        middleware = (
                [Middleware(ServerErrorMiddleware)]
                + self.__user_middlewares
                + [Middleware(ExceptionMiddleware)]
        )

        call_next = self.router
        for cls, args, kwargs in reversed(middleware):
            call_next = cls(call_next=call_next, *args, **kwargs)

        return call_next
