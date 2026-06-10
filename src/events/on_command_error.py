from discord.ext import commands as cmds


def register(bot: cmds.Bot):
    @bot.event
    async def on_command_error(ctx, error):
        print(error)
