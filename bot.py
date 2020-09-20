import asyncio
import os
import discord
from discord.ext import commands
from data import settings

client = commands.Bot(command_prefix='b!', case_insensitive=True)
client.remove_command("help")

folder_list = ['events', 'commands', 'moderator']
bot_name = "Bumblebee"


async def change_status():
    await client.wait_until_ready()
    while client.is_ready():
        status = discord.Activity(name=f"Optimus Prime", type=discord.ActivityType.watching)
        await client.change_presence(activity=status)
        await asyncio.sleep(60)


@client.command()
async def load(ctx, types=None, extension=None):
    if ctx.author.id == 643072638075273248:
        if types is not None and extension is not None:
            if types.lower() in folder_list:
                if extension == "*":
                    for filenames in os.listdir(f'./{types}'):
                        if filenames.endswith('.py'):
                            print(f"Load {extension}, by {ctx.author}")
                            client.load_extension(f'{types}.{filenames[:-3]}')
                    await ctx.send(f"Loaded all extensions in {types}, succes!")
                else:
                    client.load_extension(f'{types}.{extension}')
                    print(f"Load {extension}, by {ctx.author} in {types}")
                    await ctx.send(f"Load {extension}, succes!")


@client.command()
async def reload(ctx, types=None, extension=None):
    if ctx.author.id == 643072638075273248:
        if types is not None and extension is not None:
            if types.lower() in folder_list:
                if extension == "*":
                    for filenames in os.listdir(f'./{types}'):
                        if filenames.endswith('.py'):
                            print(f"Reload {extension}, by {ctx.author}")
                            client.unload_extension(f'{types}.{filenames[:-3]}')
                            client.load_extension(f'{types}.{filenames[:-3]}')
                    await ctx.send(f"Reloaded all extensions in {types}, succes!")
                else:
                    client.unload_extension(f'{types}.{extension}')
                    client.load_extension(f'{types}.{extension}')
                    print(f"Reload {extension}, door {ctx.author} in {types}")
                    await ctx.send(f"Reload {extension}, succes!")


@client.command()
async def unload(ctx, types=None, extension=None):
    if ctx.author.id == 643072638075273248:
        if types is not None and extension is not None:
            if types.lower() in folder_list:
                if extension == "*":
                    for filenames in os.listdir(f'./{types}'):
                        if filenames.endswith('.py'):
                            print(f"Unload {extension}, by {ctx.author}")
                            client.unload_extension(f'{types}.{filenames[:-3]}')
                    await ctx.send(f"Unloaded all extensions in {types}, succes!")
                else:
                    client.unload_extension(f'{types}.{extension}')
                    print(f"Unload {extension}, door {ctx.author} in {types}")
                    await ctx.send(f"Unload {extension}, succes!")


for folder in folder_list:
    print(f"[{bot_name}] ----------------------[ {folder.title()} ]--------------------")
    for filename in os.listdir(f'./{folder}'):
        if filename.endswith('.py'):
            print(f"[{bot_name}] {folder.title()} > {filename[:-3]} > Loaded!")
            client.load_extension(f'{folder}.{filename[:-3]}')

print(f"[{bot_name}] ------------------------------------------------------")

client.loop.create_task(change_status())
client.run(settings.token)
