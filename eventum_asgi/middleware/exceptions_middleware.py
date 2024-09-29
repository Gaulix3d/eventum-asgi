from typing import Union, Any
from eventum_asgi.connection import WSConnection
from eventum_asgi.exceptions.http_exception import HttpException
from eventum_asgi.http_eventum import HttpResponse
from eventum_asgi.middleware import MiddlewareClass, CallNext


class ExceptionMiddleware(MiddlewareClass):
    def __init__(self,
                 call_next: Union[CallNext[WSConnection], MiddlewareClass[WSConnection]],
                 *args: Any,
                 **kwargs: Any
                 ) -> None:
        """
        Initialize the middleware with the given call next function.
        """         
        self.call_next = call_next

    async def __call__(self, connection: WSConnection) -> None:
        """
        Call the next middleware in the chain.
        """
        try:
            await self.call_next(connection)
        except HttpException as e:
            await self.handle_exc(exception=e,
                                  connection=connection
                                  )

    @staticmethod
    async def handle_exc(exception: HttpException,
                         connection: WSConnection):
        """
        Handle the exception by sending an HTTP response.
        """
        if isinstance(exception, HttpException):
            await connection.send_http_response(
                response=HttpResponse(
                    *exception.get_details()
                )
            )
