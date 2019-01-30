# --- imports
import discord
import asyncio
import aiosqlite
from discord.ext import commands
from datetime import datetime


class DEV:
    # --- attributs
    staff = 519421170517540864
    participant = 519421297235853313
    backQueue = 521693581589741573

    server = {
        "Equindar": 509301003376525314,
        "NorthgardBattle": 486105985782644736
    }

    # --- methods
    # constructor
    def __init__(self, bot):
        self.bot = bot


    # info(): async
    @commands.group(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def info(self, ctx):
        """display information"""
        if ctx.invoked_subcommand is None:
            await ctx.send("No param...")


    # server_info(): async
    @info.command(name="server", hidden=True)
    async def server_info(self, ctx):
        """display server information"""
        s = ctx.guild
        data = ""
        value = ""
        dict = {
            'Name': s.name,
            'ID': s.id,
            'Owner': f"{s.owner.name} [ID: {s.owner.id}]"
        }
        for k,v in dict.items():
            data += f"{k}\n"
            value += f"{v}\n"
        embed = discord.Embed(title=f"__{s.name}__",colour=3158584)
        embed.set_footer(text="--- Server information ---")
        embed.add_field(name="Data", value=data, inline=True)
        embed.add_field(name="Value", value=value, inline=True)
        await ctx.send(content=f"used `{ctx.message.content}`", embed=embed)


    # category_info(): async
    @info.command(name="category", hidden=True)
    async def category_info(self, ctx):
        """display category information"""
        name = ""
        id = ""
        for item in ctx.guild.categories:
            name += f"`#{item.position}` {item.name} \u200b \u200b \u200b\n"
            id += f"{item.id}\n"
        embed = discord.Embed(title=f"__{ctx.guild.name}__",colour=3158584)
        embed.set_footer(text="--- Category information ---")
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="ID", value=id, inline=True)
        await ctx.send(content=f"used `{ctx.message.content}`", embed=embed)


    # channel_info(): async
    @info.command(name="channel", hidden=True)
    async def channel_info(self, ctx, type: str = "text"):
        """display roles information"""
        name = ""
        id = ""
        for item in ctx.guild.channels:
            if type == "text":
                if isinstance(item, discord.TextChannel):
                    name += f"`#{item.position}` {item.name} \u200b \u200b \u200b\n"
                    id += f"{item.id}\n"
            else:
                if isinstance(item, discord.VoiceChannel):
                    name += f"`#{item.position}` {item.name} \u200b \u200b \u200b\n"
                    id += f"{item.id}\n"
        embed = discord.Embed(title=f"__{ctx.guild.name}__",colour=3158584)
        embed.set_footer(text="--- Channel information ---")
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="ID", value=id, inline=True)
        await ctx.send(content=f"used `{ctx.message.content}`", embed=embed)


    # roles_info(): async
    @info.command(name="roles", hidden=True)
    async def roles_info(self, ctx):
        """display roles information"""
        name = ""
        id = ""
        for item in ctx.guild.roles:
            name += "{} \u200b \u200b \u200b\n".format(item.name.replace("@","\@"))
            id += f"{item.id}\n"
        embed = discord.Embed(title=f"__{ctx.guild.name}__",colour=3158584)
        embed.set_footer(text="--- Role information ---")
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="ID", value=id, inline=True)
        await ctx.send(content=f"used `{ctx.message.content}`", embed=embed)


    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def test(self, ctx):
        """DEV function !test for testing"""

        # init
        server = self.bot.get_guild(self.bot.northgardbattle)
        for item in server.categories:
            if item.id == 519174714002898984:
                category = item
        print(category.name)

#        desc = f"`❗` Confirmation Phase is over.\nTeam participation confirmations got locked..."
#        embed = discord.Embed(description=desc,colour=discord.Colour.red(), timestamp = datetime.now())
#        embed.set_footer(text="--- Tournament: Bloody January 2019 --- ||")
#        return await self.bot.get_guild(self.bot.northgardbattle).get_channel(537581556202733568).send(embed=embed)

#        for member in ctx.guild.members:
#            if member.bot:
#                return await ctx.send(f"Found a freaking Bot: called {member.name}")
#        overwrites = {
#            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
#            ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
#        }
#        category = await ctx.guild.create_category_channel("Tournament Dummy", overwrites=overwrites)
#        await category.edit(position=1)
#        ch_info     = await ctx.guild.create_text_channel("Information", category=category)
#        ch_bracket  = await ctx.guild.create_text_channel("Bracket", category=category)
#        ch_question = await ctx.guild.create_text_channel("Questions", category=category)


#        overwrite = PermissionOverwrite(self.bot.get_guild(self.server).get_role(514423325049618460).permissions)
#        await category.set_permissions(self.bot.get_guild(self.server).get_role(514423325049618460), overwrite = overwrite)
#        print(category.id)
#        for item in self.bot.get_guild(self.server).categories:
#            if item.name == "Test":
#                print(item.id)

    # recover_team_channels(): async
    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def recover_team_channels(self, ctx):
        # init
        server = self.bot.get_guild(self.bot.northgardbattle)
        for item in server.categories:
            if item.id == 519174714002898984:
                category = item
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            async with db.execute("""
                SELECT participant.ParticipantTypeID, participant.Position, team.Name
                FROM participant
                LEFT JOIN team ON team.TeamID = participant.TeamID
                WHERE participant.TournamentID = 2
                ORDER BY participant.ParticipantID;""") as cursor:
                async for result in cursor:
                    team = None
                    flag = True
                    if team is None:
                        for item in server.roles:
                            if f"Team: {result[2]}" == item.name:
                                team = item
                                break
                    for channel in category.channels:
                        if f"[#{result[1]}] {result[2]}" == channel.name:
                            flag = False
                            break
                    if flag:
                        perms = {   team: discord.PermissionOverwrite(read_messages=True, connect=True, speak=True),
                            server.get_role(self.staff): discord.PermissionOverwrite(read_messages=True, connect=True, speak=True),
                            server.get_role(self.participant): discord.PermissionOverwrite(read_messages=False),
                            server.get_role(self.backQueue): discord.PermissionOverwrite(read_messages=False),
                            server.default_role: discord.PermissionOverwrite(read_messages=False, connect=False)
                        }
                        team_ch = await server.create_voice_channel(f"[#{result[1]}] {result[2]}", category=category, overwrites=perms)


    # recover_team_channels(): async
    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def delete_team_channels(self, ctx):
        # init
        server = self.bot.get_guild(self.bot.northgardbattle)
        for item in server.categories:
            if item.id == 519174714002898984:
                category = item
        for channel in category.channels:
            await channel.delete()
            await ctx.send(f"Channel {channel.name} deleted.")



    # recover_roles(): async
    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def recover_roles(self, ctx):
        # init:
        server = self.bot.get_guild(self.bot.northgardbattle)

        participant = server.get_role(519421297235853313)
        backQueue = server.get_role(521693581589741573)
        team_leader = server.get_role(519185793907032083)
        team_member = server.get_role(519422680647204873)
        team_sub = server.get_role(519433111478599690)

        rec_leader = []
        rec_member = []
        rec_sub = []
        rec_team = []
        rec_part = []
        rec_back = []
        users = { }
        async with aiosqlite.connect('./ext/Northgard/battle/data/battle-db.sqlite') as db:
            # check: list active tournament
            async with db.execute("""
                SELECT discord.InternalID, player.Name, teamplayer.RoleID, team.Name, participant.ParticipantTypeID
                FROM player
                LEFT JOIN discord ON discord.ReferenceID = player.PlayerID
                LEFT JOIN teamplayer ON teamplayer.PlayerID = player.PlayerID
                LEFT JOIN team ON team.TeamID = teamplayer.TeamID
                LEFT JOIN participant ON participant.TeamID = team.TeamID
                WHERE discord.Reference = "Player"
                ORDER BY player.PlayerID ASC;""") as cursor:
                async for result in cursor:
                    users[result[0]] = (result)
        for member in server.members:
            print(member.name)
            if member.id in users.keys():

                if team_leader not in member.roles:
                    if users[member.id][2] == 2:
                        rec_leader.append(member.name)
                        await member.add_roles(team_leader)
                if team_member not in member.roles:
                    if users[member.id][2] == 3:
                        rec_member.append(member.name)
                        await member.add_roles(team_member)
                if team_sub not in member.roles:
                    if users[member.id][2] == 4:
                        rec_sub.append(member.name)
                        await member.add_roles(team_sub)

                if participant not in member.roles:
                    if users[member.id][4] == 1:
                        rec_part.append(member.name)
                        await member.add_roles(participant)
                        for item in server.roles:
                            if f"Team: {users[member.id][3]}" == item.name:
                                team = item
                                rec_team.append(member.name)
                                await member.add_roles(team)
                                break

                if backQueue not in member.roles:
                    if users[member.id][4] == 2:
                        rec_back.append(member.name)
                        await member.add_roles(backQueue)
                        for item in server.roles:
                            if f"Team: {users[member.id][3]}" == item.name:
                                team = item
                                rec_team.append(member.name)
                                await member.add_roles(team)
                                break

        desc = f"`✔️` The following Users got their Roles recovered:"
        embed = discord.Embed(title = "__Role Recovery from Database__", description=desc,colour=discord.Colour.dark_green(), timestamp = datetime.now())
        embed.set_footer(text="--- EquinsBot --- || --- Data Recovery --- ||")
        if len(rec_leader) != 0:
            embed.add_field(name=f"Role: Team Leader ({len(rec_leader)})", value=", ".join(rec_leader), inline=False)
        if len(rec_member) != 0:
            embed.add_field(name=f"Role: Team Member ({len(rec_member)})", value=", ".join(rec_member), inline=False)
        if len(rec_sub) != 0:
            embed.add_field(name=f"Role: Team Substitute ({len(rec_sub)})", value=", ".join(rec_sub), inline=False)
        if len(rec_part) != 0:
            embed.add_field(name=f"Role: Participant ({len(rec_part)})", value=", ".join(rec_part), inline=False)
        if len(rec_back) != 0:
            embed.add_field(name=f"Role: BackupQueue ({len(rec_back)})", value=", ".join(rec_back), inline=False)
        if len(rec_team) != 0:
            embed.add_field(name=f"Team Roles ({len(rec_team)})", value=", ".join(rec_team), inline=False)
        return await server.get_channel(537553412041080833).send(embed=embed)


#        member = ctx.guild.get_member(ctx.message.author.id)
#        for role in member.roles:
#            if role.name != "@everyone":
#                await ctx.send(f"Role: {role.name} [ID: {role.id}]")


    @commands.command(hidden=True)
    async def bla(self, ctx):
        """bla test funtion"""
        str = "Leader"
        await ctx.send(f"`{str:<9}:`")


#@bot.command()
#async def liv(ctx):
#    embed=discord.Embed(title="Liv (Raven Clan)", url="https://northgard.gamepedia.com/Liv", description="The custom warchief of the Raven Clan", color=0xff0000)
#    embed.set_thumbnail(url="https://d1u5p3l4wpay3k.cloudfront.net/northgard_gamepedia_en/4/48/Liv-40x40.png")
#    embed.add_field(name="Health", value=75, inline=True)
#    embed.add_field(name="Defense", value=10, inline=True)
#    embed.add_field(name="AttackPower", value=15, inline=True)
#    embed.add_field(name="XP", value=80, inline=True)
#    await ctx.send(embed=embed)


# --- routine: setup/assign cog
def setup(bot):
    bot.add_cog(DEV(bot))
