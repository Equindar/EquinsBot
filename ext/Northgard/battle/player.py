# --- imports
import discord
import aiosqlite
from datetime import datetime
from discord.ext import commands

class Player:
    # --- attributs

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot


    # me(): async
    @commands.command(name = "me")
    async def me(self, ctx):
        """display your Player profile"""
        await ctx.invoke(self.show_player, name = ctx.author.name)


    # register(): async
    @commands.command()
    async def register(self, ctx):
        """register your Player profile"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("SELECT PlayerID FROM player WHERE Name = ?;", (ctx.author.name,))
            player = await cursor.fetchone()
            await cursor.close()
            if player is None:
                await db.execute("""
                    INSERT INTO player (Name, Registration)
                    VALUES (?, ?);""", (ctx.author.name, str(datetime.now())))
                await db.commit()
                await db.execute("""
                    UPDATE discord
                    SET InternalID = ?
                    WHERE ReferenceID =
                        (SELECT PlayerID
                         FROM player
                         WHERE Name = ?);""", (str(ctx.author.id), ctx.author.name))
                await db.commit()
                return await ctx.send(f"{ctx.author.mention} got sucessfully registered. Welcome!")
            else:
                await ctx.send("You are already registered. Use `!me` to check your profile")


    # player(): async
    @commands.group()
    async def player(self, ctx):
        """manage your Player profile"""
        if ctx.invoked_subcommand is None:
            await ctx.send('no param...')


    # show_player(): async
    @player.command(name="show")
    async def show_player(self, ctx, *, name: str):
        """display a Player profile"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("""
                SELECT player.PlayerID, player.Name, player.Steam, player.Points,
                       player.Description, player.Registration, status.Value, team.Name,
                       discord.InternalID, achievements.AchievementID
                FROM player
                LEFT JOIN status ON status.StatusID = player.StatusID
                LEFT JOIN teamplayer ON teamplayer.PlayerID = player.PlayerID
                LEFT JOIN team ON team.TeamID = teamplayer.TeamID
                LEFT JOIN discord ON discord.ReferenceID = player.PlayerID
                LEFT JOIN playerachievements ON playerachievements.PlayerID = player.PlayerID
                LEFT JOIN achievements ON achievements.AchievementID = playerachievements.AchievementID
                WHERE player.Name = ? AND discord.Reference = 'Player';""", (name,))
            result = await cursor.fetchone()
            await cursor.close()
            # load achievements
            if result is not None and result[9] is not None:
                achievement = ""
                cursor = await db.execute("""
                    SELECT achievements.Icon, achievements.Name, playerachievements.Value
                    FROM player
                    LEFT JOIN playerachievements ON playerachievements.PlayerID = player.PlayerID
                    LEFT JOIN achievements ON achievements.AchievementID = playerachievements.AchievementID
                    WHERE player.PlayerID = ?;""", (result[0],))
                achievements = await cursor.fetchall()
                await cursor.close()
                for item in achievements:
                    if item[2] > 1:
                        achievement += f"`{item[0]}` {item[2]}x {item[1]}\n"
                    else:
                        achievement += f"`{item[0]}` {item[1]}\n"
            else:
                achievement = "no achievements yet"
        # TO-DO
        if result is not None:
            # data manipulation: db result (tuple)
            if result[4] is None:
                desc = "use `!player add description [text]` to add your description..."
            else:
                desc = result[4]
            if result[7] is None:
                team = "none..."
            else:
                team = result[7]
            if result[2] is None:
                steam = ""
            else:
                steam = result[2]
            embed = discord.Embed(title=f"__{result[1]}__",description=desc,colour=6809006,url=steam)
            embed.set_thumbnail(url = self.bot.get_guild(self.bot.northgardbattle).get_member(result[8]).avatar_url_as(format='png', size=512))
            embed.set_footer(text=f"--- Player-ID: #{result[0]} --- || --- Registered: {result[5][:-7]} --- || --- Status: {result[6]} ---")
            embed.add_field(name="Team", value=team, inline=True)
            embed.add_field(name="Performance", value=f"**--- {result[3]} pts ---**", inline=True)
            embed.add_field(name="Achievements", value=achievement, inline=True)
            await ctx.send(content=f"used Feature: NorthgardBattle `{ctx.message.content}`", embed=embed)
        else:
            await ctx.send(f"Player not found: '{name}'")


    # list_players(): async
    @player.command(name="list")
    async def list_players(self, ctx, page: int = 1):
        """list all registered Players"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            async with db.execute("""
                SELECT p.PlayerID, p.Name, p.Points, s.Value, p.Registration
                FROM player p
                LEFT JOIN status s on s.StatusID = p.StatusID
                ORDER BY p.PlayerID LIMIT ?, 15;""", ((page-1) * 15, )) as cursor:
                players = ""
                points = ""
                stati = ""
                async for result in cursor:
                    # data manipulation: db result (tuple)
                    players += f"`#{result[0]}` {result[1]} \u200b \u200b \u200b\n"
                    points += f"{result[2]} pts \u200b \n"
                    stati += f"{result[3]}\n"
        # generate embed
        embed = discord.Embed(title="__Player List__",
                              description=f"List of all registered players in Northgard Battle\n \nPage: {page}",
                              colour=6809006,
                              timestamp = datetime.now())
        embed.set_footer(text="--- List: sorted by PlayerID --- ||")
        if not players:
            embed.add_field(name="Player", value="no players listed here.", inline=True)
        else:
            embed.add_field(name="Player", value=players, inline=True)
            embed.add_field(name="Points", value=points, inline=True)
            embed.add_field(name="Status", value=stati, inline=True)
        await ctx.send(content=f"used Feature: NorthgardBattle `{ctx.message.content}`", embed=embed)


    # add_player(): async
    @player.command(name="add")
    @commands.guild_only()
    @commands.is_owner()
    async def add_player(self, ctx, *, name: str):
        """add a Player"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            await db.execute("""
                INSERT INTO player (Name, Registration, StatusID)
                VALUES (?, ?, 1);""", (name, str(datetime.now())))
            await db.commit()
        await ctx.send(f"Player '{name}' got sucessfully added.")


    # verify_player(): async
    @player.command(name="verify", hidden=True)
    @commands.is_owner()
    async def verify_player(self, ctx, *, name: str):
        """verify a Player"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            await db.execute("UPDATE player SET StatusID = 2 WHERE name = ?;", (name,))
            await db.commit()
        await ctx.send(f"Player '{name}' got verified.")


    # delete_player(): async
    @player.command(name="delete")
    async def delete_player(self, ctx):
        """delete the Player"""
        #TO-DO: check for invoker in a team
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("""
                SELECT PlayerID
                FROM player
                WHERE Name = ?;""", (ctx.author.name,))
            player = await cursor.fetchone()
            await cursor.close()
            if player is not None:
                await ctx.send(
                    """Are you sure, you want to delete your Player profile?\n
                    This action cannot be reverted.\n
                    Type `delete` to confirm...""")

                def check(msg):
                    return msg.content == 'delete' and msg.channel == ctx.channel

                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=10.0)
                except asyncio.TimeoutError:
                    await ctx.send("Your Player-Delete request (10sec) timed out. Retry...")
                else:
                    await db.execute("DELETE FROM playerachievements WHERE PlayerID = ? ;", (player[0],))
                    await db.execute("DELETE FROM teamplayer WHERE PlayerID = ? ;", (player[0],))
                    await db.execute("DELETE FROM player WHERE PlayerID = ? ;", (player[0],))
                    await db.commit()
                    return await ctx.send("You successfully deleted your Player profile.")
            else:
                await ctx.send("You dont have a registered Player profile.")


    # edit_player(): async
    @player.command(name="set")
    async def set_playerdata(self, ctx, subject: str, *, data: str):
        """set Data for your Player profile"""
        args = ["steam", "description"]
        if subject.lower() in args:
            async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
                if subject.lower() == "steam":
                    if data.startswith("https://steamcommunity.com/"):
                        await db.execute("UPDATE player SET Steam = ? WHERE Name = ?;", (data,ctx.author.name))
                elif subject.lower() == "description":
                    await db.execute('UPDATE player SET Description = ? WHERE Name = ?;', (data,ctx.author.name))
                await db.commit()
            await ctx.send(f"Your Player-Data '{subject}' got set to `{data}`")


    # [DEV] dummy(): async
    @player.command(name="dummy", hidden = True)
    async def dummy_player(self, ctx):
        """[DEV] Player Dummy"""
        embed = discord.Embed(title='__Equindar__',description='bla bla bla, custom description, bla bla blubb, bla bla bla, custom description, bla bla blubb, bla bla bla, custom description, bla bla blubb, bla bla bla, custom description, bla bla blubb!',colour=6809006)
        embed.set_thumbnail(url = "https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/0/05/Through_Helheim_and_back.jpg")
        embed.set_footer(text='--- Player-ID: #2 --- || --- Registered: 2018-12-01 --- || --- Status: verified ---')
        embed.add_field(name='Team(s)', value='Blood Eagle Selfie', inline = True)
        embed.add_field(name='Performance', value='**--- 28 pts ---**\n75% Winrate\n*4 Matches played*', inline = True)
        embed.add_field(name='Match History (latest 5)', value='`W 📈 +10 pts` -vs- `Team: Frostbite`\n`L 📉 -14 pts` -vs- `Team: Set in Stone`\n`W 📈 + 8 pts` -vs- `Team: Pinar`\n`W 📈 +24 pts` -vs- `Team: chip n dale`', inline = True)
        await ctx.send(content='used Feature: NorthgardBattle `' + ctx.message.content + '`', embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Player(bot))
