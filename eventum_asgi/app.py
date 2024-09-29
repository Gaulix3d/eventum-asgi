import typing
from typing import Callable, Any, Literal
import pydantic
from eventum_asgi.connection import WSConnection
from eventum_asgi.handshake_router import HandshakeRouter
from eventum_asgi.lifespan import Lifespan
from eventum_asgi.middleware_chain import HandshakeMiddlewareConstructor
from eventum_asgi.types import Scope, Receive, Send, Handler
from eventum_asgi.event_loop import EventLoop
from eventum_asgi.event_router import EventRouter
from eventum_asgi.http_eventum import http_bad_request


class Eventum:
    def __init__(self):
        """
        Initializes the Eventum application.

        This constructor sets up the necessary components for handling WebSocket connections and lifecycle events.
        It initializes the handshake router, middleware constructor, middleware stack, event router, event loop, and lifespan manager.
        """
        self.handshake = HandshakeRouter()
        self.middleware_constructor = HandshakeMiddlewareConstructor(router=self.handshake)
        self.middleware_stack: typing.Optional[typing.Callable[[WSConnection], typing.Any]] = None
        self.event_router = EventRouter()
        self.event_loop = EventLoop(router=self.event_router)
        self.lifespan = Lifespan()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Asynchronous callable method for handling incoming connections.

        This method is called when the ASGI server passes a new connection to the application.
        It handles both lifespan events and WebSocket connections.

        Parameters:
        -----------
        scope : Scope
            A dictionary containing metadata about the connection.
        receive : Receive
            An awaitable callable for receiving ASGI events.
        send : Send
            An awaitable callable for sending ASGI events.

        Returns:
        --------
        None

        Behavior:
        ---------
        - Adds the current application instance to the scope.
        - For lifespan events, it delegates to the lifespan handler.
        - For other events (assumed to be WebSocket connections):
          - Constructs the middleware stack if not already done.
          - Creates a WSConnection instance.
          - Applies the middleware stack to the connection.
          - Hands over the connection to the event loop for further processing.
        """
        scope["app"] = self
        if scope["type"] == "lifespan":
            await self.lifespan(scope, receive, send)
        elif scope["type"] == "http":
            await http_bad_request(send)
        else:
            if self.middleware_stack is None:
                self.construct_middleware()
            connection = WSConnection(scope=scope, receive=receive, send=send)
            await self.middleware_stack(connection)
            await self.event_loop.handle_connection(connection)
    def lifespan_event(self,
                       event_type: Literal['startup', 'shutdown']
                       ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        Decorator to register a function as a handler for a specified lifecycle event.

        Args:
            event_type (str): The type of event to handle. Expected values are
                              'startup' or 'shutdown'.

        Returns:
            Callable: A decorator that registers the given function as an event handler.
        """
        return self.lifespan.on_event(event_type)

    def handshake_route(self,
                        route: str,
                        required_headers: typing.List[str] = None
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
        return self.handshake.route(route, required_headers=required_headers)

    def add_handshake_route(self,
                            path: str,
                            handler: Handler,
                            required_headers: typing.List[str] = None
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
        self.handshake.add_route(path=path, handler=handler, required_headers=required_headers)

    def event(self,
              event: str,
              validator: typing.Optional[typing.Type[pydantic.BaseModel]] = None
              ) -> typing.Callable[[Handler], Handler]:
        """
        A method to register a WebSocket event handler by directly passing the event name and handler.

        Parameters:
        -----------
        event : str
            The event type to be registered (e.g., "registered", "message_sent").
        handler : Handler
            The asynchronous handler function for the event.
        """
        return self.event_router.route(event=event, validator=validator)

    def add_event(self,
                  event: str,
                  handler: Handler,
                  validator: typing.Optional[typing.Type[pydantic.BaseModel]] = None
                  ) -> None:
        """
        A method to register a WebSocket event handler by directly passing the event name and handler.

        Parameters:
        -----------
        event : str
            The event type to be registered (e.g., "registered", "message_sent").
        handler : Handler
            The asynchronous handler function for the event.
        validator : typing.Optional[typing.Type[pydantic.BaseModel]]
            A Pydantic model to validate the event data against.
        """
        self.event_router.add_event(event=event, handler=handler, validator=validator)

    def construct_middleware(self) -> None:
        self.middleware_stack = self.middleware_constructor.construct_middleware()
