from __future__ import annotations
import dataclasses
from typing import Any

from crescent.internal import Includable

from .typedefs import PrefixCommandProto


@dataclasses.dataclass(unsafe_hash=True)
class CommandID:
    name: str


class PrefixReg:
    registry: dict[CommandID, Includable[PrefixCommandProto]] = {}
