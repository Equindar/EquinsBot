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


    # confirmation(): async
    @blueprint.command()
    async def confirmation(self, ctx):
        """Confirmation Blueprint"""
        desc = """Ahoiiii Warchiefs!
            \nWe have 16 teams! Enjoy your time under siege sharpening your strategys.
            Come saturday, its WAR!
            *Check your schedule and make sure you can play on saturday.*"""
        embed = discord.Embed(title="__Confirmation Phase__",description=desc,
            colour=discord.Colour.dark_red(), timestamp = datetime.now())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format='png', size=512))
        embed.set_footer(text=f"--- Tournament: Bloody January 2019 --- ||")
        embed.add_field(name="Perform the following command to confirm:", value="```Diff\n!tournament confirm\n``` \u200b \u200b\u200b \u200b\u200b \u200b\u200b \u200b `⚠️` Only the Team Leader can confirm the Team participation.\n\u200b \u200b", inline=False)
        embed.add_field(name="Confirmation ends:", value="**2019-01-25 **(Fri.)\n**12:00 pm CET**", inline=True)
        embed.add_field(name="Bracket Announcement:", value="**2019-01-25 **(Fri.)\n**2:00 pm CET**", inline=True)
        return await ctx.send(embed=embed)


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
            "Map Size":             "Medium",
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
        return await ctx.send(embed=embed)


    # announcement(): async
    @blueprint.command()
    async def announcement(self, ctx):
        """Announcement Blueprint"""

        embed = discord.Embed(title="__Announcement: **Bloody January 2019**__",description="""
            Ahoi Warchief's
            *Its again time to be victorious for the first time im 2019.
            Compete with your team in our `Bloody January 2019` tournament and face 15 other teams.
            Train, fight, win...*
            ~ NorthgardBattle Staff
            \n```\"Grab your strongest brother in arms and sign up to fight until you're the last one standing\"\n\u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b~Weihn8smann```
            For more information check out the NorthgardBattle Discord server:
            https://discord.gg/aBFNP27""",
                              colour=discord.Colour.dark_red(),
                              timestamp = datetime.now())
        embed.set_author(name="NorthgardBattle Staff")
        embed.set_image(url="https://i.imgur.com/AMxwdFU.png")
        embed.set_footer(text=f"--- Tournament: Bloody January 2019 --- ||")
        embed.add_field(name="Start", value="**2019-01-26 **(Sat.)\n**12:00 pm CET**", inline=True)
        embed.add_field(name="Prize (team based)", value="**1st Place: 120€**", inline=True)
        embed.add_field(name="Team Limit:", value="16 Teams", inline=True)
        embed.add_field(name="Match-Ups", value="2 vs 2", inline=True)
        return await ctx.send(content="*NorthgardBattle is hosting a new Tournament*, @everyone", embed=embed)


    # news(): async
    @blueprint.command()
    async def news(self, ctx):
        """Announcement Blueprint"""

        embed = discord.Embed(title="__Announcement: **Bloody January 2019**__",description="""
            Ahoi Warchief's
            *Its again time to be victorious for the first time im 2019.
            Compete with your team in our `Bloody January 2019` tournament and face 15 other teams.
            Train, fight, win...*
            ~ NorthgardBattle Staff
            \n```\"Grab your strongest brother in arms and sign up to fight until you're the last one standing\"\n\u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b~Agrathan```""",
                              colour=discord.Colour.dark_red(),
                              timestamp = datetime.now())
        embed.set_author(name="NorthgardBattle Staff")
        embed.set_footer(text=f"--- Tournament: Bloody January 2019 --- ||")
        embed.set_image(url="https://i.imgur.com/AMxwdFU.png")
        embed.add_field(name="Start", value="**2019-01-26 **(Sat.)\n**12:00 pm CET**", inline=True)
        embed.add_field(name="Prize (team based)", value="**1st Place: 120€**", inline=True)
        embed.add_field(name="Team Limit:", value="16 Teams", inline=True)
        embed.add_field(name="Match-Ups", value="2 vs 2", inline=True)
        return await ctx.send(content="A new NorthgardBattle Tournament, YAY! @everyone", embed=embed)


    # announcement(): async
    @blueprint.command()
    async def information(self, ctx):
        """Information Blueprint"""
        server = self.bot.get_guild(self.bot.northgardbattle)
        embed = discord.Embed(title="__Information: **Bloody January 2019**__",description="""
            Hello Warlords of Northgard!
            ... and welcome to the "Bloody January 2019"-Tournament.

            It's a **2 v 2** Tournament with **16** Teams compete against each other.""",
                              colour=discord.Colour.dark_red(),
                              timestamp = datetime.now())
        embed.set_author(name="NorthgardBattle Staff")
        embed.set_footer(text=f"--- Tournament: Bloody January 2019 --- ||")
        embed.add_field(name="__Start:__", value="```2019-01-26 (Sat.)\n12:00 pm CET```", inline=True)
        embed.add_field(name="__Prize: (team based)__", value="```1st Place: 120 €```", inline=True)
        embed.add_field(name="\u200b \u200b", value="\u200b \u200b", inline=True)
        embed.add_field(name="Registration:", value=server.get_channel(537581556202733568).mention, inline=True)
        embed.add_field(name="Bracket:", value=server.get_channel(537580627105415168).mention, inline=True)
        embed.add_field(name="Match-Results:", value=server.get_channel(537580628736999434).mention, inline=True)
        return await ctx.send(embed=embed)


    # announcement(): async
    @blueprint.command()
    async def details(self, ctx):
        """Details Blueprint"""
        desc = """
            **Registration:**
            Once 16 Teams are registered, the `BackUp-Queue` is enabled.
            *Further team registration are put into the queue and getting chronologically replaced, when a team disband or dont show up intime at the tournament.*
            Let the hope die last!

            **Bracket:**
            When all 16 teams are confirmed, the Bracket gets shuffled and published.
            The Bracket will show what team that is going to create the lobby. It is very important that you check the bracket to see who your opponent is. When the lobby is created, the other team has 10 min to join and start the game. If not, they will auto loose.

            **Bans:**
            Each team will have the option to BAN a clan. The 2 clans that are banned can not be played by either team! Performing the Banning Phase in the Game Lobby!

            **Disconnects:**
            If someone during game gets disconnected, you cannot start over. This is yet again because we have to provide a good flow so we don’t have to wait to long for next match to start.

            **Match-Results:**
            As soon as the match is finished, you have to notify it with the winning team name so we can update the bracket. The Team Leader of the winning Team attachs anEndGame-Screenshot as evidence.

            **Broadcasts / Streaming:**
            Most of the games will be streamed by some streamers. They will have to add you on steam so they can be able to stream it. So check your friends request on steam so you can add the streamers."""
        server = self.bot.get_guild(self.bot.northgardbattle)
        embed = discord.Embed(title="__Details: **Bloody January 2019**__",description=desc,colour=discord.Colour.dark_red(),timestamp = datetime.now())
        embed.set_author(name="NorthgardBattle Staff")
        embed.set_footer(text=f"--- Tournament: Bloody January 2019 --- ||")
        return await ctx.send(embed=embed)


    # announcement(): async
    @blueprint.command()
    async def banner(self, ctx):
        """Banner Blueprint"""
        embed = discord.Embed(colour=discord.Colour.dark_red())
        embed.set_image(url="https://i.imgur.com/AMxwdFU.png")
        return await ctx.send(embed=embed)


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
        embed.add_field(name="Questions?", value=f"*Post your question on {self.bot.get_guild(self.bot.northgardbattle).get_channel(537580627537559554).mention} or contact {self.bot.get_guild(self.bot.northgardbattle).get_role(509005550948974603).mention} / {self.bot.get_guild(self.bot.northgardbattle).get_role(519434488225333269).mention}.*")
        embed.set_author(name="NorthgardBattle Staff")
        embed.set_footer(text="--- Tournament: Bloody January 2019 --- ||")
        return await ctx.send(embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Blueprint(bot))
