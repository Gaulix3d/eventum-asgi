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

# This function defines a simple WebSocket connection handler to perform the handshake, later, the connection gets into a loop and waits for a client to send an event.
@app.handshake_route('/')
async def websocket_handler(connection: WSConnection):
    await connection.accept()

# This function defines a simple event handler to handle the event sent by the client. All the events should be in the form of a json object in order for event handlers to proccess them. In this case an event might look like this:
# {
#     "event": "user_registered",
#     "username": "user_1", 
#     "password": "password_1"
# }
@app.event('user_registered')
async def message_handler(connection: WSConnection, event: dict):
    await connection.send_text(f"You said: {message}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```