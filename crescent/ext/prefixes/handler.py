from __future__ import annotations
import dataclasses
from typing import Any, Awaitable, Callable, Sequence, cast
import crescent
from crescent.internal import MetaStruct

import hikari

from .exceptions import CommandNotFoundError
from .typedefs import PrefixCommandProto
from .context import Context

HANDLER_MAP: dict[crescent.Bot, Handler] = {}


def set_prefix(bot: crescent.Bot, *prefixes: str) -> None:
    handle = Handler(prefixes, bot)
    HANDLER_MAP[bot] = handle
    bot.subscribe(hikari.MessageCreateEvent, handle.message_event)


@dataclasses.dataclass
class Handler:
    prefixes: Sequence[str]
    app: crescent.Bot
    registry: dict[str, Callable[[Context], Awaitable[None]]] = dataclasses.field(
        default_factory=dict
    )

    async def message_event(self, event: hikari.MessageCreateEvent) -> None:
        if not event.content:
            return
        cur_prefix: str
        for prefix in self.prefixes:
            if event.content.startswith(prefix):
                cur_prefix = prefix
                break
        else:
            return

        args = event.content[len(cur_prefix) :].split(" ")
        command_name = args[0]
        args = args[1:]

        command_class = self.registry.get(command_name)
        if not command_class:
            raise CommandNotFoundError(command_name)

        await command_class(
            Context(
                app=cast("crescent.Bot", event.app),
                _arguments=args,
                channel_id=event.channel_id,
                guild_id=event.guild_id
                if isinstance(event, hikari.GuildMessageCreateEvent)
                else None,
                user=event.author,
                member=event.member
                if isinstance(event, hikari.GuildMessageCreateEvent)
                else None,
            )
        )
