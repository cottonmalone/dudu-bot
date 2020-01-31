import discord
from discord.ext import commands
import asyncio

TOKEN = 'YOUR DISCORD BOT TOKEN HERE'

client = commands.Bot(command_prefix = '$')
client.remove_command('help')

extensions = ['RaidCommands']

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def logout(ctx):
    if ctx.message.author.id in [YOUR DISCORD ID HERE]:
        await ctx.send('```Shutting down...```')
        await client.logout()
    else:
        await ctx.send('Nice try jackass!')

@client.command()
async def greet(ctx):
	await ctx.send("Hello everyone! I am Lanturn and I'm here to assist you :)")

@client.command()
async def load(extension):
    try:
        client.load_extension(extension)
        print('Loaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error))

@client.command()
async def unload(extension):
    try:
        client.unload_extension(extension)
        print('Unloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be unloaded. [{}]'.format(extension, error))

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    client.run(TOKEN)
