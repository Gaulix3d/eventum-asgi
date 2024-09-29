import orjson


class Event:
    """
    Base event class for all events in the system.
    """
    def __init__(self, **kwargs):
        """
        Initialize the event with the given keyword arguments.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        """
        Convert the event to a JSON string.
        """
        return orjson.dumps(self.__dict__).decode('utf-8')
