from __future__ import annotations
from typing import cast

class StarArgsType:
    ...

StarArgs = StarArgsType()


def star_args() -> list[str]:
    return cast("list[str]", StarArgs)
