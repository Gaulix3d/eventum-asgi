from typing import Callable, Any, Literal
from eventum_asgi.types import Scope, Receive, Send


class Lifespan:
    def __init__(self):
        """
        Initializes the Lifespan instance, setting on_startup and on_shutdown
        handlers to None.
        """
        self.on_startup = None
        self.on_shutdown = None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Manages the lifespan cycle by handling 'lifespan.startup' and 'lifespan.shutdown'
        events. This method is intended to be called with the scope, receive, and send
        arguments as per the ASGI specification.

        Args:
            scope (dict): The ASGI connection scope.
            receive (callable): An awaitable callable to receive messages.
            send (callable): An awaitable callable to send messages.

        Returns:
            None
        """
        assert scope['type'] == 'lifespan'
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                if self.on_startup:
                    await self.on_startup()
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                if self.on_shutdown:
                    await self.on_shutdown()
                await send({'type': 'lifespan.shutdown.complete'})
                return

    def on_event(self,
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
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            """
            Registers the given function as the handler for the specified event type.

            Args:
                func (callable): The function to register as an event handler.

            Returns:
                callable: The original function, unmodified.
            """
            if event_type == 'startup':
                self.on_startup = func
            elif event_type == 'shutdown':
                self.on_shutdown = func
            return func
        return decorator
    
