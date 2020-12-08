from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database


class OnGuildJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"[ADD] Guild: {guild} heeft de bot toegevoegd.")

        insert_guilddata = "INSERT INTO bumblebee_guildsettings (guild_id, logchannel_id, mute_role, prefix) VALUES (%s, %s, %s, %s)"
        record = (guild.id, 0, 0, "b!")

        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()
        bumblebee_cursor.execute(insert_guilddata, record)
        db_bumblebee.commit()
        db_bumblebee.close()


def setup(client):
    client.add_cog(OnGuildJoin(client))
