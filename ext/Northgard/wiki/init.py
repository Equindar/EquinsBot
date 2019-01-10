# --- imports
import discord
import aiohttp
from discord.ext import commands

class Wiki:
    # --- attributs

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot

    # knowledge(): async
    @commands.command()
    async def knowledge(self, ctx):
        """Display a Knowledge (atm: Journeymen)"""
        embed = discord.Embed(title='Knowledge: Journeymen',description='Increases your Happiness based on the areas you have explored.',colour=0xFF0000)
        embed.set_thumbnail(url = "https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/6/6f/Journeymen-42x42.png")
        embed.set_footer(text='unique Raven Knowledge',icon_url='https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/e/e1/Raven_red-24x24.png')
        await ctx.send(content='used Feature: NorthgardWiki `!wiki journeymen`', embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Wiki(bot))
