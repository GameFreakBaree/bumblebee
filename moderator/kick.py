import discord
import mysql.connector
from settings import host, user, passwd, database, embedcolor, footer
from discord.ext import commands
import datetime


class ModKick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason="Unspecified"):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()
        guild = ctx.guild.id

        bumblebee_cursor.execute(f"SELECT kick FROM bumblebee_commands WHERE guild_id = {guild}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            if member is not None and member != ctx.author:
                await member.send(f"You got kicked from **{ctx.guild}** by **{ctx.author}**\n```\nReason: {reason}\n```")

                await member.kick(reason=reason)

                prekick_embed = discord.Embed(
                    description=f"**Reason:** {reason}",
                    color=embedcolor
                )
                prekick_embed.set_author(name=f"{member} has been kicked!", icon_url=member.avatar_url)
                await ctx.send(embed=prekick_embed)

                bumblebee_cursor.execute(f"SELECT logchannel_id FROM bumblebee_guildsettings WHERE guild_id = {guild}")
                log_channel_id = bumblebee_cursor.fetchone()

                try:
                    if log_channel_id[0] != 0:
                        log_channel = self.client.get_channel(log_channel_id[0])
                        kick_embed = discord.Embed(
                            color=embedcolor,
                            timestamp=datetime.datetime.utcnow()
                        )
                        kick_embed.add_field(name="User", value=f"**Name:**\t{member.mention}\n**ID:**\t{member.id}", inline=True)
                        kick_embed.add_field(name="Moderator", value=f"**Name:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                        kick_embed.add_field(name="Reason", value=f"{reason}", inline=False)
                        kick_embed.set_author(name=f"[KICK] {member}", icon_url=member.avatar_url)
                        kick_embed.set_footer(text=footer)
                        await log_channel.send(embed=kick_embed)
                except AttributeError:
                    pass
        db_bumblebee.close()

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def silentkick(self, ctx, member: discord.Member = None, *, reason="Unspecified"):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()
        guild = ctx.guild.id

        bumblebee_cursor.execute(f"SELECT kick FROM bumblebee_commands WHERE guild_id = {guild}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            await ctx.message.delete()

            if member is not None and member != ctx.author:
                await member.kick(reason=reason)

                bumblebee_cursor.execute(f"SELECT logchannel_id FROM bumblebee_guildsettings WHERE guild_id = {guild}")
                log_channel_id = bumblebee_cursor.fetchone()

                try:
                    if log_channel_id[0] != 0:
                        log_channel = self.client.get_channel(log_channel_id[0])
                        kick_embed = discord.Embed(
                            color=embedcolor,
                            timestamp=datetime.datetime.utcnow()
                        )
                        kick_embed.add_field(name="User", value=f"**Name:**\t{member.mention}\n**ID:**\t{member.id}", inline=True)
                        kick_embed.add_field(name="Moderator", value=f"**Name:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                        kick_embed.add_field(name="Reason", value=f"{reason}", inline=False)
                        kick_embed.set_author(name=f"[KICK] {member}", icon_url=member.avatar_url)
                        kick_embed.set_footer(text=footer)
                        await log_channel.send(embed=kick_embed)
                except AttributeError:
                    pass
        db_bumblebee.close()

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        else:
            raise error

    @silentkick.error
    async def silentkick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        else:
            raise error


def setup(client):
    client.add_cog(ModKick(client))
