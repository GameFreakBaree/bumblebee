import asyncio
import discord
import datetime
from settings import host, user, passwd, database, embedcolor, footer
from discord.ext import commands
import mysql.connector


class ModWarn(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, member: discord.Member = None, *, reason="Unspecified"):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()

        bumblebee_cursor.execute(f"SELECT warn FROM bumblebee_commands WHERE guild_id = {ctx.guild.id}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            if member is not None and member != ctx.author:
                if not member.bot:
                    bumblebee_cursor.execute(f"SELECT * FROM bumblebee_warns WHERE guild_id = {ctx.guild.id} AND user = {member.id}")
                    total_warns = bumblebee_cursor.fetchall()

                    if len(total_warns) <= 15:
                        await member.send(f"You have been warned in **{ctx.guild}** by **{ctx.author}**\n```\nReason: {reason}\n```")

                        prewarn_embed = discord.Embed(
                            description=f"**Reason:** {reason}",
                            color=embedcolor
                        )
                        prewarn_embed.set_author(name=f"{member} has been warned!", icon_url=member.avatar_url)
                        await ctx.send(embed=prewarn_embed)

                        instertwarn = "INSERT INTO bumblebee_warns (guild_id, user, moderator, reason) VALUES (%s, %s, %s, %s)"
                        warn = (ctx.guild.id, member.id, ctx.author.id, reason)
                        bumblebee_cursor.execute(instertwarn, warn)
                        db_bumblebee.commit()

                        bumblebee_cursor.execute(f"SELECT logchannel_id FROM bumblebee_guildsettings WHERE guild_id = {ctx.guild.id}")
                        log_channel_id = bumblebee_cursor.fetchone()

                        if log_channel_id is None:
                            insert_guilddata = "INSERT INTO bumblebee_guildsettings (guild_id, logchannel_id, mute_role, prefix) VALUES (%s, %s, %s, %s)"
                            record = (ctx.guild.id, 0, 0, "b!")
                            bumblebee_cursor.execute(insert_guilddata, record)
                            db_bumblebee.commit()
                            log_channel_id = (0,)

                        try:
                            if log_channel_id[0] != 0:
                                log_channel = self.client.get_channel(log_channel_id[0])
                                warn_embed = discord.Embed(
                                    color=embedcolor,
                                    timestamp=datetime.datetime.utcnow()
                                )
                                warn_embed.add_field(name="User", value=f"**Name:**\t{member.mention}\n**ID:**\t{member.id}",
                                                     inline=True)
                                warn_embed.add_field(name="Moderator",
                                                     value=f"**Name:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                                warn_embed.add_field(name="Reason", value=f"{reason}", inline=False)
                                warn_embed.set_author(name=f"[WARN] {member}", icon_url=member.avatar_url)
                                warn_embed.set_footer(text=footer)
                                await log_channel.send(embed=warn_embed)
                        except AttributeError:
                            pass
                    else:
                        await ctx.send("You reached the limit of warns you can give one user. **Buy PRO to unlock unlimited warns per user.**")
                else:
                    await ctx.send("You cannot warn a bot.")
            else:
                if member is None:
                    await ctx.send("Invalid user.")
                elif member == ctx.author:
                    await ctx.send("You can't warn yourself.")
        db_bumblebee.close()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def delwarn(self, ctx, warn_id=None, *, member: discord.Member = None):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()

        bumblebee_cursor.execute(f"SELECT warn FROM bumblebee_commands WHERE guild_id = {ctx.guild.id}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            id_check = False
            valid_id_check = False
            log_check = False
            member_mention = 0

            try:
                if warn_id == "all":
                    id_check = True
                else:
                    warn_id = int(warn_id)

                    if warn_id > 0:
                        id_check = True
            except ValueError:
                await ctx.send("Invalid Warn ID... Try `b!warninfo <member>` to see what ID a warn is.\nIf you wan't to clear all warns type: `b!delwarn all <member>` to delete all warns from one member"
                               "or `b!resetwarns` to reset all warns in the server.")

            if id_check:
                if warn_id == "all":
                    bumblebee_cursor.execute(f"DELETE FROM bumblebee_warns WHERE guild_id = {ctx.guild.id} AND user = {member.id}")
                    db_bumblebee.commit()

                    member_mention = member.mention
                    log_check = True

                    delwarn_embed = discord.Embed(
                        description=f"All warns of {member.mention} have been removed.",
                        color=embedcolor
                    )
                    delwarn_embed.set_author(name=f"[DELETE WARN] {member}", icon_url=member.avatar_url)
                    await ctx.send(embed=delwarn_embed)
                else:
                    bumblebee_cursor.execute(f"SELECT warn_id FROM bumblebee_warns WHERE guild_id = {ctx.guild.id}")
                    warn_id_tuple = bumblebee_cursor.fetchall()

                    for ids in warn_id_tuple:
                        if warn_id == ids[0]:
                            valid_id_check = True
                            break

                if valid_id_check:
                    bumblebee_cursor.execute(f"SELECT * FROM bumblebee_warns WHERE warn_id = {warn_id}")
                    warn_tuple = bumblebee_cursor.fetchone()

                    bumblebee_cursor.execute(f"DELETE FROM bumblebee_warns WHERE warn_id = {warn_id}")
                    db_bumblebee.commit()

                    try:
                        member = self.client.get_user(warn_tuple[2])
                        member_mention = member.mention
                    except AttributeError:
                        member_mention = warn_tuple[2]

                    delwarn_embed = discord.Embed(
                        description=f"The warn on {member_mention} with reason **{warn_tuple[4]}** has been removed.",
                        color=embedcolor
                    )
                    delwarn_embed.set_author(name=f"[DELETE WARN] {member}", icon_url=member.avatar_url)
                    await ctx.send(embed=delwarn_embed)
                    log_check = True

                if log_check:
                    bumblebee_cursor.execute(f"SELECT logchannel_id FROM bumblebee_guildsettings WHERE guild_id = {ctx.guild.id}")
                    log_channel_id = bumblebee_cursor.fetchone()

                    try:
                        if log_channel_id[0] != 0:
                            log_channel = self.client.get_channel(log_channel_id[0])
                            warn_embed = discord.Embed(
                                color=embedcolor,
                                timestamp=datetime.datetime.utcnow()
                            )
                            warn_embed.add_field(name="User", value=f"**Name:**\t{member_mention}\n**ID:**\t{member.id}",
                                                 inline=True)
                            warn_embed.add_field(name="Moderator",
                                                 value=f"**Name:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                            warn_embed.set_author(name=f"[DELETE WARN] {member}", icon_url=member.avatar_url)
                            warn_embed.set_footer(text=footer)
                            await log_channel.send(embed=warn_embed)
                    except AttributeError:
                        pass
            else:
                await ctx.send("Invalid Warn ID... Try `b!warninfo <member>` to see what ID a warn is.\nIf you wan't to clear all warns type: `b!delwarn all <member>` to delete all warns from one member"
                               "or `b!resetwarns` to reset all warns in the server.")
        db_bumblebee.close()

    @commands.command()
    @commands.is_owner()
    async def resetwarns(self, ctx):
        db_bumblebee = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        bumblebee_cursor = db_bumblebee.cursor()
        bumblebee_cursor.execute(f"DELETE FROM bumblebee_warns WHERE guild_id = %s", (ctx.guild.id,))
        db_bumblebee.commit()
        db_bumblebee.close()

        resetwarn_embed = discord.Embed(
            description=f"All warns of **{ctx.guild}** have been removed.",
            color=embedcolor
        )
        resetwarn_embed.set_author(name=f"[RESET WARNS] {ctx.guild}", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=resetwarn_embed)

    @commands.command(aliases=["warns", "warnsinfo"])
    @commands.has_permissions(manage_guild=True)
    async def warninfo(self, ctx, *, member: discord.Member):
        # Command is not finished yet. Do not use this!
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()

        bumblebee_cursor.execute(f"SELECT warn FROM bumblebee_commands WHERE guild_id = {ctx.guild.id}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            page = 1
            items_per_pagina = 3
            offset = (page - 1) * items_per_pagina
            volgnummer = offset
            warn_list = ""
            doorgaan = True

            bumblebee_cursor.execute(f"SELECT * FROM bumblebee_warns WHERE guild_id = {ctx.guild.id} AND user = {member.id} LIMIT {items_per_pagina}")
            warn_id_tuple = bumblebee_cursor.fetchall()

            for ids in warn_id_tuple:
                try:
                    user_name = self.client.get_user(ids[2])
                except AttributeError:
                    user_name = ids[2]

                try:
                    moderator = self.client.get_user(ids[3])
                except AttributeError:
                    moderator = ids[3]

                volgnummer += 1
                warn_list = f"{warn_list}**{volgnummer}.** **Warn ID:** {ids[0]}\n- **User:** {user_name}\n- **Moderator:** {moderator}\n- **Reason:** {ids[4]}\n\n"

            if warn_list == "":
                warn_list = "**No warnings found!**"
                doorgaan = False

            bumblebee_cursor.execute(f"SELECT * FROM bumblebee_warns WHERE guild_id = {ctx.guild.id} AND user = {member.id}")
            max_rows_tuple = bumblebee_cursor.fetchall()
            max_rows = len(max_rows_tuple)

            if max_rows % items_per_pagina != 0:
                max_rows = max_rows // items_per_pagina + 1
            else:
                max_rows = max_rows // items_per_pagina

            if max_rows == 1:
                doorgaan = False

            warn_embed = discord.Embed(
                description=f"{warn_list}",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            warn_embed.set_author(name=f"[WARNINGS] {member}", icon_url=member.avatar_url)
            warn_embed.set_footer(text=f"{footer} | Page {page}/{max_rows}")
            await ctx.send(embed=warn_embed)

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        else:
            raise error

    @delwarn.error
    async def delwarn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        else:
            raise error

    @warninfo.error
    async def warninfo_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        else:
            raise error

    @resetwarns.error
    async def resetwarns_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have enough permissions. "
                           "You need to be the **OWNER** of this Guild to use this command.")
        else:
            raise error


def setup(client):
    client.add_cog(ModWarn(client))
