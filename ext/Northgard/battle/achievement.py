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
        """manage NorthgardBattle Achievements"""
        if ctx.invoked_subcommand is None:
            await ctx.send("No param...")


    # list_achievements(): async
    @achievement.command(name="list")
    async def list_achievements(self, ctx, page: int = 1):
        """list all Achievements"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            async with db.execute("SELECT * FROM achievements LIMIT ?, 15;", ((page-1) * 15, )) as cursor:
                achievements = ""
                async for result in cursor:
                    achievements += f"`#{result[0]:>2}` `{result[1]}` {result[2]}\n"
        # generate embed
        embed = discord.Embed(title="__Achievement List__",
                              description=f"List of all registered Achievements in Northgard Battle\n \nPage: {page}",
                              colour=6809006,
                              timestamp = datetime.now())
        embed.set_footer(text='--- List: sorted by AchievementID --- ||')
        if not achievements:
            embed.add_field(name='Achievements', value="no Achievements listed here.", inline=True)
        else:
            embed.add_field(name='Achievements', value=achievements, inline=True)
        await ctx.send(content=f"used Feature: NorthgardBattle `{ctx.message.content}`", embed=embed)


    # add_achievement(): async
    @achievement.command(name="add")
    @commands.is_owner()
    async def add_achievement(self, ctx, icon: str, *, title: str):
        """add an Achievement"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            await db.execute("INSERT INTO achievements (Icon, Name) VALUES (?, ?);", (icon, title))
            await db.commit()
        await ctx.send(f"Achievement '{title}' (Icon: {icon}) got sucessfully added.")


    # grant_achievement(): async
    @achievement.command(name="assign")
    async def assign_achievement(self, ctx, id: int, *, target: str):
        """assign an Achievement to a Player"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("""
                SELECT AchievementID, Name
                FROM achievements
                WHERE AchievementID = ?;""", (id,))
            achievement = await cursor.fetchone()
            await cursor.close()
            if achievement is not None:
                cursor = await db.execute("""
                    SELECT player.PlayerID, discord.InternalID
                    FROM player
                    LEFT JOIN discord ON discord.ReferenceID = player.PlayerID
                    WHERE discord.Reference = 'Player' AND player.Name = ?;""", (target,))
                player = await cursor.fetchone()
                await cursor.close()
                if player is not None:
                    cursor = await db.execute("""
                        SELECT playerachievements.Value
                        FROM playerachievements
                        LEFT JOIN player ON player.PlayerID = playerachievements.PlayerID
                        WHERE player.PlayerID = ? AND playerachievements.AchievementID = ?;""", (player[0],achievement[0]))
                    result = await cursor.fetchone()
                    await cursor.close()
                    # Achievement already exists?
                    if result is not None:
                        await db.execute("""
                            UPDATE playerachievements
                            SET Value = ?
                            WHERE PlayerID = ? AND AchievementID = ?;""", (result[0] + 1,player[0],achievement[0]))
                    else:
                        await db.execute("""
                            INSERT INTO playerachievements (PlayerID, AchievementID)
                            VALUES (?,?)""", (player[0], achievement[0]))
                    await db.commit()
                    await ctx.send(f"Achievement '{achievement[1]}' got sucessfully assigned to Player '{target}'.")
                    await self.bot.get_guild(self.bot.northgardbattle).get_member(player[1]).send(
                        f"Congratulations! You have got a new Achievement on Northgard Battle:\n`{achievement[1]}`")
                else:
                    return await ctx.send(f"Player not found (Name: {target})")
            else:
                return await ctx.send(f"Achievement not found (ID: {id})")


    # delete_achievement(): async
    @achievement.command(name="delete", hidden=True)
    async def delete_achievement(self, ctx):
        """delete an Achievement"""
        print("Here: !achievement delete")


    # set_achievement_data(): async
    @achievement.command(name="set", hidden=True)
    async def set_achievement_data(self, ctx, subject: str, *, data: str):
        """set Data for your achievement profile"""
        args = ["icon", "title"]
        if subject.lower() in args:
            async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
                if subject.lower() == "icon":
                    if data.startswith("https://steamcommunity.com/"):
                        await db.execute("UPDATE achievement SET Steam = ? WHERE Name = ?;", (data, ctx.author.name))
                elif subject.lower() == "title":
                    await db.execute('UPDATE achievement SET Description = ? WHERE Name = ?;', (data, ctx.author.name))
                await db.commit()
            await ctx.send(f"Your Achievement-Data '{subject}' got set to `{data}`")



# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Achievements(bot))
