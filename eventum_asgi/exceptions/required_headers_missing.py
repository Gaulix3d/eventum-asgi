from eventum_asgi.exceptions.http_exception import HttpException
from eventum_asgi.models.headers import Headers


class RequiredHeadersMissingException(HttpException):
    """
    Exception raised when required headers are missing.
    """
    def __init__(self, code: int = 400,
                 headers: Headers = Headers(),
                 body: bytes = b'Missing required headers'):
        """
        Initialize the exception with the given status code, headers, and body.
        """
        super().__init__(code, headers, body)
