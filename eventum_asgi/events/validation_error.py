from eventum_asgi.events.base_event import Event


class EventValidationException(Event):
    def __init__(self,
                 event: str = 'validation_error',
                 message: str = 'Invalid data received',
                 **kwargs):
        """
        Initialize the event with the given keyword arguments.
        """
        self.event = event
        self.message = message
        super().__init__(**kwargs)
