# --- imports
import discord
from datetime import datetime
from discord.ext import commands

class Match:
    # --- attributs

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot

    # match(): async
    @commands.group()
    async def match(self, ctx):
        """Manage the Match"""
        if ctx.invoked_subcommand is None:
            await ctx.send("No param...")

    # show_match(): async
    @match.command(name="show")
    async def show_match(self, ctx):
        """Display a Match"""
        print("Here: !match show")
        await ctx.send(f"{ctx.command.cog_name}: {ctx.command.name}")

    # add_match(): async
    @match.command(name="add")
    async def add_match(self, ctx):
        """add a Match"""
        print("Here: !match add")

    # [DEV] dummy(): async
    @match.command(name="dummy")
    async def dummy_match(self, ctx, number: int):
        """[DEV] Match Dummy"""
        if number == 1:
            embed = discord.Embed(title='Team #1 --- VS ---  Team #2',description='`Status:`\nTeam #1 is banning... **done**\nTeam #2 is banning...',colour=6809006, timestamp=datetime.now())
            embed.set_thumbnail(url = "https://vignette.wikia.nocookie.net/callofduty/images/e/e3/Personal_N7_vs.png")
            embed.set_footer(text='now: Banning Phase',icon_url='https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/2/2c/The_Value_of_Great_Deeds-42x42.png')
            embed.add_field(name='Team #1', value='```Ban:      Dragon\n1st Pick:\n2nd Pick:```')
            embed.add_field(name='Team #2', value='```Ban:\n1st Pick:\n2nd Pick:```')
            await ctx.send(content='used Feature: NorthgardBattle `!match dummy 1`', embed=embed)
        if number == 2:
            embed = discord.Embed(title='Team #1 --- VS ---  Team #2',description='`Status:`\nBanning Phase... **complete**\nTeam #2 is picking (1 Clan)... **done**\nTeam #1 is picking (2 Clans)... **done**\nTeam #2 is picking (1 Clan)...',colour=6809006, timestamp=datetime.now())
            embed.set_thumbnail(url = "https://vignette.wikia.nocookie.net/callofduty/images/e/e3/Personal_N7_vs.png")
            embed.set_footer(text='now: Picking Phase',icon_url='https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/2/2c/The_Value_of_Great_Deeds-42x42.png')
            embed.add_field(name='Team #1', value='```Ban:      Dragon\n1st Pick: Boar\n2nd Pick: Bear```')
            embed.add_field(name='Team #2', value='```Ban:      Snake\n1st Pick: Raven\n2nd Pick:```')
            await ctx.send(content='used Feature: NorthgardBattle `!match dummy 2`', embed=embed)
        if number == 3:
            embed = discord.Embed(title='Team #1 --- VS ---  Team #2',description='`Status:`\nBanning Phase... **complete**\nPicking Phase... **complete**\nFighting...',colour=6809006, timestamp=datetime.now())
            embed.set_thumbnail(url = "https://vignette.wikia.nocookie.net/callofduty/images/e/e3/Personal_N7_vs.png")
            embed.set_footer(text='now: Fighting...',icon_url='https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/0/0c/Young_and_Proud-42x42.png')
            embed.add_field(name='Team #1', value='```Ban:      Dragon\n1st Pick: Boar\n2nd Pick: Bear```')
            embed.add_field(name='Team #2', value='```Ban:      Snake\n1st Pick: Raven\n2nd Pick: Wolf```')
            await ctx.send(content='used Feature: NorthgardBattle `!match dummy 3`', embed=embed)
        if number == 4:
            embed = discord.Embed(title='Team #1 --- VS ---  Team #2',description='`Result`\nBanned Clans: Dragon, Snake\n`Setup:`\nTeam #1: Boar, Bear\nTeam #1: Raven, Wolf',colour=6809006, timestamp=datetime.now())
            embed.set_thumbnail(url = "https://vignette.wikia.nocookie.net/callofduty/images/e/e3/Personal_N7_vs.png")
            embed.set_footer(text='finished: Team #1 is victorious!',icon_url='https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/5/52/Fame.png')
            await ctx.send(content='used Feature: NorthgardBattle `!match dummy 4`', embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Match(bot))
