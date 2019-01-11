# --- imports
import discord
import time
from datetime import datetime, timedelta
from discord.ext import commands

class Tournament:
    # --- attributs
    staff = 519421170517540864
    admin = 509002502117785600
    headmoderator = 519434488225333269
    moderator = 509005550948974603
    participant = 519421297235853313
    backQueue = 521693581589741573
    leader = 519185793907032083

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot


    # tournament(): async
    @commands.group(hidden=True)
    async def tournament(self, ctx):
        """Manage the Tournament"""
        if ctx.invoked_subcommand is None:
            await ctx.send("No param...")


    # create_tournament(): async
    @tournament.command(name="create")
    @commands.is_owner()
    async def create_tournament(self, ctx, *, name: str = "Untitled Tournament"):
        """create a new Tournament"""
        ow_category = {
            ctx.guild.get_role(self.participant): discord.PermissionOverwrite(read_messages=True),
            ctx.guild.get_role(self.backQueue): discord.PermissionOverwrite(read_messages=True),
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        ow_info = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                read_messages=True, send_messages=False, read_message_history=True, add_reactions=False)
        }
        ow_bracket = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True)
        }
        ow_results = {
            ctx.guild.get_role(self.leader): discord.PermissionOverwrite(attach_files=True)
        }

        # create category
        category = await ctx.guild.create_category_channel(f"[{name}]", overwrites=ow_category)
        await category.edit(position=2)
        # create channels
        ch_info     = await ctx.guild.create_text_channel("Information", category=category)
        ch_bracket  = await ctx.guild.create_text_channel("Bracket", category=category, overwrites=ow_bracket)
        ch_question = await ctx.guild.create_text_channel("Questions", category=category)
        ch_results  = await ctx.guild.create_text_channel("Match Results", category=category)
        # set channel perms
        await ch_info.set_permissions(ow_info)
        await ctx.send("Tournament got set up.")


    # set_date(): async
    @tournament.command(name="date")
    @commands.is_owner()
    async def set_date(self, date: datetime):
        self.date = date
        print(type(self.date))
        print(self.date)


    # deadline(): async
    @commands.command()
    @commands.guild_only()
    async def deadline(self, ctx):
        """[DEV] Deadline Display"""
        emoji = {
            0:':zero:', 1:':one:', 2:':two:', 3:':three:', 4:':four:',
            5:":five:", 6:":six:", 7:":seven:", 8:":eight:", 9:":nine:"
        }

        now = datetime.now()
        date = datetime(2018,12,15,12,0,0)
        # create dict
        td = date - now
        if td.total_seconds() < 0:
            return
        d = {"D": td.days }
        d["H"], rem = divmod(td.seconds, 3600)
        d["M"], d["S"] = divmod(rem, 60)
        # get string / + zfill()
        s = ""
        for key, value in d.items():
            s += str(value).zfill(2) + " **:** "
        # replace with dict
        x = ""
        for c in s[:-7]:
            if(c.isdigit()):
                x += emoji[int(c)]
            else:
                x += c
        embed = discord.Embed(colour=6809006, timestamp = date - timedelta(hours=1))
        embed.add_field(name='aXe-Mas Tournament starting in...', value=':stopwatch: ' + x)
        await ctx.send(content='used Feature: Deadline `!deadline`', embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Tournament(bot))
