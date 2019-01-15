# --- imports
import discord
import time
import aiosqlite
from datetime import datetime, timedelta
from discord.ext import commands

class Blueprint:
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


    # blueprint(): async
    @commands.group(hidden=True)
    async def blueprint(self, ctx):
        """Manage the Tournament"""
        if ctx.invoked_subcommand is None:
            await ctx.send("No param...")


    # lobby(): async
    @blueprint.command()
    async def lobby(self, ctx):
        """Lobby Blueprint"""
        dict = {
            "Lobby Name":           "NorthgardBattle Match #`[No.]`",
            "Mode":                 "Public",
            "Players":              "Team 2 vs 2",
            "Game Server":          "Europe",
            "Difficulty":           "High (not Extreme)",
            "Map Generation":       "Balanced",
            "Game Mode":            "Ragnarok",
            "Victory Conditions":   "All"
        }
        setting = ""
        value = ""
        for k, v in dict.items():
            setting += f"`✔️` {k}\n"
            value += f"{v}\n"
        embed = discord.Embed(title="__Checklist (Teamleader): **Lobby Creation**__",
                              description="Setup a Tournament-Match with the following preset:",
                              colour=discord.Colour.dark_teal(),
                              timestamp = datetime.now())
        embed.set_author(name="NorthgardBattle Staff")
        embed.set_footer(text=f"--- Tournament: Bloody January 2019 --- ||")
        embed.add_field(name="Lobby Settings", value=setting, inline=True)
        embed.add_field(name="\u200b \u200b", value=value, inline=True)
        return await ctx.send(content="\u200b \u200b", embed=embed)


    # announcement(): async
    @blueprint.command()
    async def announcement(self, ctx):
        """Announcement Blueprint"""

        embed = discord.Embed(title="__Announcement: **Bloody January 2019**__",description="""
            Ahoi Warchief's
            *Its again time to be victorious for the first time im 2019.
            Compete with your team in our `Bloody January 2019` tournament and face 15 other teams.
            Train, fight, win...*
            \n```\"Grab your strongest brother in arms and sign up to fight until you're the last one standing\"\n\u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b~Agrathan```
            For more information check out the NorthgardBattle Discord server:
            https://discord.gg/aBFNP27""",
                              colour=discord.Colour.dark_red(),
                              timestamp = datetime.now())
        embed.set_author(name="NorthgardBattle Staff")
        embed.set_image(url="https://i.imgur.com/AMxwdFU.png")
        embed.set_footer(text=f"--- Tournament: Bloody January 2019 --- ||")
        embed.add_field(name="Start", value="**2018-01-26 **(Sat.)\n**12:00 pm CET**", inline=True)
        embed.add_field(name="Prize (team based)", value="1st Place: 120€", inline=True)
        embed.add_field(name="Team Limit:", value="16 Teams", inline=True)
        embed.add_field(name="Match-Ups", value="2 vs 2", inline=True)
        return await ctx.send(content="\u200b \u200b", embed=embed)


    @blueprint.command()
    async def registration(self, ctx):
        """Registration Blueprint"""
        embed = discord.Embed(title="__Tournament: **Team Registration**__",description="Register your Team here...",
                              colour=discord.Colour.dark_red(),
                              timestamp = datetime.now())
        embed.add_field(name="**Feature: Quick-Join** `[🔥NEW]`",value="""
                If you are already a Team Leader with a registered team,
                "quick-join" the Tournament "Bloody January 2019" with:
                ```!tournament join```""")
        embed.add_field(name="Common Way", value="""
                Otherwise its also fairly simple, check out the EquinsBot Guides, start with:
                ```!guide player```Or take the Crash Course (the "TLDR" Guide):
                ```!crash-course```""")
        embed.add_field(name="Problems with `!commands`?", value=f"*If you have issues, feel free to contact {self.bot.get_guild(self.bot.northgardbattle).get_member(362347317724184580).mention} for help.*")
        embed.add_field(name="Questions?", value=f"*Post your question on {self.bot.get_guild(self.bot.northgardbattle).get_channel(532526880113295361).mention} or contact {self.bot.get_guild(self.bot.northgardbattle).get_role(509005550948974603).mention} / {self.bot.get_guild(self.bot.northgardbattle).get_role(519434488225333269).mention}.*")
        embed.set_author(name="NorthgardBattle Staff")
        embed.set_footer(text="--- Tournament: Bloody January 2019 --- ||")
        return await ctx.send(content="\u200b \u200b", embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Blueprint(bot))