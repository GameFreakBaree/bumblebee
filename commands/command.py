import discord
from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database, embedcolor, footer


class CommandsCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def command(self, ctx, setting=None, command_name=None):
        db_bumblebee = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        bumblebee_cursor = db_bumblebee.cursor()

        bumblebee_cursor.execute("SELECT prefix FROM bumblebee_guildsettings WHERE guild_id = %s" % (ctx.guild.id,))
        prefix_tuple = bumblebee_cursor.fetchone()

        if prefix_tuple is None:
            prefix = "b!"
        else:
            prefix = prefix_tuple[0]

        command_list = ['ban', 'tempban', 'unban', 'mute', 'tempmute', 'unmute',
                        'kick', 'clear', 'warn', 'automoderator']

        if setting.lower() == "enable" or setting.lower() == "disable":
            if setting.lower() == "enable":
                on_off = 1
            elif setting.lower() == "disable":
                on_off = 0
            else:
                on_off = 0

            if command_name.lower() in command_list:
                bumblebee_cursor.execute("SELECT * FROM bumblebee_commands WHERE guild_id = %s", ctx.guild.id)
                command_data = bumblebee_cursor.fetchone()

                if command_data is None:
                    insert_command_data = "INSERT INTO bumblebee_commands (guild_id, ban, mute, kick, clear, warn, automoderator) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    record = (ctx.guild.id, 1, 1, 1, 1, 1, 1, 1)
                    bumblebee_cursor.execute(insert_command_data, record)
                    db_bumblebee.commit()

                bumblebee_cursor.execute(f"UPDATE bumblebee_commands SET {command_name.lower()} = %s WHERE guild_id = %s", (on_off, ctx.guild.id))
                db_bumblebee.commit()

                embed = discord.Embed(
                    description=f"You've succesfully {setting.lower()}d the command {command_name.lower()}",
                    color=embedcolor
                )
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Invalid Arguments. Try: `{prefix}command <enable/disable> <command>`"
                               f"\nPossible Commands: ban, tempban, unban, mute, tempmute, unmute, kick, clear, warn, automoderator")
        else:
            await ctx.send(f"Invalid Arguments. Try: `{prefix}command <enable/disable> <command>`"
                           f"\nPossible Commands: ban, tempban, unban, mute, tempmute, unmute, kick, clear, warn, automoderator")
        db_bumblebee.close()

    @command.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        else:
            raise error


def setup(client):
    client.add_cog(CommandsCommand(client))
