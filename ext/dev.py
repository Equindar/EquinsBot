# --- imports
import discord
import asyncio
from discord.ext import commands
from datetime import datetime


class DEV:
    # --- attributs
    server = {
        "Equindar": 509301003376525314,
        "NorthgardBattle": 486105985782644736
    }

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot


    # info(): async
    @commands.group(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def info(self, ctx):
        """display information"""
        if ctx.invoked_subcommand is None:
            await ctx.send("No param...")


    # server_info(): async
    @info.command(name="server", hidden=True)
    async def server_info(self, ctx):
        """display server information"""
        s = ctx.guild
        data = ""
        value = ""
        dict = {
            'Name': s.name,
            'ID': s.id,
            'Owner': f"{s.owner.name} [ID: {s.owner.id}]"
        }

        for k,v in dict.items():
            data += f"{k}\n"
            value += f"{v}\n"
        embed = discord.Embed(title=f"__{s.name}__",colour=3158584)
        embed.set_footer(text="--- Server information ---")
        embed.add_field(name="Data", value=data, inline=True)
        embed.add_field(name="Value", value=value, inline=True)
        await ctx.send(content=f"used `{ctx.message.content}`", embed=embed)


    # category_info(): async
    @info.command(name="category", hidden=True)
    async def category_info(self, ctx):
        """display category information"""
        name = ""
        id = ""

        for item in ctx.guild.categories:
            name += f"`#{item.position}` {item.name} \u200b \u200b \u200b\n"
            id += f"{item.id}\n"

        embed = discord.Embed(title=f"__{ctx.guild.name}__",colour=3158584)
        embed.set_footer(text="--- Category information ---")
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="ID", value=id, inline=True)
        await ctx.send(content=f"used `{ctx.message.content}`", embed=embed)


    # channel_info(): async
    @info.command(name="channel", hidden=True)
    async def channel_info(self, ctx, type: str = "text"):
        """display roles information"""
        name = ""
        id = ""

        for item in ctx.guild.channels:
            if type == "text":
                if isinstance(item, discord.TextChannel):
                    name += f"`#{item.position}` {item.name} \u200b \u200b \u200b\n"
                    id += f"{item.id}\n"
            else:
                if isinstance(item, discord.VoiceChannel):
                    name += f"`#{item.position}` {item.name} \u200b \u200b \u200b\n"
                    id += f"{item.id}\n"

        embed = discord.Embed(title=f"__{ctx.guild.name}__",colour=3158584)
        embed.set_footer(text="--- Channel information ---")
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="ID", value=id, inline=True)
        await ctx.send(content=f"used `{ctx.message.content}`", embed=embed)


    # roles_info(): async
    @info.command(name="roles", hidden=True)
    async def roles_info(self, ctx):
        """display roles information"""
        name = ""
        id = ""

        for item in ctx.guild.roles:
            name += "{} \u200b \u200b \u200b\n".format(item.name.replace("@","\@"))
            id += f"{item.id}\n"

        embed = discord.Embed(title=f"__{ctx.guild.name}__",colour=3158584)
        embed.set_footer(text="--- Role information ---")
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="ID", value=id, inline=True)
        await ctx.send(content=f"used `{ctx.message.content}`", embed=embed)


    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def test(self, ctx):
        """DEV function !test for testing"""
        await ctx.send(f"ID: {ctx.channel.id}")

#        for member in ctx.guild.members:
#            if member.bot:
#                return await ctx.send(f"Found a freaking Bot: called {member.name}")
#        overwrites = {
#            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
#            ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
#        }
#        category = await ctx.guild.create_category_channel("Tournament Dummy", overwrites=overwrites)
#        await category.edit(position=1)
#        ch_info     = await ctx.guild.create_text_channel("Information", category=category)
#        ch_bracket  = await ctx.guild.create_text_channel("Bracket", category=category)
#        ch_question = await ctx.guild.create_text_channel("Questions", category=category)


#        overwrite = PermissionOverwrite(self.bot.get_guild(self.server).get_role(514423325049618460).permissions)
#        await category.set_permissions(self.bot.get_guild(self.server).get_role(514423325049618460), overwrite = overwrite)
#        print(category.id)
#        for item in self.bot.get_guild(self.server).categories:
#            if item.name == "Test":
#                print(item.id)



    # myroles(): async
    # Check this:
    # " ".join(r.name.replace("@",\@") for r in ctx.guild.roles)
    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def myroles(self, ctx):
        member = ctx.guild.get_member(ctx.message.author.id)
        for role in member.roles:
            if role.name != "@everyone":
                await ctx.send(f"Role: {role.name} [ID: {role.id}]")


    @commands.command(hidden=True)
    @commands.is_owner()
    async def bla(self, ctx):
        """bla test funtion"""
        #TO-DO: check for invoker in a team
        await ctx.send("Are you sure, you want to disband your Team?\nThis action cannot be reverted.\nType `disband` to confirm...")

        def check(msg):
            return msg.content == 'disband' and msg.channel == ctx.channel

        try:
            reply = await self.bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send("Your Team-Disband request (10sec) timed out. Retry...")
        else:
            # TO-DO: database operations
            await ctx.send("You successfully disbanded your Team")



#@bot.command()
#async def liv(ctx):
#    embed=discord.Embed(title="Liv (Raven Clan)", url="https://northgard.gamepedia.com/Liv", description="The custom warchief of the Raven Clan", color=0xff0000)
#    embed.set_thumbnail(url="https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/4/48/Liv-40x40.png")
#    embed.add_field(name="Health", value=75, inline=True)
#    embed.add_field(name="Defense", value=10, inline=True)
#    embed.add_field(name="AttackPower", value=15, inline=True)
#    embed.add_field(name="XP", value=80, inline=True)
#    await ctx.send(embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(DEV(bot))
