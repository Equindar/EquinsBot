# --- imports
import discord
from discord.ext import commands
import random


class CodeGen:
    # --- attributs (constants)
    numbers = "0123456789"
    upperLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowerLetters = "abcdefhijklmnopqrstuvwxyz"

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot

    # generate()
    def generate(self, blocks: int, size: int, amount: int = 1, delimiter: str = "-"):
        list = []
        pool = self.numbers + self.upperLetters + self.lowerLetters
        for i in range(amount):
            code = ""
            for x in range(blocks * size):
                if((x % size == 0) and (x != 0)):
                    code += delimiter
                code += pool[random.randint(0,len(pool)-1)]
            list.append(code)
        return list


    # get_code(): async
    @commands.command(name="code", hidden=True)
    async def get_code(self, ctx, blocks: int, size: int, amount: int = 1, delimiter: str = "-"):
        """generating Codes"""
        result = ""
        list = self.generate(blocks, size, amount, delimiter)
        for item in list:
            result += f"`{item}`\n"
            
        embed = discord.Embed(colour=3158584)
        embed.set_footer(text=f"--- Blocks: {blocks} --- || --- Block-Size: {size} ---")
        embed.add_field(name=f"Code Generator ({amount})", value=result, inline=True)
        await ctx.send(content=f"used Feature: CodeGen `{ctx.message.content}`", embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(CodeGen(bot))
