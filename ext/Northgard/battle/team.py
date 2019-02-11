# --- imports
import discord
import aiosqlite
from datetime import datetime
from discord.ext import commands
from ...codegen import CodeGen

class Team:
    # --- attributs

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot


    # myteam(): async
    @commands.command(name = "myteam")
    async def myteam(self, ctx):
        """display your Team profile"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("""
                SELECT team.Name
                FROM team
                LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                WHERE player.Name = ?;""", (ctx.author.name,))
            result = await cursor.fetchone()
            await cursor.close()
        if result is not None:
            await ctx.invoke(self.show_team, name = result[0])
        else:
            await ctx.author.send("You are not part of a Team")


    # team(): async
    @commands.group()
    async def team(self, ctx):
        """manage your Team"""
        if ctx.invoked_subcommand is None:
            await ctx.send("No param...")


    # show_team(): async
    @team.command(name="show")
    async def show_team(self, ctx, *, name: str):
        """display a Team profile"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            roster = ""
            points = 0
            members = 0
            cursor = await db.execute("""
                SELECT
                    team.Name, team.Description, role.Name, player.Name, player.Steam,
                    player.Points, team.TeamID, team.Registration, status.Value
                FROM team
                LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                LEFT JOIN role ON role.RoleID = teamplayer.RoleID
                LEFT JOIN player ON teamplayer.PlayerID = player.PlayerID
                LEFT JOIN status ON status.StatusID = team.StatusID
                WHERE team.name = ?
                ORDER BY role.RoleID ASC;""", (name,))
            team = await cursor.fetchall()
            await cursor.close()

            # data manipulation: db result (tuple)
            if team:
                for member in team:
                    name = ""
                    if member[3] is not None:
                        if member[4] is not None:
                            name = f"[{member[3]}]({member[4]})"
                        else:
                            name = member[3]
                        if member[2][5:] == "Substitute":
                            roster += f"`{member[2][5:]}:` {name}\n"
                        elif member[2][5:] == "Manager":
                            roster += f"`{member[2][5:]} \u200b \u200b \u200b:` {name}\n"
                        else:
                            roster += f"`{member[2][5:]} \u200b \u200b \u200b \u200b:` {name}\n"
                        points += member[5]
                        members += 1
                    else:
                        roster = "no players assigned"
                        # avoid div by zero
                        members = 1
                if team[0][1] is None:
                    desc = "no team description yet..."
                else:
                    desc = team[0][1]

                embed = discord.Embed(title=f"__{team[0][0]}__",description=desc,colour=6809006)
                embed.set_thumbnail(url = "https://gamepedia.cursecdn.com/northgard_gamepedia_en/d/d4/Tactician_icon.png")
                embed.set_footer(text=f"--- Team-ID: #{team[0][6]} --- || --- Registered: {team[0][7][:-7]} --- || --- Status: {team[0][8]} ---")
                embed.add_field(name="Team Roster", value=roster, inline=True)
                embed.add_field(name="Performance", value='**--- %.2f pts ---**' % (points / members), inline=True)
                # Match History: `W 📈 +10 pts` -vs- `Team: Frostbite`\n`L 📉 -14 pts` -vs- `Team: Set in Stone`\n`W 📈 + 8 pts` -vs- `Team: Pinar`\n`W 📈 +24 pts` -vs- `Team: chip n dale`
                embed.add_field(name="Match History (latest 5)", value="feature coming soon...", inline=False)
                return await ctx.author.send(content=f"used Feature: NorthgardBattle `{ctx.message.content}`", embed=embed)
            else:
                await ctx.author.send(f"Team '{name}' not found.")





    # list_teams(): async
    @team.command(name="list")
    async def list_teams(self, ctx, page: int = 1):
        """list all registered Teams"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            async with db.execute("""
                SELECT
                    team.TeamID, player.Points, team.Name, player.Name, player.Steam,
                    team.Registration, status.Value
                FROM team
                LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                LEFT JOIN role ON role.RoleID = teamplayer.RoleID
                LEFT JOIN player ON teamplayer.PlayerID = player.PlayerID
                LEFT JOIN status ON status.StatusID = team.StatusID
                WHERE role.RoleID == 2 OR role.RoleID IS NULL
                GROUP BY team.TeamID
                ORDER BY team.TeamID ASC
                LIMIT ?, 15;""", ((page-1) * 15,)) as cursor:
                teamname = ""
                leaders = ""
                async for result in cursor:
                    # data manipulation: db result (tuple)
                    if result[1] is None:
                        pts = 0
                    else:
                        pts = result[1]
                    if result[3] is not None:
                        if result[4] is not None:
                            leaders += f"[{result[3]}]({result[4]})"
                        else:
                            leaders += result[3]
                    else:
                        leaders += "`no leader`"
                    leaders += "\n"
                    teamname += f"`#{result[0]:>2}` {result[2]} \u200b \u200b \u200b\n"
        # generate embed
        embed = discord.Embed(title="__Team List__",
                              description=f"List of all registered teams in Northgard Battle\n \nPage: {page}",
                              colour=6809006,
                              timestamp = datetime.now())
        embed.set_footer(text="--- List: sorted by TeamID --- ||")
        if not teamname:
            embed.add_field(name="Team", value="no teams listed here.", inline=True)
        else:
            embed.add_field(name="Team", value=teamname, inline=True)
            embed.add_field(name="Leader", value=leaders, inline=True)
        await ctx.author.send(content=f"used Feature: NorthgardBattle `{ctx.message.content}`", embed=embed)


    # register_team(): async
    @team.command(name="register")
    async def register_team(self, ctx, *, name: str):
        """register your Team profile"""
        name = name.strip()
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("""
                SELECT player.PlayerID, player.StatusID, teamplayer.TeamID
                FROM player
                LEFT JOIN teamplayer ON teamplayer.PlayerID = player.PlayerID
                WHERE player.Name = ?;""", (ctx.author.name,))
            player = await cursor.fetchone()
            await cursor.close()
            # check: is player registered?
            if player is not None:
                # check: has no team?
                if player[2] == None:
                    # check: is verified player?
                    if player[1] == 2:
                        cursor = await db.execute("SELECT TeamID FROM team WHERE Name = ?;", (name,))
                        team = await cursor.fetchone()
                        await cursor.close()
                        if team is None:
                            await db.execute("""
                                INSERT INTO team (Name, Registration)
                                VALUES (?, ?);""", (name, str(datetime.now())))
                            await db.commit()
                            await db.execute("""
                                INSERT INTO teamplayer (TeamID, PlayerID, RoleID)
                                SELECT TeamID, ?, 2
                                FROM team
                                WHERE Name = ?;""", (player[0], name))
                            await db.commit()
                            return await ctx.send(f"{ctx.author.mention} successfully registered the Team '{name}'")
                        else:
                            return await ctx.author.send(f"Team '{name}' is already registered, use a unique team name.")
                    else:
                        return await ctx.author.send(f"Your Player Profile '{ctx.author.name}' isnt 'verified' yet.")
                else:
                    return await ctx.author.send("You are already part of a Team.")
            else:
                await ctx.author.send("""
                    Only verfied players can register teams.\n
                    Use: `!register` to create your player profile.\n
                    After your Status became 'verified', try again.""")


    # add_team(): async
    @team.command(name="add", hidden=True)
    @commands.is_owner()
    async def add_team(self, ctx, *, name: str):
        """add a Team"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            await db.execute("""
                INSERT INTO team (Name, Registration, StatusID)
                VALUES (?, ?, 1);""", (name, str(datetime.now())))
            await db.commit()
        await ctx.send(f"Team '{name}' got **sucessfully added**.")


    # verify_team(): async
    @team.command(name="verify", hidden=True)
    @commands.has_role(519421170517540864)
    async def verify_team(self, ctx, *, name: str):
        """verify a Team"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("""
                SELECT TeamID, StatusID
                FROM team
                WHERE team.Name = ?""", (name,))
            team = await cursor.fetchone()
            await cursor.close()
            if team is not None:
                if team[1] != 2:
                    cursor = await db.execute("""
                        SELECT player.Name, status.Value, discord.InternalID, teamplayer.RoleID
                        FROM player
                        LEFT JOIN teamplayer ON teamplayer.PlayerID = player.PlayerID
                        LEFT JOIN team ON team.TeamID = teamplayer.TeamID
                        LEFT JOIN status ON status.StatusID = player.StatusID
                        LEFT JOIN discord ON discord.ReferenceID = player.PlayerID
                        WHERE discord.Reference = "Player" AND team.teamID = ?;""", (team[0],))
                    players = await cursor.fetchall()
                    await cursor.close()
                    issues = { }
                    for item in players:
                        if item[1] != "verified":
                            issues[item[0]] = item[1]
                        if item[3] == 2:
                            leader_id = item[2]
                    if not issues:
                        await db.execute("UPDATE team SET StatusID = 2 WHERE TeamID = ?;", (team[0],))
                        await db.commit()
                        desc = f"Your Team **{name}** got verified by {ctx.author.name}"
                        embed = discord.Embed(description=desc,
                            colour=discord.Colour.green(), timestamp = datetime.now())
                        embed.set_footer(text="--- NorthgardBattle: Team Notification --- ||")
                        await self.bot.get_guild(self.bot.northgardbattle).get_member(leader_id).send(embed=embed)
                        await ctx.author.send(f"Team '{name}' got **verified**.")
                    else:
                        await ctx.author.send(f"Team '{name}' cannot be verified.\nPlayer Status: `{str(issues)}`")
                else:
                    await ctx.author.send(f"Team '{name}' is already **verified**.")
            else:
                await ctx.author.send(f"Team '{name}' not found.")


    # invite_to_team(): async
    @team.command(name="invite")
    async def invite_to_team(self, ctx, type: str = "Member"):
        """create an Invite Code for your Team"""
        dict = { "manager": 1, "member": 3, "substitute": 4 }
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("""
                SELECT PlayerID
                FROM player
                WHERE StatusID = 2 AND Name = ?;""", (ctx.author.name,))
            player = await cursor.fetchone()
            await cursor.close()
            # check: is player registered and verified?
            if player is not None:
                cursor = await db.execute("""
                    SELECT RoleID
                    FROM teamplayer
                    WHERE RoleID = 2 AND PlayerID = ?;""", (player[0],))
                leader = await cursor.fetchone()
                await cursor.close()
                # check: is player leader?
                if leader is not None:
                    if type.lower() in dict:
                        roleID = dict[type.lower()]
                        code = CodeGen.generate(CodeGen,3,4,1)
                        await db.execute("""
                            INSERT INTO codes (TeamID, Value, RoleID, Date)
                            SELECT team.teamID, ?, ?, datetime()
                            FROM team
                            LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                            LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                            WHERE player.Name = ? AND teamplayer.RoleID = 2;""", (code[0], roleID, ctx.author.name))
                        await db.commit()
                        embed = discord.Embed(title=f"Invite Code for __Team {type.lower().capitalize()}__",
                                              description=f"{code[0]}\n```\n!team join {code[0]}\n```",
                                              colour=3158584)
                        await ctx.author.send(content=f"used Feature: NorthgardBattle `{ctx.message.content}`", embed=embed)
                    else:
                        return await ctx.author.send(
                            f"{type} is not a valid Team role, only `Manager`, `Member` and `Substitute` is allowed.")
                else:
                    return await ctx.author.send("You are not in a Team or not the Leader of the Team.")
            else:
                await ctx.author.send(
                    """You dont have a __verified__, registered Player profile.\n
                    Use: `!register` to register yourself.\n
                    Use: `!me` to check your 'verified'-Status.""")


    # join_team(): async
    @team.command(name="join")
    async def join_team(self, ctx, code: str):
        """join a Team with an Invite Code"""
        # code valid? (14 chars)
        if len(code) == 14:
            async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
                # check: is code in database
                cursor = await db.execute("SELECT CodeID FROM codes WHERE Value = ?", ( code, ))
                data = await cursor.fetchone()
                await cursor.close()
                # code valid? (in database)
                if data is not None:
                    # check: registered player
                    cursor = await db.execute("SELECT PlayerID FROM player WHERE Name = ?", ( ctx.author.name, ))
                    player = await cursor.fetchone()
                    await cursor.close()
                    # code valid! player registered?
                    if player is not None:
                        # check team member IDs based on TeamID from Code
                        cursor = await db.execute("""
                            SELECT teamplayer.PlayerID
                            FROM codes
                            LEFT JOIN teamplayer ON teamplayer.TeamID = codes.TeamID
                            WHERE codes.Value = ?""", (code,))
                        team = await cursor.fetchall()
                        await cursor.close()
                        inteam = False
                        for member in team:
                            if player[0] in member:
                                inteam = True
                        # code valid! player registered! player not in Team?
                        if not inteam:
                            cursor = await db.execute("""
                                SELECT codes.TeamID, codes.RoleID, team.Name, role.Name
                                FROM codes
                                LEFT JOIN team ON team.TeamID = codes.TeamID
                                LEFT JOIN role ON role.RoleID = codes.RoleID
                                WHERE codes.Value =  ?""", (code,))
                            result = await cursor.fetchone()
                            await cursor.close()
                            await db.execute("""
                                INSERT INTO teamplayer (TeamID, PlayerID, RoleID)
                                VALUES (?, ?, ?);""", (result[0], player[0], result[1]))
                            await db.execute("DELETE FROM codes WHERE CodeID = ?;", (data[0],))
                            await db.commit()
                            return await ctx.author.send(
                                f"""Code `{code}` successfully redeemed...\n
                                {ctx.author.mention} joined **{result[2]}** as a *{result[3]}*.""")
                        # code valid! User in Team
                        else:
                            return await ctx.author.send("You are already in the Team.")
                    else:
                        return await ctx.author.send(
                            """Only registered players can join teams.\n
                            Use: `!register` to create your player profile.""")
                else:
                    return await ctx.author.send(f"Code `{code}` is invalid.")
        else:
            await ctx.author.send(f"Code `{code}` is not a proper code (length: 14 characters)")


    # claim_team(): async
    @team.command(name="claim")
    async def claim_team(self, ctx, *, name: str):
        """claim your leaderless Team (become the Leader)"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("""
                SELECT teamplayer.RoleID, player.Name, team.TeamID, player.PlayerID
                FROM team
                LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                WHERE team.Name = ?;""", (name,))
            result = await cursor.fetchall()
            for item in result:
                if ctx.author.name in item:
                    if item[0] != 2:
                        await db.execute("""
                            UPDATE teamplayer
                            SET RoleID = 2
                            WHERE TeamID = ? AND PlayerID = ?;""", (item[2], item[3]))
                        await db.commit()
                        return await ctx.send(f"{ctx.author.name} became the **Team Leader** of '{name}'.")


    # assign_player(): async
    @team.command(name="assign")
    async def assign_player(self, ctx, role: str, *, name: str):
        """assign a Team member to a role"""
        dict = { "manager": 1, "member": 3, "substitute": 4 }
        if role.lower() in dict:
            async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
                cursor = await db.execute("""
                    SELECT teamplayer.TeamID
                    FROM teamplayer
                    LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                    WHERE teamplayer.RoleID = 2 AND player.Name = ?;""", (ctx.author.name,))
                teamID = await cursor.fetchone()
                await cursor.close()
                # check: leader?
                if teamID is not None:
                    cursor = await db.execute("""
                        SELECT teamplayer.TeamPlayerID
                        FROM team
                        LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                        LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                        LEFT JOIN role ON role.RoleID = teamplayer.RoleID
                        WHERE team.TeamID = ? AND player.Name = ?""", (teamID[0], name))
                    result = await cursor.fetchone()
                    await cursor.close()
                    if result is not None:
                        await db.execute("""
                            UPDATE teamplayer
                            SET RoleID = ?
                            WHERE TeamPlayerID = ?;""", (dict[role.lower()], result[0]))
                        await db.commit()
                        return await ctx.author.send(f"{name} became **Team {role.lower().capitalize()}** of the team.")
                    else:
                        return await ctx.author.send(f"{name} is not a part of the Team.")
                else:
                    return await ctx.author.send("You are not a Team Leader.")
        else:
            await ctx.author.send(f"{role} is not a valid Team role, only `Manager`, `Member` and `Substitute` is allowed.")


    # set_teamdata(): async
    @team.command(name="set")
    async def set_teamdata(self, ctx, subject: str, *, data: str):
        """set Data for your Team profile"""
        args = ["description", "name"]
        if subject.lower() in args:
            async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
                if subject.lower() == "description":
                    await db.execute("""
                        UPDATE team
                        SET Description = ?
                        WHERE team.TeamID =
                            (SELECT team.TeamID
                             FROM team
                             LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                             LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                             WHERE player.Name = ? AND teamplayer.RoleID = 2);""", (data, ctx.author.name))
                if subject.lower() == "name":
                    await db.execute("""
                        UPDATE team
                        SET Name = ?
                        WHERE team.TeamID =
                            (SELECT team.TeamID
                             FROM team
                             LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                             LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                             WHERE player.Name = ? AND teamplayer.RoleID = 2);""", (data, ctx.author.name))
                    await db.execute("""
                        UPDATE team
                        SET StatusID = 1
                        WHERE team.TeamID =
                            (SELECT team.TeamID
                             FROM team
                             LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                             LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                             WHERE player.Name = ? AND teamplayer.RoleID = 2);""", (ctx.author.name,))
                await db.commit()
            await ctx.author.send(f"Your Team-Data '{subject}' got set to `{data}`")


    # leave_team(): async
    @team.command(name="leave")
    async def leave_team(self, ctx):
        """leave your Team"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            await db.execute("""
                DELETE FROM teamplayer
                WHERE teamplayer.PlayerID =
                    (SELECT player.PlayerID
                     FROM player
                     WHERE player.Name = ?);""", (ctx.author.name,))
            await db.commit()
        await ctx.author.send("You have successfully left the team.")


    # disband_team(): async
    @team.command(name="disband", hidden=True)
    @commands.guild_only()
    async def disband_team(self, ctx):
        """disband the Team"""
        #TO-DO: check for invoker in a team
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("""
                SELECT team.teamID
                FROM team
                LEFT JOIN teamplayer ON teamplayer.TeamID = team.TeamID
                LEFT JOIN player ON player.PlayerID = teamplayer.PlayerID
                WHERE player.Name = ? AND teamplayer.RoleID = 2;""", (ctx.author.name,))
            team = await cursor.fetchone()
            await cursor.close()
            if team is not None:
                await ctx.send(
                    """Are you sure, you want to disband your Team?\n
                    This action cannot be reverted.\n
                    Type `disband` to confirm...""")

                def check(msg):
                    return msg.content == 'disband' and msg.channel == ctx.channel

                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=10.0)
                except asyncio.TimeoutError:
                    await ctx.send("Your Team-Disband request (10sec) timed out. Retry...")
                else:
                    await db.execute("DELETE FROM teamplayer WHERE teamID = ? ;", (team[0],))
                    await db.execute("DELETE FROM team WHERE teamID = ? ;", (team[0],))
                    await db.commit()
                    return await ctx.send("You successfully disbanded your Team")
            else:
                await ctx.send("You are not in a Team.")


    # delete_team(): async
    @team.command(name="delete", hidden=True)
    @commands.is_owner()
    async def delete_team(self, ctx, *, name: str):
        """delete a Team"""
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            cursor = await db.execute("SELECT TeamID FROM team WHERE Name = ?;", (name,))
            team = await cursor.fetchone()
            await cursor.close()
            if team is not None:
                await db.execute("DELETE FROM team WHERE TeamID = ?;", (team[0],))
                await db.commit()
                return await ctx.send(f"Team {name} got successfully deleted.")
            else:
                await ctx.send(f"Team {name} not found.")


    # [DEV] dummy(): async
    @team.command(name="dummy", hidden=True)
    async def dummy_team(self, ctx):
        """[DEV] Team Dummy"""
        embed = discord.Embed(title='__Blood Eagle Selfie__',description='bla bla bla, custom description, bla bla blubb, bla bla bla, custom description, bla bla blubb, bla bla bla, custom description, bla bla blubb, bla bla bla, custom description, bla bla blubb!',colour=6809006)
        embed.set_thumbnail(url = "https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/d/d4/Tactician_icon.png")
        embed.set_footer(text='--- Team-ID: #3 --- || --- Registered: 2018-12-04 --- || --- Status: verified ---')
        embed.add_field(name='Team Roster', value='`Leader    :` [Piratenhut](http://google.de)\n`Member(s) :` [DerAndreas](http://google.de)\n`Substitute:` [Equindar](http://google.de)', inline = True)
        embed.add_field(name='Performance', value='**--- 2570 pts ---**\n100% Winrate\n*2 Matches played*', inline = True)
        await ctx.send(content='used Feature: NorthgardBattle `' + ctx.message.content + '`', embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(Team(bot))
