import sys
import random
import logging
from os import (
    getcwd,
    listdir,
    path,
    chdir,
    system,
    environ as ENV,
)
from time import sleep

import discord
from discord import CategoryChannel
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get as _get
from requests import get

from core.pundit.helpers import tag_responses
from extensions.leaderboard import Leaderboard
from extensions.firstblood import Firstbloods

from core.pundit.pundit import (
    PUNDIT,
    TASKS,
    Pundit
)

logger = logging.getLogger(__name__)


COMMAND_PREFIX = PUNDIT['prefix']
TOKEN = PUNDIT['token']
ADMINCHNLS = PUNDIT['admincategories']


pundit = Pundit()
client = commands.Bot(command_prefix=commands.when_mentioned_or(
    '!'), description='Your pundit!!')

extensions = [
    'tasks',
    'polls',
    'leaderboard',
    'plagiarism',
    'statistics',
]

# Events
@client.event
async def on_member_join(member):
    await member.send("Hey {0}! Welcome to the recruitment server :candy:!\nI'm the official recruitment bot - Pundit!\nPlease head over to #general and look at the welcome note.\nIf you have no idea what to do next, ask for help in #welcome!".format(member.name))


# Events
@client.event
async def on_ready():
    print("<" + client.user.name + " Online>")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your progress | Good Luck :)"))
    print(client.guilds[0].members)
    await Leaderboard(client).start()
    await Firstbloods(client).start()

@client.event
async def on_message(message):  
    if "Awesome" in message.content:
        await message.channel.send("Wutt??")
    if client.user in message.mentions and message.content == f"<@!{client.user.id}>":
        await message.channel.send(tag_responses(message))
    await client.process_commands(message)


@client.event
async def on_message_edit(before, after):
    threshold = 30  # time in seconds
    if (
        after.content != before.content
        and after.edited_at.timestamp() - after.created_at.timestamp() <= threshold
    ):
        await client.process_commands(after)

# No Category Commands
@client.command()
@commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
async def whoispundit(ctx):
    """
    More about me
    """
    await ctx.send("Hey There,\nI'm pundit!!, your task evaluator. Complete your tasks and impress me to get your way up in the recruitment process.")
    sleep(random.randint(1, 5))
    await ctx.send("Oh yes, I forgot to tell - I was made by f4lc0n, baycho, varmasir and TheKid")


@client.command(pass_context=True)
@commands.dm_only()
async def register(ctx, flag):
    """
    Register
    """
    if(flag == PUNDIT['playerroles']['base'][0]['secret']):
        server = client.get_guild(id=PUNDIT['server'])
        baserole = _get(
            server.roles, name=PUNDIT['playerroles']['base'][0]['role'])
        user =  await server.fetch_member(ctx.message.author.id)
        if(
            _get(
                user.roles,
                name=PUNDIT['playerroles']['base'][0]['role']
            ) or _get(
                user.roles,
                name=PUNDIT['playerroles']['base'][1]['role']
            )
        ):
            return await ctx.send(pundit.register(ctx.message.author))
        else:
            await user.add_roles(baserole)
            await ctx.send(pundit.register(ctx.message.author))
            await _get(_get(server.categories, name='general').channels, name="general").send(f"Yay, {user.name} just found the welcome flag!! Everybody please welcome {user.name}.\n{user.mention} take your time around the server, and I wish you all the very best on your tasks!!")
            
    elif(flag == PUNDIT['playerroles']['base'][1]['secret']):
        server = client.get_guild(id=PUNDIT['server'])
        baserole = _get(
            server.roles, name=PUNDIT['playerroles']['base'][1]['role'])
        user = await server.fetch_member(ctx.message.author.id)
        if(
            _get(
                user.roles,
                name=PUNDIT['playerroles']['base'][1]['role']
            ) or _get(
                user.roles,
                name=PUNDIT['playerroles']['base'][0]['role']
            )
        ):
            await ctx.send(pundit.register(ctx.message.author))
            return
        else:
            await user.add_roles(baserole)
            await ctx.send(pundit.register(ctx.message.author))
            await _get(_get(server.categories, name='general').channels, name="general").send(f"Yay, {user.name} just found the welcome flag!! Everybody please welcome {user.name}.\n{user.mention} take your time around the server, and I wish you all the very best on your tasks!!")
    else:
        await ctx.send("Wrong flag, You sure you filled out the form?? \nIf you're stuck. please ask for help!!!")



@client.command()
async def coin(ctx):
    """
    Flip a coin
    """
    await ctx.send(f"Oh!! it's {random.choice(['heads', 'tails'])}")


@client.command()
async def die(ctx):
    """
    Roll a die
    """
    await ctx.send(f"Hey, it's a {random.randint(1,6)}")


@client.command()
async def ping(ctx):
    """
    !!Knock Knock!!
    """
    await ctx.send("Pong!")


@client.command()
@commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
async def joke(ctx, *params):
    """
    Tell a joke

    !joke       -  Tell a joke
    !joke geek  -  Tell a geek joke
    !joke cn    -  Tell a Chuck Norris Joke
    """
    if not len(params):
        joke = get(
            'https://official-joke-api.appspot.com/jokes/general/random').json()[0]
        await ctx.send(joke['setup'])
        sleep(random.randint(1, 4))
        await ctx.send(joke['punchline'])
    elif params[0] == 'geek':
        joke = get(
            'https://official-joke-api.appspot.com/jokes/programming/random').json()[0]
        await ctx.send(joke['setup'])
        sleep(random.randint(1, 4))
        await ctx.send(joke['punchline'])
    elif params[0] == 'cn':
        joke = get(
            "http://api.icndb.com/jokes/random?exclude=[explicit]&escape=javascript").json()
        await ctx.send(joke["value"]["joke"])
    else:
        await ctx.send("No proper tag selected!!")


def launch(client):
    for extension in extensions:
        client.load_extension(f'extensions.{extension}')
        print(f"Loaded {extension}")
    client.run(TOKEN)


# if(sys.argv):
#     system("""find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf""")
launch(client)