# --- imports
import discord
import aiosqlite
from datetime import datetime
from discord.ext import commands

class Achievements:
    # --- attributs

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot


    # achievement(): async
    @commands.group()
    async def achievement(self, ctx):
        """manage NorthgardBattle Achievements """
        if ctx.invoked_subcommand is None:
            await ctx.send('no param...')


    # list_achievements(): async
    @achievement.command(name="list")
    async def list_achievements(self, ctx, page: int = 1):
        """list all Achievements"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            async with db.execute("SELECT * FROM achievements LIMIT ?, 15;", ((page-1) * 15, )) as cursor:
                achievements = ""
                async for result in cursor:
                    # data manipulation: db result (tuple)
                    achievements += "`#%s` `%s` %s\n" % (str(result[0]), result[1], result[2])
        # generate embed
        embed = discord.Embed(title='__Achievement List__',description='List of all registered achievements in Northgard Battle\n \nPage: '+ str(page),colour=6809006, timestamp = datetime.now())
        embed.set_footer(text='--- List: sorted by AchievementID --- ||')
        if not achievements:
            embed.add_field(name='Achievements', value="no achievements listed here.", inline = True)
        else:
            embed.add_field(name='Achievements', value=achievements, inline = True)
        await ctx.send(content='used Feature: NorthgardBattle `' + ctx.message.content + '`', embed=embed)


    # add_achievement(): async
    @achievement.command(name="add")
    @commands.is_owner()
    async def add_achievement(self, ctx, icon: str, *, title: str):
        """add an Achievement"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            await db.execute("INSERT INTO achievements (Icon, Name) VALUES (?, ?);", ( icon, title ))
            await db.commit()
        await ctx.send("Achievement '%s' (Icon: %s) got sucessfully added." % (title, icon))


    # grant_achievement(): async
    @achievement.command(name="assign")
    @commands.is_owner()
    async def assign_achievement(self, ctx, id: int, *, target: str):
        """assign an Achievement to a Player"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("SELECT AchievementID, Name FROM achievements WHERE AchievementID = ?;", ( id, ))
            achievement = await cursor.fetchone()
            await cursor.close()
            if achievement is not None:
                cursor = await db.execute("SELECT player.PlayerID, discord.InternalID FROM player LEFT JOIN discord ON discord.ReferenceID = player.PlayerID WHERE discord.Reference = 'Player' AND player.Name = ?;", ( target, ))
                player = await cursor.fetchone()
                await cursor.close()
                if player is not None:
                    await db.execute("INSERT INTO playerachievements (PlayerID, AchievementID) VALUES (?,?)", (player[0], achievement[0]))
                    await db.commit()
                    await ctx.send("Achievement '%s' got sucessfully assigned to Player '%s'." % (achievement[1], target))
                    await self.bot.get_guild(self.bot.northgardbattle).get_member(player[1]).send("Congratulations! You have got a new Achievement on Northgard Battle:\n`%s`" % (achievement[1]))
                else:
                    return await ctx.send("Player not found (Name: %s)" % (target))
            else:
                return await ctx.send("Achievement not found (ID: %s)" % (id))


    # delete_achievement(): async
    @achievement.command(name="delete", hidden = True)
    async def delete_achievement(self, ctx):
        """delete an Achievement"""
        print("Here: !achievement delete")
        print(self.bot.northgardbattle)


    # set_achievement_data(): async
    @achievement.command(name="set", hidden = True)
    async def set_achievement_data(self, ctx, subject: str, *, data: str):
        """set Data for your achievement profile"""
        args = ["icon", "title"]
        if subject.lower() in args:
            async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
                if subject.lower() == "icon":
                    if data.startswith("https://steamcommunity.com/"):
                        await db.execute("UPDATE achievement SET Steam = ? WHERE Name = ?;", ( data, ctx.author.name ))
                elif subject.lower() == "title":
                    await db.execute('UPDATE achievement SET Description = ? WHERE Name = ?;', (data, ctx.author.name))
                await db.commit()
            await ctx.send("Your Achievement-Data '%s' got set to `%s`" % (subject, data))



# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Achievements(bot))
