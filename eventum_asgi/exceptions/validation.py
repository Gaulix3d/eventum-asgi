class ValidationException(Exception):
    """
    Exception raised when validation fails.
    """
    def __init__(self, message='Validation failed'):
        """
        Initialize the exception with the given message.
        """
        super().__init__(message)

