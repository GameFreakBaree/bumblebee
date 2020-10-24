import discord
from discord.ext import commands


class PingCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        ping = round(self.client.latency * 1000)

        if ping > 1000:
            embedcolor = 0xEC0808
        elif 1000 >= ping >= 250:
            embedcolor = 0xFF8A00
        else:
            embedcolor = 0x01D31E

        embed = discord.Embed(
            description=f"**Ping:** {ping}ms",
            color=embedcolor
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PingCmd(client))
