import typing
from eventum_asgi.models.headers import Headers


class HttpResponse:
    """
    Class representing an HTTP response.
    """
    def __init__(self, code: int,
                 headers: typing.Union[typing.Dict[str, str], Headers] = Headers(),
                 body: typing.Union[str, bytes] = b''
                 ) -> None:
        """
        Initialize the response with the given code, headers, and body.
        """
        self.code = code
        self.headers = self.headers_to_tuples(headers=headers)
        self.body = self.encode_body(body=body)

    @staticmethod
    def headers_to_tuples(headers) -> typing.List[typing.Tuple[bytes, typing.Any]]:
        """
        Convert the headers to a list of tuples.
        """
        if isinstance(headers, Headers):
            return headers.to_tuples()
        elif isinstance(headers, dict):
            return Headers(**headers).to_tuples()
        else:
            raise TypeError

    @staticmethod
    def encode_body(body) -> bytes:
        """
        Encode the body to bytes.
        """
        if isinstance(body, bytes):
            return body
        elif isinstance(body, str):
            return body.encode('utf-8')
        else:
            raise TypeError

    def get_response_data(self):
        """
        Get the response data as a tuple of code, headers, and body.
        """
        return self.code, self.headers, self.body
