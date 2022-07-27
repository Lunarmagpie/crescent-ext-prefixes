from __future__ import annotations
from asyncio import gather

from functools import partial
from inspect import isclass
from typing import Any, Sequence, cast

from crescent import command
from crescent.internal import MetaStruct, AppCommandMeta
from crescent.internal.registry import _command_app_set_hook
from hikari import CommandOption

from .context import Context
from .typedefs import PrefixCommandProto
from .handler import set_prefix, HANDLER_MAP
from .serializer import serialize
from .args import star_args, StarArgs
from .exceptions import ParsingError


__all__: Sequence[str] = (
    "prefix_command",
    "Context",
    "set_prefix",
    "star_args",
)


def prefix_command(
    cls_or_meta: PrefixCommandProto | MetaStruct[Any, Any] | None = None,
    /,
    *,
    name: str | None = None,
) -> MetaStruct[Any, Any]:

    if cls_or_meta is None:
        return partial(
            prefix_command,
            name=name,
        )  # type: ignore

    cmd: MetaStruct[Any, Any]
    cls: PrefixCommandProto | None
    if isclass(cls_or_meta):
        cls = cast("PrefixCommandProto", cls_or_meta)
        cmd = command(name=name)(cls_or_meta)
        cmd.app_set_hooks = list(
            filter(lambda hook: hook is not _command_app_set_hook, cmd.app_set_hooks)
        )
    else:
        cmd = cls_or_meta  # type: ignore

    def _app_set_hook(self: MetaStruct[Any, Any]) -> None:
        print(cmd.metadata.app.name)
        HANDLER_MAP[self.app].registry[cmd.metadata.app.name] = partial(
            _prefix_command_callback, cls, cmd
        )

    cmd.app_set_hooks.append(_app_set_hook)

    return cmd


async def _prefix_command_callback(
    cls: type[PrefixCommandProto], cmd: MetaStruct[Any, AppCommandMeta], ctx: Context
) -> None:

    instance = cls()

    options: Sequence[CommandOption]
    if not cmd.metadata.app.options:
        options = []
    else:
        options = cmd.metadata.app.options

    remaining_args = ctx._arguments[len(options) :]

    for k, v in cls.__dict__.items():
        if v is StarArgs:
            setattr(instance, k, remaining_args)
            break
    else:
        if len(remaining_args) != 0:
            await instance.incorrect_argument_count(ctx, ctx._arguments)

    async def handle_arg(option: CommandOption, arg: str) -> Exception | None:
        try:
            arg = await serialize(ctx, option, arg)
        except Exception as e:
            return e
        setattr(instance, option.name, arg)
        return None

    args = await gather(
        *(handle_arg(option, arg) for option, arg in zip(options, ctx._arguments))
    )

    for option, value, (index, arg) in zip(options, ctx._arguments, enumerate(args)):
        if arg:
            await instance.parsing_error(ctx, arg, index, option.name, value)
            break
    else:
        await instance.callback(ctx)
