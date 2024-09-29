async def http_bad_request(send):
    """
    Sends a 400 Bad Request response.

    This function is used to respond to HTTP requests when the framework
    does not support them. It sends a response with a 400 status code
    and a plain text message.

    Args:
        send (callable): An ASGI send function used to send the response.

    Returns:
        None
    """
    await send({
        "type": "http.response.start",
        "status": 400,
        "headers": [
            (b"content-type", b"text/plain"),
        ], 
    })
    await send({
        "type": "http.response.body",
        "body": b"Framework doesn't support http requests",
    })