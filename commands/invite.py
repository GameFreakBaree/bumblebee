import discord
from discord.ext import commands
from settings import embedcolor


class InviteCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            description=f":link: Invite me here: [Click Here](https://discord.com/oauth2/authorize?client_id=742776969481158766&permissions=1074097233&redirect_uri=https%3A%2F%2Fdiscord.gg%2F5gvn5pn&scope=bot)",
            color=embedcolor
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(InviteCmd(client))
