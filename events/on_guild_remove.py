from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database


class OnGuildRemove(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"[DEL] Guild: {guild} heeft de bot verwijderd.")

        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()
        bumblebee_cursor.execute(f"DELETE FROM bumblebee_guildsettings WHERE guild_id = %s", guild.id)
        bumblebee_cursor.execute(f"DELETE FROM bumblebee_commands WHERE guild_id = %s", guild.id)
        bumblebee_cursor.execute(f"DELETE FROM bumblebee_warns WHERE guild_id = %s", guild.id)
        db_bumblebee.commit()
        db_bumblebee.close()


def setup(client):
    client.add_cog(OnGuildRemove(client))
