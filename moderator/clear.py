import asyncio
import discord
import datetime
from settings import host, user, passwd, database, embedcolor, footer
from discord.ext import commands
import mysql.connector


class ModClear(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["purge", "clean"])
    @commands.has_permissions(manage_guild=True)
    async def clear(self, ctx, amount=0):
        db_bumblebee = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        bumblebee_cursor = db_bumblebee.cursor()
        guild = ctx.guild.id

        bumblebee_cursor.execute(f"SELECT clear FROM bumblebee_commands WHERE guild_id = {guild}")
        command_enabled = bumblebee_cursor.fetchone()

        if command_enabled is None:
            command_status = 1
        else:
            command_status = command_enabled[0]

        if command_status == 1:
            if amount == 0:
                await ctx.channel.purge(limit=1)
                delete_message = await ctx.send(
                    "You have to use a bigger value than 0. (e.g.: `!clear 5`).")
                await asyncio.sleep(3)
                await delete_message.delete()
            elif amount > 125:
                await ctx.channel.purge(limit=1)
                delete_message = await ctx.send("You have to use a smaller value than 125")
                await asyncio.sleep(3)
                await delete_message.delete()
            else:
                await ctx.channel.purge(limit=amount + 1)
                if amount == 1:
                    correct_message = "message"
                else:
                    correct_message = "messages"
                delete_message = await ctx.send(f"{amount} {correct_message} has been deleted!")
                await asyncio.sleep(3)
                await delete_message.delete()

                bumblebee_cursor.execute(f"SELECT logchannel_id FROM bumblebee_guildsettings WHERE guild_id = {guild}")
                log_channel_id = bumblebee_cursor.fetchone()

                try:
                    if log_channel_id[0] != 0:
                        log_channel = self.client.get_channel(log_channel_id[0])
                        clear_embed = discord.Embed(
                            color=embedcolor,
                            timestamp=datetime.datetime.utcnow()
                        )
                        clear_embed.add_field(name="Moderator", value=f"**Name:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                        clear_embed.add_field(name="Messages Deleted", value=f"{amount}", inline=True)
                        clear_embed.add_field(name="Channel", value=f"{ctx.channel.mention}", inline=True)
                        clear_embed.set_author(name=f"[CLEAR] {ctx.author}", icon_url=ctx.author.avatar_url)
                        clear_embed.set_footer(text=footer)
                        await log_channel.send(embed=clear_embed)
                except AttributeError:
                    pass
        db_bumblebee.close()

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("I don't have enough permissions.\nMake sure that I have the permission MANAGE MESSAGES in at least one of my roles and in this channel.")
        else:
            raise error


def setup(client):
    client.add_cog(ModClear(client))
