import discord
import datetime
from discord.ext import commands
from settings import host, user, passwd, database, embedcolor, footer
from discord.utils import get
import mysql.connector


class ModeratorMute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason="Unspecified"):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()
        guild = ctx.guild.id

        bumblebee_cursor.execute(f"SELECT mute FROM bumblebee_commands WHERE guild_id = {guild}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            if member is not None and member != ctx.author:
                bumblebee_cursor.execute("SELECT * FROM bumblebee_guildsettings WHERE guild_id = %s", (ctx.guild.id,))
                guildsettings = bumblebee_cursor.fetchone()

                if guildsettings is None:
                    insert_guilddata = "INSERT INTO bumblebee_guildsettings (guild_id, logchannel_id, mute_role, prefix) VALUES (%s, %s, %s, %s)"
                    record = (ctx.guild.id, 0, 0, "b!")
                    bumblebee_cursor.execute(insert_guilddata, record)
                    db_bumblebee.commit()

                bumblebee_cursor.execute(f"SELECT mute_role FROM bumblebee_guildsettings WHERE guild_id = {guild}")
                role_id = bumblebee_cursor.fetchone()

                guild = ctx.guild
                if role_id[0] == 0:
                    perms = discord.Permissions(send_messages=False, read_messages=True)
                    role = await guild.create_role(name="Muted", permissions=perms)

                    bumblebee_cursor.execute(f"UPDATE bumblebee_guildsettings SET mute_role = %s WHERE guild_id = %s", (role.id, ctx.guild.id))
                    db_bumblebee.commit()
                else:
                    role = guild.get_role(role_id[0])

                muted_role = get(ctx.guild.roles, name=f"{role}")
                if muted_role not in member.roles:
                    try:
                        await member.add_roles(role)
                    except AttributeError:
                        perms = discord.Permissions(send_messages=False, read_messages=True)
                        role = await guild.create_role(name="Muted", permissions=perms)

                        bumblebee_cursor.execute(f"UPDATE bumblebee_guildsettings SET mute_role = %s WHERE guild_id = %s", (role.id, ctx.guild.id))
                        db_bumblebee.commit()

                        await member.add_roles(role)

                    premute_embed = discord.Embed(
                        description=f"**Reason:** {reason}",
                        color=embedcolor
                    )
                    premute_embed.set_author(name=f"{member} has been muted!", icon_url=member.avatar_url)
                    await ctx.send(embed=premute_embed)

                    bumblebee_cursor.execute(f"SELECT logchannel_id FROM bumblebee_guildsettings WHERE guild_id = {ctx.guild.id}")
                    log_channel_id = bumblebee_cursor.fetchone()

                    try:
                        if log_channel_id[0] != 0:
                            log_channel = self.client.get_channel(log_channel_id[0])
                            mute_embed = discord.Embed(
                                color=embedcolor,
                                timestamp=datetime.datetime.utcnow()
                            )
                            mute_embed.add_field(name="User", value=f"**Name:**\t{member.mention}\n**ID:**\t{member.id}", inline=True)
                            mute_embed.add_field(name="Moderator", value=f"**Name:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                            mute_embed.add_field(name="Reason", value=f"{reason}", inline=False)
                            mute_embed.add_field(name="Duration", value=f"∞", inline=False)
                            mute_embed.set_author(name=f"[MUTE] {member}", icon_url=member.avatar_url)
                            mute_embed.set_footer(text=footer)
                            await log_channel.send(embed=mute_embed)
                    except AttributeError:
                        pass
                else:
                    await ctx.send("This user is already muted.")
        db_bumblebee.close()

    @commands.command()
    async def unmute(self, ctx, *, member: discord.Member):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()
        guild = ctx.guild.id

        bumblebee_cursor.execute(f"SELECT mute FROM bumblebee_commands WHERE guild_id = {guild}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            if member is not None and member != ctx.author:
                bumblebee_cursor.execute("SELECT * FROM bumblebee_guildsettings WHERE guild_id = %s", (ctx.guild.id,))
                guildsettings = bumblebee_cursor.fetchone()

                if guildsettings is None:
                    insert_guilddata = "INSERT INTO bumblebee_guildsettings (guild_id, logchannel_id, mute_role, prefix) VALUES (%s, %s, %s, %s)"
                    record = (ctx.guild.id, 0, 0, "b!")
                    bumblebee_cursor.execute(insert_guilddata, record)
                    db_bumblebee.commit()

                bumblebee_cursor.execute(f"SELECT mute_role FROM bumblebee_guildsettings WHERE guild_id = {guild}")
                role_id = bumblebee_cursor.fetchone()

                guild = ctx.guild
                if role_id[0] == 0:
                    await ctx.send("No mute role found.")
                else:
                    role = guild.get_role(role_id[0])
                    # role = discord.utils.find(lambda r: r.name == f"{role}", ctx.message.guild.roles)

                    if role in member.roles:
                        await member.remove_roles(role)

                        premute_embed = discord.Embed(
                            color=embedcolor
                        )
                        premute_embed.set_author(name=f"{member} is now unmuted!", icon_url=member.avatar_url)
                        await ctx.send(embed=premute_embed)

                        bumblebee_cursor.execute(f"SELECT logchannel_id FROM bumblebee_guildsettings WHERE guild_id = {ctx.guild.id}")
                        log_channel_id = bumblebee_cursor.fetchone()

                        try:
                            if log_channel_id[0] != 0:
                                log_channel = self.client.get_channel(log_channel_id[0])
                                mute_embed = discord.Embed(
                                    color=embedcolor,
                                    timestamp=datetime.datetime.utcnow()
                                )
                                mute_embed.add_field(name="User", value=f"**Name:**\t{member.mention}\n**ID:**\t{member.id}", inline=True)
                                mute_embed.add_field(name="Moderator", value=f"**Name:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                                mute_embed.set_author(name=f"[UNMUTE] {member}", icon_url=member.avatar_url)
                                mute_embed.set_footer(text=footer)
                                await log_channel.send(embed=mute_embed)
                        except AttributeError:
                            pass
                    else:
                        await ctx.send(f"{member} is not muted.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("I don't have enough permissions.\nMake sure that I have the permission MANAGE ROLES in at least one of my roles.")
        else:
            raise error


def setup(client):
    client.add_cog(ModeratorMute(client))
