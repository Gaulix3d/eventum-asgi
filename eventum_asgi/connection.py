import uuid
from typing import Optional, Union, Dict, Callable, List, Any
from eventum_asgi.events.base_event import Event
from eventum_asgi.models.headers import Headers
from eventum_asgi.types import Scope, Receive, Send
from eventum_asgi.exceptions import DisconnectedException
from eventum_asgi.http_eventum import HttpResponse


class WSConnection:
    def __init__(self, scope: Scope, receive: Receive, send: Send):
        """
        Initializes a WSConnection instance.

        Parameters:
        - scope (Scope): The connection scope containing metadata about the WebSocket connection.
          This includes details like headers, path, and subprotocols.
        - receive (Receive): An awaitable callable to receive messages from the WebSocket connection.
        - send (Send): An awaitable callable to send messages to the WebSocket connection.

        The `__init__` method sets up the initial state of the WSConnection instance, storing the
        provided scope, receive, and send callables. It also initializes internal attributes for
        request headers, subprotocols, and path based on the scope.
        """
        self.id = uuid.uuid4()
        self.scope = scope
        self.receive = receive
        self.__flags = {}
        self.send = send
        self.__request_headers: Optional[Headers] = self.__create_request_headers_model()
        self.__subprotocols: list = self.scope.get('subprotocols')
        self.__path: str = self.scope.get('path')

    async def accept(self,
                     extra_headers: Optional[Union[Dict[str, str], Headers]] = None,
                     subprotocol_factory: Callable[[List[str]], str] = lambda subprotocols: subprotocols[0]
                     ) -> None:
        """
        Accepts the WebSocket connection.

        Parameters:
        - extra_headers (Optional[Union[Dict[str, str], Headers]]): Additional headers to include in the response.
        - subprotocol_factory (Callable[[List[str]], str]): A factory function to choose a subprotocol from
         the list of subprotocols offered by the client. Defaults to choosing the first subprotocol.

        This method sends a `websocket.accept` message to the client,
        indicating that the server accepts the WebSocket connection.
        """
        if extra_headers is None:
            extra_headers = Headers()
        elif isinstance(extra_headers, dict):
            extra_headers = Headers(**extra_headers)

        extra_headers_tuples_list = extra_headers.to_tuples()

        if self.subprotocols:
            subprotocol = subprotocol_factory(self.subprotocols)
            extra_headers_tuples_list.append((
                'Sec-WebSocket-Protocol'.encode(),
                subprotocol.encode()
            ))

        response_dict = {
            "type": "websocket.accept",
            "headers": extra_headers_tuples_list
        }
        await self.send(response_dict)

    async def send_text(self, message: Union[str, Event]) -> None:
        """
        Sends a text message to the client.

        Parameters:
        - message (str): The text message to send.

        This method sends a `websocket.send` message with the text data to the client.
        """
        if isinstance(message, Event):
            message = message.to_json()

        await self.send({
            "type": "websocket.send",
            "text": message
        })
    
    async def send_bytes(self, message: bytes) -> None:
        """
        Sends a binary message to the client.

        Parameters:
        - message (bytes): The binary data to send.

        This method sends a `websocket.send` message with the binary data to the client.
        """
        await self.send({
            "type": "websocket.send",
            "bytes": message
        })

    async def receive_data(self) -> Optional[Union[str, bytes]]:
        """
        Receives a message from the client.

        Returns:
        - Optional[Union[str, bytes]]: The received message, or None if the connection is closed.

        This method waits for a `websocket.receive` message from the client and returns the message data.
        """
        event = await self.receive()
        if event['type'] == 'websocket.receive':
            if event.get('text'):
                return event['text']
            elif event.get('bytes'):
                return event['bytes']
        elif event['type'] == 'websocket.disconnect':
            raise DisconnectedException(connection_id=self.id)

    async def receive_bytes(self) -> Optional[bytes]:
        """
        Receives a binary message from the client.

        Returns:
        - Optional[bytes]: The received binary message, or None if the connection is closed.

        This method waits for a `websocket.receive` message from the client and returns the binary data.
        """
        event = await self.receive()
        if event['type'] == 'websocket.receive':
            return event['bytes']
        elif event['type'] == 'websocket.disconnect':
            raise DisconnectedException(connection_id=self.id)

    async def receive_text(self) -> Optional[str]:
        """
        Receives a text message from the client.

        Returns:
        - Optional[str]: The received text message, or None if the connection is closed.

        This method waits for a `websocket.receive` message from the client and returns the text data.
        """
        event = await self.receive()
        if event['type'] == 'websocket.receive':
            return event['text']
        elif event['type'] == 'websocket.disconnect':
            raise DisconnectedException(connection_id=self.id)

    async def close(self, code: int = 1000, reason: str = "") -> None:
        """
        Closes the WebSocket connection.

        Parameters:
        - code (int): The WebSocket close code. Default is 1000 (normal closure).
        - reason (str): The reason for closing the connection. Default is an empty string.

        This method sends a `websocket.close` message to the client,
        indicating that the server is closing the WebSocket connection.
        """
        await self.send({
            "type": "websocket.close",
            "code": code,
            "reason": reason
        })

    def __create_request_headers_model(self):
        """
        Creates a Headers model from the request headers in the scope.

        This private method extracts headers from the scope, decodes them from bytes to strings,
        and constructs a `Headers` model instance with these headers.

        Returns:
            Headers: A Headers object populated with the request headers.

        Example:
            Given the scope headers:
                [(b'Content-Type', b'application/json'), (b'Authorization', b'Bearer token')]

            The resulting Headers object will be:
                Headers(Content-Type='application/json', Authorization='Bearer token')
        """
        request_headers_dict = {key.decode(): value.decode() for key, value in self.scope['headers']}
        return Headers(**request_headers_dict)

    def get_flag(self, name: Any) -> Any:
        """
        Get the value of a flag by name.

        Parameters:
        - name (Any): The name of the flag to retrieve.

        Returns:
        - Any: The value of the flag, or None if the flag is not set.
        """
        return self.__flags.get(name)
    
    def get_all_flags(self) -> Dict[Any, Any]:
        """
        Get all flags.
        
        Returns:
        - Dict[Any, Any]: A dictionary of all flags as a copy.
        """
        return self.__flags.copy()

    def add_flag(self, name: Any, value: Any) -> None:
        """
        Add a flag with the specified name and value.

        Parameters:
        - name (Any): The name of the flag.
        - value (Any): The value of the flag.
        """
        self.__flags[name] = value

    def add_flags(self, flags: Dict[Any, Any]) -> None:
        """
        Add multiple flags from a dictionary.

        Parameters:
        - flags (Dict[Any, Any]): A dictionary of flags to add.
        """
        self.__flags.update(flags)

    def remove_flag(self, name: Any) -> None:
        """
        Remove a flag by name.

        Parameters:
        - name (Any): The name of the flag to remove.
        """
        self.__flags.pop(name)
    
    def remove_flags(self, names: List[str]) -> None:
        for name in names:
            self.__flags.pop(name, None)

    def clear_flags(self) -> None:
        """
        Remove all flags.
        """
        self.__flags = {}

    async def send_http_response(self, response: HttpResponse):
        """
        Send an HTTP response to the client.

        Parameters:
        - response (HttpResponse): The HTTP response to send.
        """
        code, headers, body = response.get_response_data()
        await self.send({
            "type": "websocket.http.response.start",
            "status": code,
            "headers": headers,
        })
        await self.send({
            "type": "websocket.http.response.body",
            "body": body,
        })

    @property
    def request_headers(self) -> Headers:
        """
        Returns the request headers.

        Returns:
        - Headers: The request headers.
        """
        return self.__request_headers

    @property
    def path(self) -> str:
        """
        Returns the path from the scope.

        Returns:
        - str: The request path.
        """
        return self.__path

    @property
    def subprotocols(self) -> List[str]:
        """
        Returns the subprotocols from the scope.

        Returns:
        - List[str]: The list of subprotocols offered by the client.
        """
        return self.__subprotocols

    @property
    def flags(self) -> Dict[Any, Any]:
        """
        Get the flags dictionary.

        Returns:
        - Dict[Any, Any]: The flags dictionary.
        """
        return self.__flags
