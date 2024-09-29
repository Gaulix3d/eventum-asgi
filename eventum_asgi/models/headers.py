import pydantic
import typing


class Headers(pydantic.BaseModel):
    """
    Class representing HTTP headers.
    """

    model_config = pydantic.ConfigDict(extra='allow')

    def to_tuples(self) -> typing.List[typing.Tuple[bytes, typing.Any]]:
        """
        Convert the headers to a list of tuples.
        """
        tuple_list = []
        for key, value in iter(self):
            tuple_list.append((key.encode(), value.encode()))
        return tuple_list




