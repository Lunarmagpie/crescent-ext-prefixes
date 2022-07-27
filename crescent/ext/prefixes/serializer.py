from typing import Any
from crescent import Bot
from hikari import (
    CommandOption,
    HikariError,
    OptionType,
    PartialChannel,
    Role,
    Snowflake,
    User,
)

from .context import Context
from .exceptions import (
    RoleNotFoundError,
    ChannelNotFoundError,
    ParsingError,
    UserNotFoundError,
)


async def serialize(ctx: Context, option: CommandOption, arg: str) -> Any:
    return await _option_serializer[OptionType(option.type)](ctx, arg)


async def _serialize_string(_: Context, option: str) -> str:
    return option


async def _serialize_float(_: Context, option: str) -> float:
    try:
        return float(option)
    except ValueError:
        raise ParsingError("Argument is not a float.")


async def _serialize_int(_: Context, option: str) -> int:
    try:
        return int(option)
    except ValueError:
        raise ParsingError("Argument is not an int.")


async def _serialize_bool(_: Context, option: str) -> bool:
    true_types = ["yes", "true"]
    false_types = ["no", "false"]
    if option.lower() in true_types or option.lower() in false_types:
        return option.lower() in true_types
    else:
        raise ParsingError("Argument is not a valid true type or false type.")


async def _serialize_user(ctx: Context, option: str) -> User:
    try:
        user_id = Snowflake(option if option.isdigit() else option[2:-1])
        user = ctx.app.cache.get_user(user_id)
        if not user:
            user = await ctx.app.rest.fetch_user(user_id)
        return user
    except Exception:
        raise UserNotFoundError(f"User could not be found.")


async def _serialize_role(ctx: Context, option: str) -> Role:
    try:
        role_id = Snowflake(option if option.isdigit() else option[3:-1])
        role = ctx.app.cache.get_role(role_id)
        if role:
            return role
        if ctx.guild_id:
            for guild_role in await ctx.app.rest.fetch_roles(ctx.guild_id):
                if guild_role.id == role_id:
                    return guild_role
    except Exception:
        pass
    raise RoleNotFoundError(f"Role could not be found.")


async def _serialize_channel(ctx: Context, option: str) -> PartialChannel:
    try:
        channel_id = Snowflake(option if option.isdigit() else option[2:-1])
        channel: PartialChannel | None = ctx.app.cache.get_guild_channel(channel_id)
        if not channel:
            channel = await ctx.app.rest.fetch_channel(channel_id)
        return channel
    except Exception:
        raise ChannelNotFoundError(f"Channel could not be found.")


_option_serializer = {
    OptionType.STRING: _serialize_string,
    OptionType.FLOAT: _serialize_float,
    OptionType.INTEGER: _serialize_int,
    OptionType.BOOLEAN: _serialize_bool,
    OptionType.USER: _serialize_user,
    OptionType.ROLE: _serialize_role,
    OptionType.CHANNEL: _serialize_channel,
}
