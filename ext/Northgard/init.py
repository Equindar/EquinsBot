# --- imports
import discord
import aiohttp
import sys
import traceback
from discord.ext import commands

class Northgard:
    # --- attributs
    modules = [ 'ext.Northgard.battle.init',
                'ext.Northgard.wiki.init',
                'ext.Northgard.battle.match',
                'ext.Northgard.battle.player',
                'ext.Northgard.battle.team',
                'ext.Northgard.battle.tournament',
                'ext.Northgard.battle.achievement'
              ]

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot
        # load modules()
        for module in self.modules:
            try:
                bot.load_extension(module)
            except Exception as e:
                print(f"Failed to load Northgard module {module}.", file=sys.stderr)
                traceback.print_exc()
            print(f"[System] Northgard Module: {module} loaded")


    # online(): async
    @commands.command()
    async def online(self, ctx):
        """shows Northgard related game information (SteamAPI)"""
        async with aiohttp.ClientSession() as session:
            target = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=466560"
            async with session.get(target) as response:
                if(response.status) == 200:
                    data = await response.json()
                    result = f"Players online in Northgard: {data['response']['player_count']}"
                    await ctx.send(result)


    # helpout_user(): async
    @commands.command(name="help-out", hidden=True)
    @commands.is_owner()
    async def helpout_user(self, ctx, *, target: str):
        """sends a Help-Out Message to a known User"""
        for member in self.bot.get_all_members():
            if member.name == target:
                return await self.bot.get_guild(member.guild.id).get_member(member.id).send(
                    f"**Hi {target},**\n*{ctx.author.name} send me to help you out!*")
        return await ctx.send(f"I dont know the User '{target}'")


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Northgard(bot))
