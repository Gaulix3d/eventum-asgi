class DisconnectedException(Exception):
    """
    Exception raised when a connection is disconnected.
    """
    def __init__(self, connection_id):
        """
        Initialize the exception with the given connection ID.
        """
        self.connection_id = connection_id
        super().__init__(f'Connection with id: {self.connection_id} got disconnected')
