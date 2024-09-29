import asyncio
import traceback
import orjson
from eventum_asgi.connection import WSConnection
from eventum_asgi.event_router import EventRouter
from eventum_asgi.events.validation_error import EventValidationException
from eventum_asgi.exceptions import DisconnectedException
from eventum_asgi.exceptions.validation import ValidationException


class EventLoop:
    def __init__(self, router: EventRouter):
        self.router = router

    @staticmethod
    async def send_validation_exception_event(connection: WSConnection):
        """
        Send a validation exception event to the client.

        Parameters:
        - connection (WSConnection): The connection object to send the event to.
        """
        await connection.send_text(EventValidationException())

    async def handle_connection(self, connection: WSConnection):
        """
        Handle the WebSocket connection by receiving data and routing events.

        Parameters:
        - connection (WSConnection): The connection object to handle.
        """
        while True:
            await asyncio.sleep(0.1)
            try:
                data = await connection.receive_data()
                if data is not None:
                    data_json = orjson.loads(data)
                    await self.router.route_event(connection, data_json)
                  
            except orjson.JSONDecodeError:
                print('Not json')
            except ValidationException:
                await self.send_validation_exception_event(connection)
            except DisconnectedException:
                break  # Exit the loop if disconnected
            except Exception as e:
                traceback.print_exception(e)
                await connection.close()
                break  # Exit the loop in case of an error