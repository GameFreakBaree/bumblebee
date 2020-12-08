import discord
from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database, embedcolor, footer
import re


class CommandsSetPrefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="set-prefix", aliases=['setprefix'])
    @commands.has_permissions(manage_guild=True)
    async def set_prefix(self, ctx, prefix=None):
        db_bumblebee = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        bumblebee_cursor = db_bumblebee.cursor()

        bumblebee_cursor.execute("SELECT * FROM bumblebee_guildsettings WHERE guild_id = %s", (ctx.guild.id,))
        guildsettings = bumblebee_cursor.fetchone()

        if guildsettings is None:
            insert_guilddata = "INSERT INTO bumblebee_guildsettings (guild_id, logchannel_id, mute_role, prefix) VALUES (%s, %s, %s, %s)"
            record = (ctx.guild.id, 0, 0, "b!")
            bumblebee_cursor.execute(insert_guilddata, record)
            db_bumblebee.commit()

        if prefix is not None:
            lengte_prefix = len(prefix)

            if lengte_prefix <= 5:
                regex = re.sub(r'[^A-Za-z!~,.<>]', '', prefix)

                if prefix == regex:
                    bumblebee_cursor.execute(f"UPDATE bumblebee_guildsettings SET prefix = %s WHERE guild_id = %s", (prefix, ctx.guild.id))
                    db_bumblebee.commit()

                    embed = discord.Embed(
                        description=f"You've updated the prefix to `{regex}`",
                        color=embedcolor
                    )
                    embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    embed.set_footer(text=footer)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Prefix contains invalid characters.\nValid charachters are:\n`A-Z`, `a-z`, `!`, `<`, `>`, `~`, `.`, `,`")
            else:
                await ctx.send("The prefix is limited to a maximum of 5 characters.")
        else:
            await ctx.send("Invalid Arguments.")
        db_bumblebee.close()

    @set_prefix.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        else:
            raise error


def setup(client):
    client.add_cog(CommandsSetPrefix(client))
