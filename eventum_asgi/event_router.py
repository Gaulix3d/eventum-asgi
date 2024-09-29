import functools
import typing
import pydantic
from eventum_asgi.connection import WSConnection
from eventum_asgi.exceptions.validation import ValidationException
from eventum_asgi.types import EventRoutesDict, Handler


class EventRouter:
    def __init__(self):
        self.events: EventRoutesDict = {}

    async def route_event(self, connection: WSConnection, event_data: dict):
        """
        Route the event to the appropriate handler.

        Parameters:
        - connection (WSConnection): The connection object.
        - event_data (dict): The event data.
        """
        event = event_data.get('event')
        path = self.events.get(event)
        if path:
            validator: typing.Type[pydantic.BaseModel] = path.get('validator')
            if validator is not None:
                if not self.validate_model(validator, event_data):
                    raise ValidationException()
            handler = path['handler']
            await handler(connection, event_data)
        else:
            print('No event')

    def route(self,
              event: str,
              validator: typing.Optional[typing.Type[pydantic.BaseModel]] = None
              ) -> typing.Callable[[Handler], Handler]:
        """
    A decorator that registers a WebSocket event handler for the specified event.

    Parameters:
    -----------
    event : str
        The event type to be registered (e.g., "registered", "message_sent").

    Returns:
    --------
    Callable[[Handler], Handler]
        A decorator that wraps the provided handler function, registering it
        for the specified event.
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
            self.events[event] = {'handler': wrapped_handler, 'validator': validator}
            return wrapped_handler

        return decorator

    @staticmethod
    def validate_model(model: typing.Type[pydantic.BaseModel], data: dict):
        """
               Validates the provided data against the given Pydantic model.

               Parameters:
               - model (Type[BaseModel]): The Pydantic model class to validate against.
               - data (dict): The dictionary data to validate.

               Returns:
               - bool: True if validation is successful, False otherwise.
               """
        try:
            model(**data)
            return True
        except pydantic.ValidationError:
            return False

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

        async def wrapped_handler(connection: WSConnection,
                                  *args: typing.Any,
                                  **kwargs: typing.Any
                                  ) -> typing.Any:
            return await handler(connection, *args, **kwargs)

        # Register the event with the wrapped handler
        self.events[event] = {'handler': wrapped_handler, 'validator': validator}