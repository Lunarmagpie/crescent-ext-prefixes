from __future__ import annotations

from typing import Protocol
from .context import Context
from .exceptions import ParsingError


class PrefixCommandProto(Protocol):
    async def prefix_callback(self, ctx: Context) -> None:
        ...

    async def incorrect_argument_count(self, ctx: Context, args: list[str]) -> None:
        ...

    async def parsing_error(
        self,
        ctx: Context,
        exc: ParsingError,
        location: int,
        name: str,
        value: str,
    ) -> None:
        ...

    @property
    def __name__(self) -> str:
        ...
