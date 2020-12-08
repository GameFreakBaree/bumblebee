import discord
from discord.ext import commands
from settings import embedcolor, footer


class InfoCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            description=f"__Created by:__ GameFreakBaree#9999"
                        f"\n__Shard:__ 1/1"
                        f"\n\n**Useful URLs**"
                        f"\n[Invite the Bot](https://discord.com/api/oauth2/authorize?client_id=744123497214902312&permissions=268823622&redirect_uri=https%3A%2F%2Fdiscord.gg%2F5gvn5pn&scope=bot)"
                        f" - [Wiki](https://github.com/GameFreakBaree/Bumblebee/wiki)"
                        f" - [Support Server](https://discord.gg/5gvn5pn)",
            color=embedcolor
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(InfoCmd(client))
