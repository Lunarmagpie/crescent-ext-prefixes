import dataclasses
from crescent.exceptions import CrescentException
from hikari import OptionType


class PrefixError(CrescentException):
    """Base error for all prefix errors"""


@dataclasses.dataclass
class SerializationError(PrefixError):
    """Argument could not be serialized"""

    value: str
    type: OptionType


class ParsingError(PrefixError):
    """Option could not be parsed."""


class RoleNotFoundError(PrefixError):
    """Role could not be found."""


class UserNotFoundError(PrefixError):
    """User could not be found."""


class ChannelNotFoundError(PrefixError):
    """Channel could not be found."""


class CommandNotFoundError(PrefixError):
    """The command was not found"""
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Command `{name}` was not registered.")
