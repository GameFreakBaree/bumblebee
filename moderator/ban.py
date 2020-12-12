import discord
import datetime
from settings import host, user, passwd, database, embedcolor, footer
from discord.ext import commands
import mysql.connector


class ModBan(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason="Unspecified"):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()
        guild = ctx.guild.id

        bumblebee_cursor.execute(f"SELECT ban FROM bumblebee_commands WHERE guild_id = {guild}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            if member is not None and member != ctx.author:
                await member.send(f"You got banned from **{ctx.guild}** by **{ctx.author}**\n```\nReason: {reason}\n```")

                await member.ban(reason=reason)

                preban_embed = discord.Embed(
                    description=f"**Reason:** {reason}",
                    color=embedcolor
                )
                preban_embed.set_author(name=f"{member} has been banned!", icon_url=member.avatar_url)
                await ctx.send(embed=preban_embed)

                bumblebee_cursor.execute(f"SELECT logchannel_id FROM bumblebee_guildsettings WHERE guild_id = {guild}")
                log_channel_id = bumblebee_cursor.fetchone()

                try:
                    if log_channel_id[0] != 0:
                        log_channel = self.client.get_channel(log_channel_id[0])
                        ban_embed = discord.Embed(
                            color=embedcolor,
                            timestamp=datetime.datetime.utcnow()
                        )
                        ban_embed.add_field(name="User", value=f"**Name:**\t{member.mention}\n**ID:**\t{member.id}", inline=True)
                        ban_embed.add_field(name="Moderator", value=f"**Name:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                        ban_embed.add_field(name="Reason", value=f"{reason}", inline=False)
                        ban_embed.add_field(name="Duration", value=f"∞", inline=False)
                        ban_embed.set_author(name=f"[BAN] {member}", icon_url=member.avatar_url)
                        ban_embed.set_footer(text=footer)
                        await log_channel.send(embed=ban_embed)
                except AttributeError:
                    pass
        db_bumblebee.close()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def silentban(self, ctx, member: discord.Member = None, *, reason="Unspecified"):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()
        guild = ctx.guild.id

        bumblebee_cursor.execute(f"SELECT ban FROM bumblebee_commands WHERE guild_id = {guild}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            await ctx.message.delete()

            if member is not None and member != ctx.author:
                await member.ban(reason=reason)

                bumblebee_cursor.execute(f"SELECT logchannel_id FROM bumblebee_guildsettings WHERE guild_id = {guild}")
                log_channel_id = bumblebee_cursor.fetchone()

                try:
                    if log_channel_id[0] != 0:
                        log_channel = self.client.get_channel(log_channel_id[0])
                        ban_embed = discord.Embed(
                            color=embedcolor,
                            timestamp=datetime.datetime.utcnow()
                        )
                        ban_embed.add_field(name="User", value=f"**Name:**\t{member.mention}\n**ID:**\t{member.id}", inline=True)
                        ban_embed.add_field(name="Moderator", value=f"**Name:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                        ban_embed.add_field(name="Reason", value=f"{reason}", inline=False)
                        ban_embed.add_field(name="Duration", value=f"∞", inline=False)
                        ban_embed.set_author(name=f"[BAN] {member}", icon_url=member.avatar_url)
                        ban_embed.set_footer(text=footer)
                        await log_channel.send(embed=ban_embed)
                except AttributeError:
                    pass
        db_bumblebee.close()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unban(self, ctx, *, member):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()
        guild = ctx.guild.id

        bumblebee_cursor.execute(f"SELECT unban FROM bumblebee_commands WHERE guild_id = {guild}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

            for ban_entry in banned_users:
                unban_user = ban_entry.user

                if (unban_user.name, unban_user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(unban_user)

                    preunban_embed = discord.Embed(
                        color=embedcolor
                    )
                    preunban_embed.set_author(name=f"{member} is now unbanned!", icon_url=ctx.author.default_avatar_url)
                    await ctx.send(embed=preunban_embed)

                    bumblebee_cursor.execute(f"SELECT logchannel_id FROM bumblebee_guildsettings WHERE guild_id = {guild}")
                    log_channel_id = bumblebee_cursor.fetchone()

                    try:
                        if log_channel_id[0] != 0:
                            log_channel = self.client.get_channel(log_channel_id[0])
                            unban_embed = discord.Embed(
                                color=embedcolor,
                                timestamp=datetime.datetime.utcnow()
                            )
                            unban_embed.add_field(name="User", value=f"**Name:**\t{member.mention}\n**ID:**\t{member.id}", inline=True)
                            unban_embed.add_field(name="Moderator", value=f"**Name:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                            unban_embed.set_author(name=f"[UNBAN] {member}", icon_url=member.avatar_url)
                            unban_embed.set_footer(text=footer)
                            await log_channel.send(embed=unban_embed)
                    except AttributeError:
                        pass
                    return
        db_bumblebee.close()

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("I don't have enough permissions.\nMake sure that I have the permission BAN MEMBERS in at least one of my roles.")
        else:
            raise error

    @silentban.error
    async def silentban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("I don't have enough permissions.\nMake sure that I have the permission BAN MEMBERS in at least one of my roles.")
        else:
            raise error


def setup(client):
    client.add_cog(ModBan(client))
