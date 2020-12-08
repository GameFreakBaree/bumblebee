import discord
from discord.ext import commands
import datetime
from settings import host, user, passwd, database, embedcolor, footer
import mysql.connector


class HelpMsg(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    @commands.has_permissions(manage_guild=True)
    async def helpcmd(self, ctx):
        db_bumblebee = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        bumblebee_cursor = db_bumblebee.cursor()

        bumblebee_cursor.execute("SELECT prefix FROM bumblebee_guildsettings WHERE guild_id = %s" % (ctx.guild.id,))
        prefix_tuple = bumblebee_cursor.fetchone()

        bumblebee_cursor.close()

        if prefix_tuple is None:
            prefix = "b!"
        else:
            prefix = prefix_tuple[0]

        if ctx.author == ctx.guild.owner:
            embed = discord.Embed(
                description=f"**__Owner Commands__**\n"
                            f"\n• **{prefix}resetall** - Remove data from the bot in the guild."
                            f"\n• **{prefix}resetwarns** - Remove all warns in the guild."
                            f"\n\n**__Staff Commands__** *- Requires MANAGE_SERVER*\n"
                            f"\n• **{prefix}kick <name> [reason]** - Kick a user from the server."
                            f"\n• **{prefix}silentkick <name> [reason]** - Kick a user without sending a DM."
                            f"\n• **{prefix}ban <name> [reason]** - Ban a user permanently."
                            f"\n• **{prefix}silentban <name> [reason]** - Ban a user permanently without sending a DM."
                            f"\n• **{prefix}unban <name>** - Unban a user from the server."
                            f"\n• **{prefix}mute <name> [reason]** - Mute a user (must have a valid `Muted` role)."
                            f"\n• **{prefix}unmute <name>** - Unmute a user if they have the Muted role."
                            f"\n• **{prefix}clear <name>** - Clear up to 125 messages at a time."
                            f"\n• **{prefix}warn <name> [reason]** - Warn a user with a reason."
                            f"\n• **{prefix}delwarn <warn_id>** - Delete a specific warning."
                            f"\n• **{prefix}delwarn all <name>** - Delete all warnings of a user."
                            f"\n• **{prefix}set-prefix <prefix>** - Setup the prefix for the bot."
                            f"\n• **{prefix}set-mute-role <role>** - Setup the mute role."
                            f"\n• **{prefix}set-logchannel <#channel>** - Setup the log channel."
                            f"\n• **{prefix}command <enable/disable> <command>** - Enable and disable specific commands."
                            f"\n\n**__Member Commands__**\n"
                            f"\n• **{prefix}help** - Displays this Embed."
                            f"\n• **{prefix}ping** - Get the ping in milliseconds of the bot."
                            f"\n• **{prefix}info** - Get all the information about the bot."
                            f"\n• **{prefix}invite** - Get an invite to add the bot."
                            f"\n• **{prefix}warninfo <name>** - Gives a list of all warnings of one user.",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                description=f"\n\n**__Staff Commands__** *- Requires MANAGE_SERVER*\n"
                            f"\n• **{prefix}kick <name> [reason]** - Kick a user from the server."
                            f"\n• **{prefix}silentkick <name> [reason]** - Kick a user without sending a DM."
                            f"\n• **{prefix}ban <name> [reason]** - Ban a user permanently."
                            f"\n• **{prefix}silentban <name> [reason]** - Ban a user permanently without sending a DM."
                            f"\n• **{prefix}unban <name>** - Unban a user from the server."
                            f"\n• **{prefix}mute <name> [reason]** - Mute a user (must have a valid `Muted` role)."
                            f"\n• **{prefix}unmute <name>** - Unmute a user if they have the Muted role."
                            f"\n• **{prefix}clear <name>** - Clear up to 125 messages at a time."
                            f"\n• **{prefix}warn <name> [reason]** - Warn a user with a reason."
                            f"\n• **{prefix}delwarn <warn_id>** - Delete a specific warning."
                            f"\n• **{prefix}delwarn all <name>** - Delete all warnings of a user."
                            f"\n• **{prefix}set-prefix <prefix>** - Setup the prefix for the bot."
                            f"\n• **{prefix}set-mute-role <role>** - Setup the mute role."
                            f"\n• **{prefix}set-logchannel <#channel>** - Setup the log channel."
                            f"\n• **{prefix}command <enable/disable> <command>** - Enable and disable specific commands."
                            f"\n\n**__Member Commands__**\n"
                            f"\n• **{prefix}help** - Displays this Embed."
                            f"\n• **{prefix}ping** - Get the ping in milliseconds of the bot."
                            f"\n• **{prefix}info** - Get all the information about the bot."
                            f"\n• **{prefix}invite** - Get an invite to add the bot."
                            f"\n• **{prefix}warninfo <name>** - Gives a list of all warnings of one user.",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @helpcmd.error
    async def helpcmd_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            db_bumblebee = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
            bumblebee_cursor = db_bumblebee.cursor()

            bumblebee_cursor.execute("SELECT prefix FROM bumblebee_guildsettings WHERE guild_id = %s" % (ctx.guild.id,))
            prefix_tuple = bumblebee_cursor.fetchone()

            bumblebee_cursor.close()

            if prefix_tuple is None:
                prefix = "b!"
            else:
                prefix = prefix_tuple[0]

            embed = discord.Embed(
                description=f"\n• **{prefix}help** - Displays this Embed."
                            f"\n• **{prefix}ping** - Get the ping in milliseconds of the bot."
                            f"\n• **{prefix}info** - Get all the information about the bot."
                            f"\n• **{prefix}invite** - Get an invite to add the bot."
                            f"\n• **{prefix}warninfo <name>** - Gives a list of all warnings of one user.",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(HelpMsg(client))
