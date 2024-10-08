# Eventum ASGI

Eventum ASGI is a simple WebSocket ASGI framework for Python.

## Description

Eventum ASGI is a lightweight, easy-to-use ASGI framework specifically designed for handling WebSocket connections. It provides a straightforward way to create WebSocket servers with event-based routing and middleware support.

## Features

- WebSocket connection handling
- Event-based routing
- Middleware support
- Lifespan event management
- Pydantic model validation for events and handhakes
- HTTP response support
- Connection flags management


## Installation

You can install Eventum ASGI using pip:

```bash
pip install eventum-asgi
```
## Quick Start


Here's a simple example of how to use Eventum ASGI:
```python
from eventum_asgi import Eventum, WSConnection, Event

app = Eventum()

@app.handshake_route('/')
async def websocket_handler(connection: WSConnection):
    await connection.accept()

@app.event('user_registered')
async def message_handler(connection: WSConnection, event: dict):
    await connection.send_text(f"You said: {message}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Handshake Routes
Handshake routes are used to handle WebSocket handshakes. They are defined using the `handshake_route` decorator and are responsible for accepting the WebSocket connection and sending the handshake response as well adding a connection to the loop where the application is waiting for events to be sent by the client.

```python
@app.handshake_route('/')
async def websocket_handler(connection: WSConnection):
    await connection.accept()
```

## Event Routes
Event routes are used to handle events sent by the client. They are defined using the `event` decorator and are responsible for handling the event and sending a response back to the client(optinal). All the events should be defined and send as JSON objects and contain an event name.

### JSON
```json
{
    "event": "user_registered",
    "data": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "password123"
    }
}
```

### Event decorator
```python
@app.event('user_registered')
async def message_handler(connection: WSConnection, event: dict):
    await connection.send_text(f"You said: {message}")
```

## Documentation
For more detailed information on how to use Eventum ASGI, please refer to our documentation (coming soon).

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE.txt file for details.