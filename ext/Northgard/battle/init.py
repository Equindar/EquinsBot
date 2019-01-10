# --- imports
import discord
import aiosqlite
from discord.ext import commands

class Battle:
    # --- attributs
    server = 486105985782644736
    teams = { }

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot
        bot.northgardbattle = self.server


    # custom Check: Server "NorthgardBattle"
    def is_NorthgardBattle():
        def predicate(ctx):
            return ctx.guild.id == 486105985782644736
        return commands.check(predicate)

    # custom Check: Role Admin
    def is_admin(ctx):
        return ctx.guild.get_role(509002502117785600) in ctx.message.author.roles

    # custom Check: Role Staff
    def is_staff(ctx):
        return ctx.guild.get_role(519421170517540864) in ctx.message.author.roles

    # custom Check: Role Team Leader
    def is_team_leader(ctx):
        return ctx.guild.get_role(519185793907032083) in ctx.message.author.roles


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Battle(bot))
