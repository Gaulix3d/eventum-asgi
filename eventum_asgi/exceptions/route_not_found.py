from eventum_asgi.exceptions.http_exception import HttpException
from eventum_asgi.models.headers import Headers


class HttpNotFoundException(HttpException):
    """
    Exception raised when a route is not found.
    """
    def __init__(self, code: int = 404,
                 headers: Headers = Headers(),
                 body: bytes = b'Not Found'):
        """
        Initialize the exception with the given status code, headers, and body.
        """
        super().__init__(code, headers, body)
