# --- imports
import sys
import discord
import traceback
from discord.ext import commands
from datetime import datetime

class Errors:
    # --- attributs

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot

    # --- @bot.event handling
    # on_command_error
    async def on_command_error(self, ctx, error):

        # TODO: improve error handling based on servers/roles/clients
        # Ignore errors from NGO
        if not isinstance(ctx.message.channel, discord.DMChannel):
            if ctx.guild.id == 225335295128633345:
                return


        # Logging error
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not isinstance(ctx.message.channel, discord.DMChannel):
            source = f"{ctx.guild.name}|{ctx.author}|{ctx.channel.name}"
        else:
            source = f"DirectMessage|{ctx.author}"
        await self.bot.get_channel(self.bot.log).send(
            f"""`❌` `⏱️ {timestamp}` [{source}] issued: `{ctx.message.content}`\n```Error: {error}```""")

        # prevent execution of custom on_error handler
        if hasattr(ctx.command, 'on_error'):
            return

        # Ignore-List procedure
        ignored = (commands.UserInputError)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return

        # DisabledCommand procedure
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"{ctx.command} has been disabled.")

        elif isinstance(error, commands.CommandNotFound):
            return await ctx.message.add_reaction('❓')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                return await ctx.send("I could not find that member. Please try again.")

        print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Errors(bot))
