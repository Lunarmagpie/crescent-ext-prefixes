import dataclasses
import crescent
from typing import Any, Sequence
from hikari import (
    PartialRole,
    Snowflake,
    SnowflakeishSequence,
    User,
    Member,
    SnowflakeishOr,
    UndefinedOr,
    Resourceish,
    Embed,
    PartialMessage,
    UNDEFINED,
    SnowflakeishSequence,
    PartialUser,
    Message,
)
from hikari.api import ComponentBuilder


@dataclasses.dataclass
class Context:
    app: crescent.Bot

    channel_id: Snowflake
    guild_id: Snowflake | None
    user: User
    member: Member | None

    _arguments: list[str]

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
        mentions_reply: UndefinedOr[bool] = UNDEFINED,
        user_mentions: UndefinedOr[
            SnowflakeishSequence[PartialUser] | bool
        ] = UNDEFINED,
        role_mentions: UndefinedOr[
            SnowflakeishSequence[PartialRole] | bool
        ] = UNDEFINED,
    ) -> Message:
        return await self.app.rest.create_message(
            channel=self.channel_id,
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
            mentions_reply=mentions_reply,
            user_mentions=user_mentions,
            role_mentions=role_mentions,
        )
