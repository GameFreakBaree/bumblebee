import discord
from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database, embedcolor


class InfoCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()

        bumblebee_cursor.execute(f"SELECT footer FROM bumblebee_guildsettings WHERE guild_id = {ctx.guild.id}")
        embed_footer = bumblebee_cursor.fetchone()
        db_bumblebee.close()

        embed = discord.Embed(
            description=f"__Created by:__ GameFreakBaree#9999\n__Shard:__ 1/1\n\n**Useful URLs**\n[Invite the Bot](https://discord.com/oauth2/authorize?client_id=742776969481158766&permissions=1074097233&redirect_uri=https%3A%2F%2Fdiscord.gg%2F5gvn5pn&scope=bot) - [Wiki](https://github.com/GameFreakBaree/Bumblebee/wiki) - [Support Server](https://discord.gg/5gvn5pn)",
            color=embedcolor
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=embed_footer[0])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(InfoCmd(client))
