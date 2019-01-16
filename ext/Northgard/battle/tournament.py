# --- imports
import discord
import time
import aiosqlite
from datetime import datetime, timedelta
from discord.ext import commands

class Tournament:
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


    # tournament(): async
    @commands.group()
    async def tournament(self, ctx):
        """Manage the Tournament"""
        if ctx.invoked_subcommand is None:
            await ctx.send("No param...")


    # add_tournament(): async
    @tournament.command(name="add", hidden=True)
    @commands.is_owner()
    async def add_tournament(self, ctx, *, name: str):
        """add a Tournament"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            await db.execute("""
                INSERT INTO tournament (Name, CreationDate)
                VALUES (?, ?);""", (name, str(datetime.now())))
            await db.commit()
        await ctx.send(f"Tournament '{name}' got **sucessfully added**.")


    # join_tournament(): async
    @tournament.command(name="join", hidden=True)
    async def join_tournament(self, ctx):
        """join an active Tournament"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            # check: list active tournament
            cursor = await db.execute("""
                SELECT TournamentID, Name, TeamLimit
                FROM tournament
                WHERE StatusID = 3""")
            tournament = await cursor.fetchall()
            await cursor.close()
            if tournament is not None:
                # list tournaments
                output = ""
                dict = {}
                for item in tournament:
                    output += f"Type in: `{item[1]}` to join...\n"
                    dict[item[1]] = item[0]
                cursor = await db.execute("""
                    SELECT team.TeamID, team.Name
                    FROM team
                    LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                    LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                    WHERE teamplayer.RoleID = 2 AND player.Name = ?""", (ctx.author.name,))
                team = await cursor.fetchone()
                await cursor.close()
                # check: in Team and Team Leader?
                if team is not None:
                    await ctx.author.send(f"Are you sure, you want to join an active Tournament?\n{output}")
                    def check(msg):
                        return msg.content in dict and msg.channel == ctx.author.dm_channel
                    try:
                        reply = await self.bot.wait_for('message', check=check, timeout=20.0)
                    except asyncio.TimeoutError:
                        await ctx.author.send("Your Tournament-Join request (20sec) timed out. Retry...")
                    else:
                        async with db.execute("""
                            SELECT Count(participant.ParticipantID), team.TeamID
                            FROM participant
                            LEFT JOIN team ON team.TeamID = participant.TeamID
                            WHERE TournamentID = ?""", (dict[reply.content],)) as cursor:
                            counter = 0
                            async for result in cursor:
                                if result[1] == team[0]:
                                    return await ctx.author.send(f"Your Team '{team[1]}' already joined '{reply.content}'")
                                counter += 1
                        if counter < tournament[0][2]:
                            # push to Participant
                            await db.execute("""
                                INSERT INTO participant (ParticipantTypeID, TournamentID, TeamID, Position)
                                VALUES (1, ?, ?, ?)""", (dict[reply.content], team[0], counter))
                            await db.commit()
                            await self.team_joined(ctx, pos = counter, team_id = team[0])
                            return await ctx.author.send(f"Your Team '{team[1]}' **successfully joined** '{reply.content}'")
                        else:
                            # push to BackupQueue
                            await db.execute("""
                                INSERT INTO participant (ParticipantTypeID, TournamentID, TeamID, Position)
                                VALUES (2, ?, ?, ?)""", (dict[reply.content], team[0], counter))
                            await db.commit()
                            await self.team_joined(ctx, pos = counter, team_id = team[0])
                            return await ctx.author.send(
                                f"""Your Team '{team[1]}' **successfully joined** '{tournament[1]}'
                                \nYou entered the BackupQueue at Position #{(counter)-tournament[2]}""")
                else:
                    await ctx.author.send("""You **cannot join** a tournament.\n
                        \n__Reasons can be:__\nYou are not in a Team.\nYou are not the Team Leader.""")
            else:
                return await ctx.author.send("No active (joinable) Tournament found.")


    async def team_joined(self, ctx, pos: int, team_id: int):
        """DISCORD WORKFLOW"""
        server = self.bot.get_guild(self.bot.northgardbattle)
        team = None
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            async with db.execute("""
                SELECT discord.InternalID, player.Name, teamplayer.RoleID, team.Name
                FROM teamplayer
                LEFT JOIN discord ON discord.ReferenceID = teamplayer.PlayerID
                LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                LEFT JOIN team ON team.TeamID = teamplayer.TeamID
                WHERE discord.Reference = "Player" AND teamplayer.TeamID = ?""", (team_id,)) as cursor:
                async for result in cursor:
                    if team is None:
                        for item in server.roles:
                            if f"Team: {result[3]}" == item.name:
                                team = item
                                break
                    if team is None:
                        team = await server.create_role(name = f"Team: {result[3]}")
                    member = server.get_member(result[0])
                    if team not in member.roles:
                        await member.add_roles(team)
                    if pos <= 16:
                        if server.get_role(self.participant) not in member.roles:
                            await member.add_roles(server.get_role(self.participant))
                    else:
                        if server.get_role(self.backQueue) not in member.roles:
                            await member.add_roles(server.get_role(self.backQueue))
        for item in  server.categories:
            if item.id == 519174714002898984:
                category = item
        perms = {   team: discord.PermissionOverwrite(read_messages=True, connect=True, speak=True),
                    server.get_role(self.staff): discord.PermissionOverwrite(read_messages=True, connect=True, speak=True),
                    server.get_role(self.participant): discord.PermissionOverwrite(read_messages=False),
                    server.get_role(self.backQueue): discord.PermissionOverwrite(read_messages=False),
                    server.default_role: discord.PermissionOverwrite(read_messages=False, connect=False)
        }
        team_ch = await server.create_voice_channel(f"[#{pos}] {result[3]}", category=category, overwrites=perms)
        if pos <= 16:
            desc = f"`✔️` Team **{result[3]}** joined the Tournament."
        else:
            desc = f"`✔️` Team **{result[3]}** joined the Tournament\nIt got set to the BackupQueue (Position: #{pos-16})."
        embed = discord.Embed(description=desc,colour=discord.Colour.dark_green(), timestamp = datetime.now())
        embed.set_footer(text="--- Tournament: Bloody January 2019 --- ||")
        return await server.get_channel(534764595970310145).send(embed=embed)


    # set_date(): async
    @tournament.command(name="date")
    @commands.is_owner()
    async def set_date(self, date: datetime):
        self.date = date
        print(type(self.date))
        print(self.date)


    # deadline(): async
    @commands.command()
    async def deadline(self, ctx):
        """[DEV] Deadline Display"""
        emoji = {
            0:':zero:', 1:':one:', 2:':two:', 3:':three:', 4:':four:',
            5:":five:", 6:":six:", 7:":seven:", 8:":eight:", 9:":nine:"
        }
        now = datetime.now()
        date = datetime(2019,1,26,12,0,0)
        # create dict
        td = date - now
        if td.total_seconds() < 0:
            return
        d = {"D": td.days }
        d["H"], rem = divmod(td.seconds, 3600)
        d["M"], d["S"] = divmod(rem, 60)
        # get string / + zfill()
        s = ""
        for key, value in d.items():
            s += str(value).zfill(2) + " **:** "
        # replace with dict
        x = ""
        for c in s[:-7]:
            if(c.isdigit()):
                x += emoji[int(c)]
            else:
                x += c
        embed = discord.Embed(colour=6809006, timestamp = date - timedelta(hours=1))
        embed.add_field(name='Tournament: **Bloody January 2019** starting in...',
                        value=f":stopwatch: {x}\n \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b`\u200b DAYS \u200b` \u200b \u200b `\u200b HOURS ` \u200b \u200b \u200b `\u200b MINS \u200b` \u200b \u200b `\u200b SECS \u200b`")
        await ctx.send(embed=embed)


    # setup_tournament(): async
    @tournament.command(name="setup", hidden=True)
    @commands.is_owner()
    async def setup_tournament(self, ctx, *, name: str = "Untitled Tournament"):
        """create a new Tournament"""
        ow_category = {
            ctx.guild.get_role(self.participant): discord.PermissionOverwrite(read_messages=True),
            ctx.guild.get_role(self.backQueue): discord.PermissionOverwrite(read_messages=True),
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        ow_info = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                read_messages=True, send_messages=False, read_message_history=True, add_reactions=False)
        }
        ow_bracket = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True)
        }
        ow_results = {
            ctx.guild.get_role(self.leader): discord.PermissionOverwrite(attach_files=True)
        }

        # create category
        category = await ctx.guild.create_category_channel(f"[{name}]", overwrites=ow_category)
        await category.edit(position=2)
        # create channels
        ch_info     = await ctx.guild.create_text_channel("Information", category=category)
        ch_bracket  = await ctx.guild.create_text_channel("Bracket", category=category, overwrites=ow_bracket)
        ch_question = await ctx.guild.create_text_channel("Questions", category=category)
        ch_results  = await ctx.guild.create_text_channel("Match Results", category=category)
        # set channel perms
        await ch_info.set_permissions(ow_info)
        await ctx.author.send("Tournament got set up.")


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Tournament(bot))
