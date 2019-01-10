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




    # --- @bot Cog handling
    # extention(): async
    @commands.group(hidden = True)
    @commands.is_owner()
    async def system(self, ctx):
        """manage the Bot System"""
        if ctx.invoked_subcommand is None:
            await ctx.send('no param...')


    @system.command(name='load', hidden=True)
    async def cog_load(self, ctx, *, cog: str):
        """load a Module."""
        self.bot.load_extension(cog)
        return await ctx.send(f"System Module '{cog}' got successfully loaded")


    @system.command(name='unload', hidden=True)
    async def cog_unload(self, ctx, *, cog: str):
        """unload a Module."""
        self.bot.unload_extension(cog)
        return await ctx.send(f"System Module '{cog}' got successfully unloaded")


    @system.command(name='reload', hidden=True)
    async def cog_reload(self, ctx, *, cog: str):
        """reload a Module."""
        self.bot.unload_extension(cog)
        self.bot.load_extension(cog)
        return await ctx.send(f"System Module '{cog}' got successfully reloaded")




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


    # Event: Command executed completely
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
