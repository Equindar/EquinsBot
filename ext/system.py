# --- imports
import discord
from discord.ext import commands
from datetime import datetime


class System:
    # --- attributs
    server = 509301003376525314

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot


    # quit(): async
    @commands.command(hidden = True)
    @commands.is_owner()
    async def quit(self, ctx):
        """Shutting down EquinsBot"""
        print("[System] EquinsBot shutting down")
        await self.bot.logout()


    @commands.command(hidden = True)
    @commands.guild_only()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

    # --- @bot.event handling
    # Event: Command got fired
    async def on_command(self, ctx):
        if not isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.message.delete()

    # Event: Bot joins a server (guild)
    async def on_guild_join(self, guild: discord.Guild):
        print("[System] EquinsBot joined %s [ID: %d]" % (guild.name, guild.id))

    # Event: User joins the server (guild)
    async def on_member_join(self, member: discord.Member):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await self.bot.get_channel(self.bot.log).send("`➕` `⏱️ %s` [%s|%s] joined the server." % (timestamp, member.guild.name, member.name))

    # Event: User leaves the server (guild)
    async def on_member_remove(self, member: discord.Member):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await self.bot.get_channel(self.bot.log).send("`➖` `⏱️ %s` [%s|%s] left the server." % (timestamp, member.guild.name, member.name))

    async def on_command_completion(self, ctx):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not isinstance(ctx.message.channel, discord.DMChannel):
            source = "%s|%s|%s" % (ctx.guild.name, ctx.author, ctx.channel.name)
        else:
            source = "DirectMessage|%s" % (ctx.author)
        await self.bot.get_channel(self.bot.log).send("`✔️` `⏱️ %s` [%s] issued: `%s`" % (timestamp, source, ctx.message.content))


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(System(bot))
