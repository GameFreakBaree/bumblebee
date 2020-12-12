import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, passwd, database, embedcolor, footer


class CommandsResetAll(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def resetall(self, ctx):
        insert_guilddata = "INSERT INTO bumblebee_guildsettings (guild_id, logchannel_id, mute_role) VALUES (%s, %s, %s)"
        record = (ctx.guild.id, 0, 0)

        db_bumblebee = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        bumblebee_cursor = db_bumblebee.cursor()
        bumblebee_cursor.execute(f"DELETE FROM bumblebee_guildsettings WHERE guild_id = %s", (ctx.guild.id,))
        bumblebee_cursor.execute(f"DELETE FROM bumblebee_commands WHERE guild_id = %s", (ctx.guild.id,))
        bumblebee_cursor.execute(f"DELETE FROM bumblebee_warns WHERE guild_id = %s", (ctx.guild.id,))
        db_bumblebee.commit()
        bumblebee_cursor.execute(insert_guilddata, record)
        db_bumblebee.commit()
        db_bumblebee.close()

        embed = discord.Embed(
            description=f"**Reset Complete!**",
            color=embedcolor,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @resetall.error
    async def resetall_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("You don't have enough permissions. "
                           "You need to be the **OWNER** of this Guild to use this command.")
        else:
            raise error


def setup(client):
    client.add_cog(CommandsResetAll(client))
