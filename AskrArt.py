import discord
import asyncio
from twython import Twython

from .. import info_keys
from cmds.bot import Bot

from cmds.projectManager import project_manager

# Create an object of all commands and list here
commands = [project_manager()]

def load_commands():
    command_dict = dict()
    for command in commands:
        command_dict.update({command.name:command})
    return command_dict

client = Bot.client

# Twitter info
twitter = Twython(info_keys.TWITTER_KEY, info_keys.TWITTER_SECRET, info_keys.TWITTER_TOKEN, info_keys.TWITTER_TOKEN_SECRET)

@client.event
async def on_ready():
    print('Ready!')

@client.event
async def on_message(message):
    if message.content.startswith('>'):
        command = message.content.split(' ')[0][1::]
        await command_dict[command].do_command(message)

command_dict = load_commands()
client.run(info_keys.BOT_TOKEN)
