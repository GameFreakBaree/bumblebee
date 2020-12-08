import asyncio
import os
import discord
from discord.ext import commands
from settings import host, user, passwd, database, token, bot_name, folder_list
import mysql.connector

intents = discord.Intents.default()
intents.members = True


def get_prefix(client, message):
    db_bumblebee = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
    bumblebee_cursor = db_bumblebee.cursor()

    bumblebee_cursor.execute("SELECT prefix FROM bumblebee_guildsettings WHERE guild_id = %s" % (message.guild.id,))
    prefix_tuple = bumblebee_cursor.fetchone()

    bumblebee_cursor.close()

    if prefix_tuple is None:
        prefix = "b!"
    else:
        prefix = prefix_tuple[0]

    return prefix


client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents)
client.remove_command("help")


async def change_status():
    await client.wait_until_ready()
    while client.is_ready():
        status = discord.Activity(name="ALPHA", type=discord.ActivityType.watching)
        await client.change_presence(activity=status)
        await asyncio.sleep(300)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

for folder in folder_list:
    print(f"[{bot_name}] ----------------------[ {folder.title()} ]--------------------")
    for filename in os.listdir(f'./{folder}'):
        if filename.endswith('.py'):
            print(f"[{bot_name}] {folder.title()} > {filename[:-3]} > Loaded!")
            client.load_extension(f'{folder}.{filename[:-3]}')
print(f"[{bot_name}] ------------------------------------------------------")

client.loop.create_task(change_status())
client.run(token)
