# Eventum ASGI

Eventum ASGI is a simple WebSocket ASGI framework for Python.

## Description

Eventum ASGI is a lightweight, easy-to-use ASGI framework specifically designed for handling WebSocket connections. It provides a straightforward way to create WebSocket servers with event-based routing and middleware support.

## Features

- WebSocket connection handling
- Event-based routing
- Middleware support
- Lifespan event management
- Pydantic model validation for events
- HTTP response support

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
    await connection.send_text("Hello, WebSocket!")

@app.event('message')
async def message_handler(connection: WSConnection, event: dict):
    await connection.send_text(f"You said: {message}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
## Documentation
For more detailed information on how to use Eventum ASGI, please refer to our documentation (coming soon).

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE.txt file for details.