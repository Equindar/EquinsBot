# --- imports
import discord
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
    @commands.group(hidden = True)
    @commands.guild_only()
    @commands.is_owner()
    async def info(self, ctx):
        """display information"""
        if ctx.invoked_subcommand is None:
            await ctx.send('no param...')


    # server_info(): async
    @info.command(name="server", hidden = True)
    async def server_info(self, ctx):
        """display server information"""
        s = ctx.guild
        data = ""
        value = ""
        dict = {
            'Name': s.name,
            'ID': s.id,
            'Owner': "%s [ID: %d]" % (s.owner.name, s.owner.id)
        }

        for k,v in dict.items():
            data += k + '\n'
            value += str(v) + '\n'
        embed = discord.Embed(title='__'+ s.name +'__',colour=3158584)
        embed.set_footer(text='--- Server information ---')
        embed.add_field(name='Data', value=data, inline = True)
        embed.add_field(name='Value', value=value, inline = True)
        await ctx.send(content='used `' + ctx.message.content + '`', embed=embed)


    # category_info(): async
    @info.command(name="category", hidden = True)
    async def category_info(self, ctx):
        """display category information"""
        name = ""
        id = ""

        for item in ctx.guild.categories:
            name += '`#%d` %s \u200b \u200b \u200b\n' % (item.position, item.name)
            id += str(item.id) + '\n'

        embed = discord.Embed(title='__'+ ctx.guild.name +'__',colour=3158584)
        embed.set_footer(text='--- Category information ---')
        embed.add_field(name='Name', value=name, inline = True)
        embed.add_field(name='ID', value=id, inline = True)
        await ctx.send(content='used `' + ctx.message.content + '`', embed=embed)


    # channel_info(): async
    @info.command(name="channel", hidden = True)
    async def channel_info(self, ctx, type: str = "text"):
        """display roles information"""
        name = ""
        id = ""

        for item in ctx.guild.channels:
            if type == "text":
                if isinstance(item, discord.TextChannel):
                    name += '`#%d` %s \u200b \u200b \u200b\n' % (item.position, item.name)
                    id += str(item.id) + '\n'
            else:
                if isinstance(item, discord.VoiceChannel):
                    name += '`#%d` %s \u200b \u200b \u200b\n' % (item.position, item.name)
                    id += str(item.id) + '\n'

        embed = discord.Embed(title='__'+ ctx.guild.name +'__',colour=3158584)
        embed.set_footer(text='--- Channel information ---')
        embed.add_field(name='Name', value=name, inline = True)
        embed.add_field(name='ID', value=id, inline = True)
        await ctx.send(content='used `' + ctx.message.content + '`', embed=embed)


    # roles_info(): async
    @info.command(name="roles", hidden = True)
    async def roles_info(self, ctx):
        """display roles information"""
        name = ""
        id = ""

        for item in ctx.guild.roles:
            name += '%s \u200b \u200b \u200b\n' % (item.name.replace("@","\@"))
            id += str(item.id) + '\n'

        embed = discord.Embed(title='__'+ ctx.guild.name +'__',colour=3158584)
        embed.set_footer(text='--- Role information ---')
        embed.add_field(name='Name', value=name, inline = True)
        embed.add_field(name='ID', value=id, inline = True)
        await ctx.send(content='used `' + ctx.message.content + '`', embed=embed)


    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def test(self, ctx):
        """DEV function !test for testing"""
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        category = await ctx.guild.create_category_channel("Tournament Dummy", overwrites=overwrites)
        await category.edit(position=1)
        ch_info     = await ctx.guild.create_text_channel("Information", category=category)
        ch_bracket  = await ctx.guild.create_text_channel("Bracket", category=category)
        ch_question = await ctx.guild.create_text_channel("Questions", category=category)


#        overwrite = PermissionOverwrite(self.bot.get_guild(self.server).get_role(514423325049618460).permissions)
#        await category.set_permissions(self.bot.get_guild(self.server).get_role(514423325049618460), overwrite = overwrite)
#        print(category.id)
#        for item in self.bot.get_guild(self.server).categories:
#            if item.name == "Test":
#                print(item.id)


# --- Delete category by ID
#        for item in self.bot.get_guild(self.server).categories:
#            if item.id == 531822368897630208:
#                await item.delete(reason = "Test Delete...")
#            print("ID: %d - %s" % (item.id, item.name))


#        print(self.get_guild().name)       #failed
#        print(self.bot.get_guild())        # no ID
#        print(self.bot.get_guild().name)   # no ID
#        print(ctx.get_guild().name)        # no ID
#        print(ctx.get_channel().id)        # no ID


    # myroles(): async
    # Check this:
    # " ".join(r.name.replace("@",\@") for r in ctx.guild.roles)
    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def myroles(self, ctx):
        member = ctx.guild.get_member(ctx.message.author.id)
        for role in member.roles:
            if role.name != "@everyone":
                await ctx.send("Role: %s [ID: %d]" % (role.name, role.id))


    @commands.command()
    @commands.is_owner()
    async def bla(self, ctx):
        """bla test funtion"""
#        await ctx.send('I am Staff')
#        await ctx.send('My ID: #' + str(ctx.author.id))

        # send a user a DM
#        return await self.bot.get_guild(self.server).get_member(362347317724184580).send("test")

#        print(self.bot.get_guild(self.server).get_member(ctx.author.id).avatar_url)


#    @commands.command(hidden = True)
#    @commands.is_owner()
#    async def info(self, ctx):
#        """Displaying Data"""
#        await ctx.send("Server '%s':\nID: %s" % (ctx.guild.name, ctx.guild.id))
#        await ctx.send("Category '%s':\nID: %s" % (ctx.channel.category.name, ctx.channel.category_id))
#        await ctx.send("Channel '%s':\nID: %s" % (ctx.channel.name, ctx.channel.id))


    @commands.command()
    @commands.is_owner()
    async def test_db(self, ctx):
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            async with db.execute('SELECT * FROM clan') as cursor:
                async for row in cursor:
                    print(row)
        return True


#@bot.command()
#async def liv(ctx):
#    embed=discord.Embed(title="Liv (Raven Clan)", url="https://northgard.gamepedia.com/Liv", description="The custom warchief of the Raven Clan", color=0xff0000)
#    embed.set_thumbnail(url="https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/4/48/Liv-40x40.png")
#    embed.add_field(name="Health", value=75, inline=True)
#    embed.add_field(name="Defense", value=10, inline=True)
#    embed.add_field(name="AttackPower", value=15, inline=True)
#    embed.add_field(name="XP", value=80, inline=True)
#    await ctx.send(embed=embed)

#@bot.command()
#async def echo(ctx, *, content:str):
#    await ctx.send(content)

# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(DEV(bot))
