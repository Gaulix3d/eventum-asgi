from eventum_asgi.models.headers import Headers


class HttpException(Exception):
    """
    Exception raised when an HTTP exception occurs.
    """
    def __init__(self, code: int, headers: Headers = Headers(), body: bytes = b''):
        """
        Initialize the exception with the given status code, headers, and body.
        """
        self.code = code
        self.headers = headers
        self.body = body
        super().__init__(f"HTTP exception occurred with status code: {self.code}, details: {self.body}")

    def get_details(self):
        return self.code, self.headers, self.body
