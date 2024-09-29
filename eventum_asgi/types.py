import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from eventum_asgi.connection import WSConnection

# Basic Types:
Scope = typing.MutableMapping[str, typing.Any]
"""
Type alias for the scope of a connection.

Scope represents the scope of a connection in ASGI (Asynchronous Server Gateway Interface) applications. It is a mutable mapping (dictionary-like object) where the keys are strings, and the values can be of any type.

Examples of scope information include the type of connection (HTTP, WebSocket), HTTP headers, path, query string parameters, etc.

Example:
    scope: Scope = {
        "type": "http_eventum",
        "headers": [(b"host", b"example.com")]
    }
"""

Message = typing.MutableMapping[str, typing.Any]
"""
Type alias for a message in an ASGI application.

Message represents a message sent or received in an ASGI application. It is a mutable mapping (dictionary-like object) where the keys are strings, and the values can be of any type.

Messages can include HTTP requests and responses, WebSocket events, etc.

Example:
    message: Message = {
        "type": "http_eventum.request",
        "body": b"Hello, world!"
    }
"""

Receive = typing.Callable[[], typing.Awaitable[Message]]
"""
Type alias for the receive callable in an ASGI application.

Receive is a callable (function) that takes no arguments and returns an awaitable which resolves to a Message. It is used to receive messages from the client in an asynchronous manner.

Example:
    async def receive() -> Message:
        return await some_receive_function()

    receive: Receive = receive
"""

Send = typing.Callable[[Message], typing.Awaitable[None]]
"""
Type alias for the send callable in an ASGI application.

Send is a callable (function) that takes a Message as an argument and returns an awaitable that resolves to None. It is used to send messages to the client in an asynchronous manner.

Example:
    async def send(message: Message) -> None:
        await some_send_function(message)

    send: Send = send
"""

# HandshakeRouter Routing types:

Handler = typing.Callable[['WSConnection', typing.Any], typing.Awaitable[typing.Any]]
"""
Handler represents an asynchronous callable that takes a `WSConnection` object 
and an optional second argument of any type (`Optional[Any]`). It returns an 
awaitable result (typically a coroutine).

This type is used for handling WebSocket connections in an asynchronous manner, 
where the handler may optionally process additional data or context passed 
alongside the `WSConnection`.
"""

# Define the HandshakeRoutesDict type alias
HandshakeRoutesDict = typing.MutableMapping[str, typing.Dict[str, typing.Union[Handler, typing.Any]]]
"""
WebSocket handshake routes dictionary.

This structure is used to map WebSocket routes to their corresponding handlers and
related metadata or configuration.

- **Keys (str)**: The keys of the outer dictionary represent paths (routes).
- **Values (Dict[str, Union[Handler, Any]])**: The values are dictionaries that
  contain:
  - **Handler**: An asynchronous function that takes a `WSConnection` object as 
    an argument. This function handles the WebSocket connection.
  - **Any**: Other optional metadata or configuration arguments that may be passed
    to the handler, such as additional arguments (`args`) or keyword arguments (`kwargs`).

# Example handshake routes dictionary
routes: HandshakeRoutesDict = {
    "/chat": {
        "handler": chat_handler,
        "description": "Handles incoming connections to the chat route",
        "active": True
    },
    "/notifications": {
        "handler": lambda ws: ws.send("Notifications are enabled"),
        "args": ["arg1", "arg2"],
        "kwargs": {"key": "value"}
    }
}
"""
EventRoutesDict = typing.MutableMapping[str, typing.Dict[str, typing.Union[Handler, typing.Any]]]
"""
WebSocket event routes dictionary.

This structure is used to map specific WebSocket event types or messages 
to their corresponding handlers and related metadata or configuration. 
It allows for dynamic routing and handling of various WebSocket events within the connection lifecycle.

- **Keys (str)**: The keys of the outer dictionary represent specific event types, message types,
 or even specific commands that are expected from the WebSocket client.
- **Values (Dict[str, Union[Handler, Any]])**: The values are dictionaries that contain:
  - **Handler**: An asynchronous function that takes a `WSConnection` object as an argument.
   This function handles the WebSocket event or message. 
   The handler can perform tasks such as sending responses,
    processing messages, or performing actions based on the event.
  - **Any**: Other optional metadata or configuration arguments that may be passed to the handler, 
  such as additional arguments (`args`), keyword arguments (`kwargs`), 
  or specific event-related configuration.

"""