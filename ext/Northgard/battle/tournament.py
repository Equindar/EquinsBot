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


    # show_tournament(): async
    @tournament.command(name="show", hidden=True)
    async def show_tournament(self, ctx, *, name: str):
        """display a Tournament"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            async with db.execute("""
                SELECT participant.Position, team.Name, AVG(player.Points),
                       COUNT(teamplayer.PlayerID), team.StatusID, status.Value
                FROM team
                LEFT JOIN teamplayer ON team.TeamID = teamplayer.TeamID
                LEFT JOIN participant ON participant.TeamID = team.TeamID
                LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                LEFT JOIN status ON participant.StatusID = status.StatusID
                LEFT JOIN tournament ON tournament.TournamentID = participant.TournamentID
                WHERE tournament.Name = ?
                GROUP BY team.TeamID
                ORDER BY participant.Position ASC;""", (name,)) as cursor:

                part_team = ""
                part_pts = ""
                part_stati = ""
                back_team = ""
                back_pts = ""
                back_stati = ""
                counter = 0
                async for result in cursor:
                    # data manipulation: db result (tuple)
                    if counter < 16:
                        if result[5] == 'confirmed':
                            part_stati += "`✔️` "
                        elif result[5] == 'failed':
                            part_stati += "`❌` "
                        else:
                            part_stati += "\u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b"
                        part_team += f"`#{result[0]:>2}` {result[1]} \u200b \u200b \u200b\n"
                        part_pts += f"{result[2]} pts \u200b \n"
                        part_stati += f"{result[5]}\n"
                    else:
                        if result[5] == 'confirmed':
                            back_stati += "`✔️` "
                        elif result[5] == 'failed':
                            back_stati += "`❌` "
                        else:
                            back_stati += "\u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b"
                        back_team += f"`#{result[0]:>2}` {result[1]} \u200b \u200b \u200b\n"
                        back_pts += f"{result[2]} pts \u200b \n"
                        back_stati += f"{result[5]}\n"
                    counter += 1
        # generate embed
        embed = discord.Embed(title=f"__{name}__",
                              description=f"List of all joined Teams",
                              colour=discord.Colour.dark_red(),
                              timestamp = datetime.now())
        embed.set_footer(text="--- List: sorted by Position --- ||")
        if not part_team:
            embed.add_field(name="Participants", value="no teams listed here.", inline=False)
        else:
            embed.add_field(name="`Pos` Participants", value=part_team, inline=True)
            embed.add_field(name="Points", value=part_pts, inline=True)
            embed.add_field(name="Confirmation", value=part_stati, inline=True)
        if not back_team:
            embed.add_field(name="Backup-Queue", value="no teams listed here.", inline=False)
        else:
            embed.add_field(name="`Pos` Backup-Queue", value=back_team, inline=True)
            embed.add_field(name="Points", value=back_pts, inline=True)
            embed.add_field(name="Confirmation", value=back_stati, inline=True)
        await ctx.send(embed=embed)


    # preview_tournament(): async
    @tournament.command(name="preview", hidden=True)
    async def preview_tournament(self, ctx):
        """display a Confirmation Preview of a Tournament"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            async with db.execute("""
                SELECT participant.Position, team.Name, teamplayer.RoleID, player.Name, player.Steam
                FROM team
                LEFT JOIN teamplayer ON team.TeamID = teamplayer.TeamID
                LEFT JOIN participant ON participant.TeamID = team.TeamID
                LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                LEFT JOIN status ON participant.StatusID = status.StatusID
                LEFT JOIN tournament ON tournament.TournamentID = participant.TournamentID
                WHERE tournament.TournamentID = 2 AND participant.StatusID = 8
                ORDER BY participant.Position ASC;""") as cursor:

                team = { }
                members = ""
                counter = 0
                output = []
                async for result in cursor:
                    if result[1] not in team.keys():
                        team[result[1]] = []
                    if result[2] == 2:
                        member= f"Leader: *{result[3]}*"
                    if result[2] == 3:
                        member = f"Member: {result[3]}"
                    if result[2] == 4:
                        member = f"Substitute: {result[3]}"
                    team[result[1]].append(member)

        # generate embed
        embed = discord.Embed(title=f"__Details: **Bloody January 2019**__",
                              description=f"All Participants of Bloody January 2019",
                              colour=discord.Colour.dark_red(),
                              timestamp = datetime.now())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format='png', size=512))
        embed.set_footer(text=f"--- Tournament: Bloody January 2019 --- ||")
        for k, v in team.items():
            embed.add_field(name=k, value="\n".join(v), inline=True)
        await ctx.send(embed=embed)


    # join_tournament(): async
    @tournament.command(name="join")
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
                    WHERE teamplayer.RoleID = 2 AND player.Name = ?;""", (ctx.author.name,))
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
                            SELECT team.TeamID, participant.Position, tournament.TeamLimit
                            FROM participant
                            LEFT JOIN team ON team.TeamID = participant.TeamID
                            LEFT JOIN tournament ON tournament.TournamentID = participant.TournamentID
                            WHERE participant.TournamentID = ?""", (dict[reply.content],)) as cursor:
                            counter = 0
                            async for result in cursor:
                                if result[0] == team[0]:
                                    return await ctx.author.send(f"Your Team '{team[1]}' already joined '{reply.content}'")
                                position = result[1]
                                limit = result[2]
                                counter += 1

                        if counter <= limit:
                            # push to Participant
                            await db.execute("""
                                INSERT INTO participant (ParticipantTypeID, TournamentID, TeamID, Position)
                                VALUES (1, ?, ?, ?)""", (dict[reply.content], team[0], position + 1))
                            await db.commit()
                            await self.team_joined(ctx, pos = counter + 1, team_id = team[0])
                            return await ctx.author.send(f"Your Team '{team[1]}' **successfully joined** '{reply.content}'")
                        else:
                            # push to BackupQueue
                            await db.execute("""
                                INSERT INTO participant (ParticipantTypeID, TournamentID, TeamID, Position)
                                VALUES (2, ?, ?, ?)""", (dict[reply.content], team[0], position + 1))
                            await db.commit()
                            await self.team_joined(ctx, pos = counter + 1, team_id = team[0])
                            return await ctx.author.send(
                                f"""Your Team '{team[1]}' **successfully joined** '{tournament[1]}'
                                \nYou entered the BackupQueue at Position #{(counter + 1) - limit}""")
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
                SELECT discord.InternalID, player.Name, teamplayer.RoleID, team.Name, participant.Position
                FROM teamplayer
                LEFT JOIN discord ON discord.ReferenceID = teamplayer.PlayerID
                LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                LEFT JOIN team ON team.TeamID = teamplayer.TeamID
				LEFT JOIN participant ON participant.TeamID = team.TeamID
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
        for item in server.categories:
            if item.id == 519174714002898984:
                category = item
        perms = {   team: discord.PermissionOverwrite(read_messages=True, connect=True, speak=True),
                    server.get_role(self.staff): discord.PermissionOverwrite(read_messages=True, connect=True, speak=True),
                    server.get_role(self.participant): discord.PermissionOverwrite(read_messages=False),
                    server.get_role(self.backQueue): discord.PermissionOverwrite(read_messages=False),
                    server.default_role: discord.PermissionOverwrite(read_messages=False, connect=False)
        }
        team_ch = await server.create_voice_channel(f"[#{result[4]}] {result[3]}", category=category, overwrites=perms)
        if pos <= 16:
            desc = f"`✔️` Team **{result[3]}** joined the Tournament."
        else:
            desc = f"`✔️` Team **{result[3]}** joined the Tournament\nIt got set to the BackupQueue (Position: #{pos-16})."
        embed = discord.Embed(description=desc,colour=discord.Colour.dark_green(), timestamp = datetime.now())
        embed.set_footer(text="--- Tournament: Bloody January 2019 --- ||")
        return await server.get_channel(537581556202733568).send(embed=embed)


    # confirm_tournament(): async
    @tournament.command(name="confirm", hidden=True)
    @commands.is_owner()
    async def confirm_tournament(self, ctx):
        alerts = {
            1: "We are so silent? - Yeah, no warcry for unworthy opponents...",
            2: ""
        }
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            # check: list active tournament
            cursor = await db.execute("""
                SELECT player.PlayerID, team.TeamID, team.Name, teamplayer.RoleID,
                    participant.TournamentID, participant.ParticipantID, participant.StatusID
                FROM player
                LEFT JOIN teamplayer ON teamplayer.PlayerID = player.PlayerID
                LEFT JOIN team ON team.TeamID = teamplayer.TeamID
                LEFT JOIN participant ON participant.TeamID = team.TeamID
                WHERE player.Name = ?;""", (ctx.author.name,))
            player = await cursor.fetchone()
            await cursor.close()
            # check: in Team and Team Leader?
            if player is not None:
                if player[1] is not None:
                    if player[3] == 2:
                        if player[4] is not None:
                            if player[6] != 8:
                                issues = { }
                                cursor = await db.execute("""
                                    SELECT player.Name, player.StatusID, team.Name, team.StatusID
                                    FROM player
                                    LEFT JOIN teamplayer ON teamplayer.PlayerID = player.PlayerID
                                    LEFT JOIN team ON team.TeamID = teamplayer.TeamID
                                    WHERE team.TeamID = ?""", (player[1],))
                                team = await cursor.fetchall()
                                await cursor.close()
                                counter = 0
                                print(team)
                                for member in team:
                                    print(member)
                                    if member[1] != 2:
                                        issues[f"Member '{member[0]}'"] = "not verified"
                                    counter += 1
                                if team[0][3] != 2:
                                    issues[f"Team '{team[0][2]}'"] = "not verified"

                                if not issues and counter >= 2:
                                    await db.execute("""
                                        UPDATE participant
                                        SET StatusID = 8
                                        WHERE ParticipantID = ?""", (player[5],))
                                    await db.commit()
                                    await ctx.author.send("You have **successfully confirmed** your Team.")
                                    desc = f"`✔️` Team **{player[2]}** confirmed its Tournament participation."
                                    embed = discord.Embed(description=desc,colour=discord.Colour.dark_green(), timestamp = datetime.now())
                                    embed.set_footer(text="--- Tournament: Bloody January 2019 --- ||")
                                    return await self.bot.get_guild(self.bot.northgardbattle).get_channel(537581556202733568).send(embed=embed)

                                else:
                                    output = ""
                                    for k, v in issues.items():
                                        output += f"{k}: {v}\n"
                                    return await ctx.author.send(f"You **cannot complete** the Team Confirmation.\n__Issues:__\n{output}")
                            else:
                                return await ctx.author.send("You already confirmed your Team.")
                        else:
                            return await ctx.author.send("Your Team hasnt joined an active Tournament")
                    else:
                        return await ctx.author.send("You are not the Team Leader.")
                else:
                    return await ctx.author.send("You are not in a Team.")
            else:
                await ctx.author.send("You dont have a registered Player profile.")


    # leave_tournament(): async
    @tournament.command(name="leave")
    async def leave_tournament(self, ctx):
        """join an active Tournament"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            # check: list active tournament
            cursor = await db.execute("""
                SELECT participant.ParticipantID, team.Name, tournament.Name, team.TeamID
                FROM participant
                LEFT JOIN tournament ON tournament.TournamentID = participant.TournamentID
                LEFT JOIN team ON team.TeamID = participant.TeamID
                LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                WHERE teamplayer.RoleID = 2 AND player.Name = ?;""", (ctx.author.name,))
            participant = await cursor.fetchone()
            await cursor.close()
            if participant is not None:
                await ctx.author.send(f"""Are you sure, your Team want to leave '{participant[2]}'?
                    \nThis action cannot be reverted.\nType `leave` to confirm...""")
                def check(msg):
                    return msg.content == 'leave' and msg.channel == ctx.author.dm_channel
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=10.0)
                except asyncio.TimeoutError:
                    await ctx.author.send("Your Tournament-Leave request (10sec) timed out. Retry...")
                else:
                    await self.team_left(ctx, team_id = participant[3])
                    await db.execute("DELETE FROM participant WHERE participant.ParticipantID = ?", (participant[0],))
                    await db.commit()
                    await ctx.author.send(f"Your Team '{participant[1]}' **successfully left** the Tournament.")
                    desc = f"`❌` Team **{participant[1]}** left the Tournament."
                    embed = discord.Embed(description=desc,colour=discord.Colour.red(), timestamp = datetime.now())
                    embed.set_footer(text="--- Tournament: Bloody January 2019 --- ||")
                    return await self.bot.get_guild(self.bot.northgardbattle).get_channel(537581556202733568).send(embed=embed)
            else:
                await ctx.author.send("""You **cannot leave** the tournament.
                    \n__Reasons can be:__\nYou are not in a Tournament.\nYou are not the Team Leader.""")


    async def team_left(self, ctx, team_id: int):
        """DISCORD WORKFLOW"""
        server = self.bot.get_guild(self.bot.northgardbattle)
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            async with db.execute("""
                SELECT discord.InternalID, player.Name, teamplayer.RoleID, team.Name
                FROM player
                LEFT JOIN teamplayer ON teamplayer.PlayerID = player.PlayerID
                LEFT JOIN team ON team.TeamID = teamplayer.TeamID
                LEFT JOIN discord ON discord.ReferenceID = player.PlayerID
                WHERE discord.Reference = 'Player' AND team.TeamID = ?""", (team_id,)) as cursor:
                async for result in cursor:
                    member = server.get_member(result[0])
                    if server.get_role(self.participant) in member.roles:
                        await member.remove_roles(server.get_role(self.participant))
                    if server.get_role(self.backQueue) in member.roles:
                        await member.remove_roles(server.get_role(self.backQueue))

                    for item in member.roles:
                        if item.name == f"Team: {result[3]}":
                            await member.remove_roles(server.get_role(item.id))

                for item in server.voice_channels:
                    if item.name[6:] == result[3]:
                        await server.get_channel(item.id).delete()


    # set_date(): async
    @tournament.command(name="date")
    @commands.is_owner()
    async def set_date(self, date: datetime):
        self.date = date
        print(type(self.date))
        print(self.date)


    # deadline(): async
    @commands.command()
    @commands.is_owner()
    async def all_deadline(self, ctx):
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
        embed = discord.Embed(colour=3158584, timestamp = date - timedelta(hours=1))
        embed.add_field(name='Tournament: **Bloody February 2019** starting in...',
                        value=f":stopwatch: {x}\n \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b`\u200b DAYS \u200b` \u200b \u200b `\u200b HOURS ` \u200b \u200b \u200b `\u200b MINS \u200b` \u200b \u200b `\u200b SECS \u200b`")
        await ctx.send(content="Last Minute Tournament Check in? @everyone", embed=embed)


    # deadline(): async
    @commands.command()
    async def deadline(self, ctx):
        """[DEV] Deadline Display"""
        emoji = {
            0:':zero:', 1:':one:', 2:':two:', 3:':three:', 4:':four:',
            5:":five:", 6:":six:", 7:":seven:", 8:":eight:", 9:":nine:"
        }
        now = datetime.now()
        date = datetime(2019,2,23,12,0,0)
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
        embed = discord.Embed(colour=3158584, timestamp = date - timedelta(hours=1))
        embed.add_field(name='Tournament: **Bloody February 2019** starting in...',
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
        ch_lft      = await ctx.guild.create_text_channel("Looking for Team", category=category)
        ch_question = await ctx.guild.create_text_channel("Questions", category=category)
        ch_results  = await ctx.guild.create_text_channel("Match Results", category=category)
        # set channel perms
        await ch_info.set_permissions(ow_info)
        await ch_lft.set_permissions({ ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True) })
        await ctx.author.send("Tournament got set up.")


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Tournament(bot))
