from typing import Protocol, TypeVar, Any, Union, Generic, Iterator
from eventum_asgi.connection import WSConnection

T = TypeVar('T', bound=WSConnection)


class CallNext(Protocol[T]):
    """
    Protocol for a callable type that takes a WSConnection and performs some action.

    Methods
    -------
    __call__(connection: T) -> None
        An asynchronous method to handle a connection.
    """

    async def __call__(self, connection: T) -> None:
        """
        Handle a WebSocket connection.

        Parameters
        ----------
        connection : T
            An instance of WSConnection or its subclass.
        """
        ...


class MiddlewareClass(Protocol[T]):
    """
    Protocol for middleware classes that handle WebSocket connections.

    Methods
    -------
    __init__(call_next: Union[CallNext[T], 'MiddlewareClass[T]'], *args: Any, **kwargs: Any) -> None
        Initializes the middleware with the next callable in the chain.

    __call__(connection: T) -> None
        An asynchronous method to process a WebSocket connection.
    """

    def __init__(self, call_next: Union[CallNext[T], 'MiddlewareClass[T]'], *args: Any, **kwargs: Any) -> None:
        """
        Initialize the middleware.

        Parameters
        ----------
        call_next : Union[CallNext[T], 'MiddlewareClass[T]']
            The next callable or middleware class in the chain.

        *args : Any
            Positional arguments to be passed to the middleware.

        **kwargs : Any
            Keyword arguments to be passed to the middleware.
        """
        ...

    async def __call__(self, connection: T) -> None:
        """
        Process a WebSocket connection.

        Parameters
        ----------
        connection : T
            An instance of WSConnection or its subclass.
        """
        ...


M = TypeVar('M', bound=MiddlewareClass)


class Middleware(Generic[M]):
    """
    A wrapper class for middleware components.

    Attributes
    ----------
    cls : type[MiddlewareClass[T]]
        The middleware class type.
    args : tuple
        Positional arguments to be passed to the middleware.
    kwargs : dict
        Keyword arguments to be passed to the middleware.

    Methods
    -------
    __init__(cls: type[_MiddlewareClass[T]], *args: Any, **kwargs: Any) -> None
        Initialize the middleware wrapper with a specific middleware class.

    __iter__() -> Iterator[Any]
        Return an iterator over the middleware class, args, and kwargs.

    __repr__() -> str
        Return a string representation of the middleware wrapper.
    """

    def __init__(
            self,
            cls: type[MiddlewareClass[T]],
            *args: Any,
            **kwargs: Any,
    ) -> None:
        """
        Initialize the Middleware instance.

        Parameters
        ----------
        cls : type[MiddlewareClass[T]]
            The middleware class type that implements `_MiddlewareClass`.

        *args : Any
            Positional arguments to be passed to the middleware class.

        **kwargs : Any
            Keyword arguments to be passed to the middleware class.
        """
        self.cls = cls
        self.args = args
        self.kwargs = kwargs

    def __iter__(self) -> Iterator[Any]:
        """
        Return an iterator over the middleware class, args, and kwargs.

        Returns
        -------
        Iterator[Any]
            An iterator that yields the middleware class, its positional arguments, and keyword arguments.
        """
        as_tuple = (self.cls, self.args, self.kwargs)
        return iter(as_tuple)

    def __repr__(self) -> str:
        """
        Return a string representation of the Middleware instance.

        Returns
        -------
        str
            A string that represents the middleware class and its initialization arguments.
        """
        class_name = self.__class__.__name__
        args_strings = [f"{value!r}" for value in self.args]
        option_strings = [f"{key}={value!r}" for key, value in self.kwargs.items()]
        args_repr = ", ".join([self.cls.__name__] + args_strings + option_strings)
        return f"{class_name}({args_repr})"
