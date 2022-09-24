# Crescent-ext-prefixes

An experimental prefix command handler for [hikari crescent](https://github.com/magpie-dev/hikari-crescent).


```python
import crescent
from crescent.ext import prefixes


bot = crescent.Bot("...")

# Prefixes are *args
prefixes.set_prefix(bot, "!", "$")

# Create a prefix command with a user option
@bot.include
@prefixes.prefix_command
class PrefixCommand:
    user = crescent.option(User)

    async def prefix_callback(self, ctx: prefixes.CombinedContext) -> None:
        await ctx.respond(self.user.username)


    # If you want to re-use these methods it is recommended to make
    # a subclass all your commands inherit from.
    async def incorrect_argument_count(
        self, ctx: prefixes.Context, args: list[str]
    ) -> None:
        await ctx.respond(f"Expected one argument, got {len(args)}.")

    async def parsing_error(
        self,
        ctx: prefixes.Context,
        exc: prefixes.exceptions.ParsingError,
        location: int,
        name: str,
        value: str,
    ) -> None:
        await ctx.respond(
            f"Argument `{location}` with name `{name}` could not be parsed."
        )
```

You can also make a combined prefix/slash command.

```python
@bot.include
# The `prefixes.prefix_command` decorator must be above the
# `crescent.commands` decorator.
@prefixes.prefix_command
@crescent.command
class PrefixCommand(prefixes.CombinedContext):
    user = crescent.option(User)

    async def combined_callback(self, ctx: prefixes.CombinedContext) -> None:
        await ctx.respond(self.user.username)

    ...
```
