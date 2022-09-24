import dataclasses
from typing import Sequence
import crescent
from typing import Any
from hikari.api import ComponentBuilder
from hikari import (
    Member,
    Snowflake,
    UndefinedOr,
    Resourceish,
    UNDEFINED,
    Embed,
    PartialMessage,
    SnowflakeishOr,
    SnowflakeishSequence,
    PartialUser,
    PartialRole,
    Message,
    User,
)
from .context import Context as p_Context


__all__: Sequence[str] = (
    "CombinedContext",
    "CombinedCommand",
)


@dataclasses.dataclass
class CombinedContext:
    channel_id: Snowflake
    guild_id: Snowflake | None

    user: User
    member: Member | None

    _app_context: crescent.Context | None = None
    _prefix_context: p_Context | None = None

    async def respond(
        self,
        content: UndefinedOr[Any] = UNDEFINED,
        *,
        attachment: UndefinedOr[Resourceish] = UNDEFINED,
        attachments: UndefinedOr[Sequence[Resourceish]] = UNDEFINED,
        component: UndefinedOr[ComponentBuilder] = UNDEFINED,
        components: UndefinedOr[Sequence[ComponentBuilder]] = UNDEFINED,
        embed: UndefinedOr[Embed] = UNDEFINED,
        embeds: UndefinedOr[Sequence[Embed]] = UNDEFINED,
        tts: UndefinedOr[bool] = UNDEFINED,
        reply: UndefinedOr[SnowflakeishOr[PartialMessage]] = UNDEFINED,
        mentions_everyone: UndefinedOr[bool] = UNDEFINED,
        user_mentions: UndefinedOr[
            SnowflakeishSequence[PartialUser] | bool
        ] = UNDEFINED,
        role_mentions: UndefinedOr[
            SnowflakeishSequence[PartialRole] | bool
        ] = UNDEFINED,
    ) -> Message:
        if self._prefix_context:
            return await self._prefix_context.respond(
                content=content,
                attachment=attachment,
                attachments=attachments,
                component=component,
                components=components,
                embed=embed,
                embeds=embeds,
                tts=tts,
                reply=reply,
                mentions_everyone=mentions_everyone,
                user_mentions=user_mentions,
                role_mentions=role_mentions,
            )
        elif self._app_context:
            return await self._app_context.respond(
                content,
                ensure_message=True,
                attachment=attachment,
                attachments=attachments,
                component=component,
                components=components,
                embed=embed,
                embeds=embeds,
                tts=tts,
                mentions_everyone=mentions_everyone,
                user_mentions=user_mentions,
                role_mentions=role_mentions,
            )
        raise NotImplementedError("Must be a prefix command or slash command")

    async def defer(self) -> None:
        if self._app_context:
            await self._app_context.defer()


class CombinedCommand:
    async def prefix_callback(self, ctx: p_Context) -> None:
        await self.combined_callback(
            CombinedContext(
                channel_id=ctx.channel_id,
                guild_id=ctx.guild_id,
                user=ctx.user,
                member=ctx.member,
                _prefix_context=ctx,
            )
        )

    async def callback(self, ctx: crescent.Context) -> None:
        await self.combined_callback(
            CombinedContext(
                channel_id=ctx.channel_id,
                guild_id=ctx.guild_id,
                user=ctx.user,
                member=ctx.member,
                _app_context=ctx,
            )
        )

    async def combined_callback(self, ctx: CombinedContext) -> None:
        ...
