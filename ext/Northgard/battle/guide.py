# --- imports
import discord
import time
import aiosqlite
from datetime import datetime, timedelta
from discord.ext import commands

class Guide:
    # --- attributs


    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot


    # blueprint(): async
    @commands.group()
    async def guide(self, ctx):
        """Manage the Tournament"""
        if ctx.invoked_subcommand is None:
            guides = {
                "Basics: Player": "player",
                "Basics: Team": "team",
                "In-Dept: Leader": "leader",
                "Basics: Tournament": "tournament"
            }
            topic = ""
            value = ""
            for k, v in guides.items():
                topic += f"{k}\n"
                value += f"`!guide {v}`\n"
            desc = "Feel free to read them, its helpful..."
            embed = discord.Embed(title="__EquinsBot Guides: **Summary**__",description=desc,colour=3158584)
            embed.set_footer(text="--- EquinsBot --- || --- Guides (\"Summary\") --- ")
            embed.add_field(name="Topic", value=topic,inline=True)
            embed.add_field(name="\u200b \u200b", value=value, inline=True)
            embed.add_field(name="\u200b \u200b", value="Thanks for reading... ~Equindar", inline=False)
            return await ctx.author.send(content="\u200b \u200b", embed=embed)


    # guide_player(): async
    @guide.command(name="player")
    async def guide_player(self, ctx):
        """Basics: Player"""
        desc = """*First of all, welcome to NorthgardBattle!*
            A Player profile can provide additional data like a Description and your Steam Profile.
            It is required to register and manage a Team on NorthgardBattle."""
        embed = discord.Embed(title="__Guide **Basics: Player**__",description=desc,colour=3158584)
        embed.set_footer(text="--- EquinsBot --- || --- Guide #1 (\"Basics: Player\") --- ")
        embed.add_field(name="How do i register my Player profile?", value="```Diff\n!register\n```",inline=False)
        embed.add_field(name="How do i edit my Player data?", value="```!player set description [text]\n!player set steam [https://steamcommunity.com/ ... ]```", inline=False)
        embed.add_field(name="How can i check my Profile?", value="```!me```", inline=True)
        embed.add_field(name="How can i check other Player Profiles?", value="```!player show [Name]```", inline=True)
        embed.add_field(name="How can i list all registered Players?", value="```!player list\n!player list 2\n!player list [page]```", inline=True)
        embed.add_field(name="How can i delete my Player profile?", value="```!player delete```", inline=True)
        embed.add_field(name="\u200b \u200b", value="**Congratulation, you know now the Basics, how to manage Player profiles!**\n*Next Step: Basics of a Team:* `!guide team`")
        return await ctx.author.send(content="\u200b \u200b", embed=embed)


    # guide_team(): async
    @guide.command(name="team")
    async def guide_team(self, ctx):
        """Basics: Team"""
        desc = """*Working with teams is no witchcraft, let's start!*
            A team profiles displays various information:
            `⬜` your Team roster (the Leader, Members and Substitutes)
            `⬜` your Team description and the **Status**
            It is required to join NorthgardBattle tournaments."""
        embed = discord.Embed(title="__Guide **Basics: Team**__",description=desc,colour=3158584)
        embed.set_footer(text="--- EquinsBot --- || --- Guide #2 (\"Basics: Team\") --- ")
        embed.add_field(name="How do i register my Team?", value="```Diff\n!team register [name]\n```", inline=False)
        embed.add_field(name="How do i join a Team?", value="```Diff\n!team join [code: XXXX-XXXX-XXXX]```", inline=False)
        embed.add_field(name="How can i check my Team?", value="```!myteam```", inline=True)
        embed.add_field(name="How can i list all registered Teams?", value="```!team list\n!team list 2\n!team list [page]```", inline=True)
        embed.add_field(name="How do i check other Teams?", value="```!team show [Name]```", inline=True)
        embed.add_field(name="How can i leave my Team?", value="```!team leave```", inline=True)
        embed.add_field(name="\u200b \u200b", value="**Congratulation, you know now the Basics of your Team!**\n*Next Step: In-Dept of a Team:* `!guide leader`")
        return await ctx.author.send(content="\u200b \u200b", embed=embed)


    # guide_leader(): async
    @guide.command(name="leader")
    async def guide_leader(self, ctx):
        """In-Dept: Leader"""
        desc = """*The magic starts as a Team Leader, ready for it?*
            As a Team Leader, you can manage your Team:
            `⬜` edit the Team data (Description, Name)
            `⬜` generate Invite-Codes for new Team Mates
            `⬜` assign a Team Mate to a new Role (Member, Substitute)
            `⬜` disband your Team"""
        embed = discord.Embed(title="__Guide **In-Dept: Leader**__",description=desc,colour=3158584)
        embed.set_footer(text="--- EquinsBot --- || --- Guide #3 (\"In-Dept: Leader\") --- ")
        embed.add_field(name="How do i edit my Team data?", value="```\n!team set name [new name]\n!team set description [text]```", inline=False)
        embed.add_field(name="How can invite registered Player?", value="```\n!team invite Member\n!team invite Substitute```", inline=False)
        embed.add_field(name="How can i change the Team roster?", value="```!team assign Member [Player Name]\n!team assign Substitute [Player Name]```", inline=False)
        embed.add_field(name="How can i disband my Team?", value="```!team disband```", inline=False)
        embed.add_field(name="\u200b \u200b", value="**Congratulation, you know now how to manage your Team!**\n*Next Step: Tournaments:* `!guide tournament`")
        return await ctx.author.send(content="\u200b \u200b", embed=embed)


    # guide_tournament(): async
    @guide.command(name="tournament")
    async def guide_tournament(self, ctx):
        """Basics: Tournament"""
        desc = """*Compete with your Team in a Tournament:*
            Finally setting up your Team pays off..."""
        embed = discord.Embed(title="__Guide **Basics: Tournament**__",description=desc,colour=3158584)
        embed.set_footer(text="--- EquinsBot --- || --- Guide #4 (\"Basics: Tournament\") --- ")
        embed.add_field(name="How do i let my Team join a Tournament?", value="```Diff\n!tournament join```", inline=False)
        embed.add_field(name="More features coming soon...", value="\u200b \u200b", inline=False)
        embed.add_field(name="\u200b \u200b", value="**Congratulation, you can deal with tournaments!**\n*Next Step:* `coming soon`")
        return await ctx.author.send(content="\u200b \u200b", embed=embed)


    # guide_crashcourse(): async
    @commands.command(name="crash-course")
    async def guide_crashcourse(self, ctx):
        """Crash-Course"""
        desc = """*First of all, welcome to NorthgardBattle!*
            This Crash Course is a **Quick'n'Dirty-Approach** to join a Tournament.
            It should do the trick for now, but *reading the Guides is recommended*..."""
        embed = discord.Embed(title="__Crash Course: **Join the Tournament**__",description=desc,colour=3158584)
        embed.set_footer(text="--- EquinsBot --- || --- Crash Course (\"Join the Tournament\") --- ")
        embed.add_field(name="Step #1: Register your Player profile", value="```!register```",inline=False)
        embed.add_field(name="Step #2: Bind your Steam Profile to your Profile", value="```!player set steam [https://steamcommunity.com/ ... ]```", inline=False)
        embed.add_field(name="Step #3: Register your Team", value="```!team register```", inline=False)
        embed.add_field(name="Step #4: Join the Tournament", value="```!tournament join```", inline=False)
        embed.add_field(name="Last Step:", value="Fill up your Team Roster before **Team Confirmation**", inline=True)
        embed.add_field(name="\u200b \u200b", value="**Congratulation, you took the 3 minutes Crash Course!**\nFeel free to read the Guides: `!guide` later.")
        return await ctx.author.send(content="\u200b \u200b", embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Guide(bot))
